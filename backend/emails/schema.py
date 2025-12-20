# # emails/schema.py
# import graphene
# from emails.mock_service import mock_service
# from scanner.service_selector import try_real_send_email

# class SendEmail(graphene.Mutation):
#     class Arguments:
#         to = graphene.String(required=True)
#         subject = graphene.String(required=True)
#         body = graphene.String(required=True)

#     status = graphene.String()
#     used = graphene.String()

#     def mutate(self, info, to, subject, body):
#         request = info.context

#         if not request.user.is_authenticated:
#             raise Exception("Authentication required")

#         route = request.service_route.get("mailserver", "mock")

#         if route == "real":
#             res = try_real_send_email({
#                 "to": to,
#                 "subject": subject,
#                 "body": body,
#             })
#         else:
#             res = mock_service.send_email(to, subject, body)

#         return SendEmail(
#             status=res.get("status", "sent"),
#             used=route,
#         )


# class Query(graphene.ObjectType):
#     pass


# class Mutation(graphene.ObjectType):
#     send_email = SendEmail.Field()

import graphene
from graphene_django import DjangoObjectType
from backend.common.graphql_permissions import login_required
from emails.models import Email
from scanner.models import ScanLog


class ScanLogType(DjangoObjectType):
    class Meta:
        model = ScanLog
        fields = ("result", "confidence", "scanned_at")


class EmailType(DjangoObjectType):
    scan = graphene.Field(ScanLogType)

    class Meta:
        model = Email
        fields = (
            "id",
            "sender",
            "subject",
            "body",
            "created_at",
            "is_outgoing",
        )

    def resolve_scan(self, info):
        return getattr(self, "scan", None)

class Query(graphene.ObjectType):
    my_emails = graphene.List(
        EmailType,
        limit=graphene.Int(default_value=50),
        offset=graphene.Int(default_value=0),
    )

    email = graphene.Field(EmailType, id=graphene.Int(required=True))

    @login_required
    def resolve_my_emails(self, info, limit, offset):
        return Email.objects.filter(
            user=info.context.user
        ).order_by("-created_at")[offset:offset + limit]

    @login_required
    def resolve_email(self, info, id):
        email = Email.objects.get(id=id)
        if email.user != info.context.user:
            raise Exception("Forbidden")
        return email
