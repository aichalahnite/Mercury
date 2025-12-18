# emails/schema.py
import graphene
from emails.mock_service import mock_service
from scanner.service_selector import try_real_send_email

class SendEmail(graphene.Mutation):
    class Arguments:
        to = graphene.String(required=True)
        subject = graphene.String(required=True)
        body = graphene.String(required=True)

    status = graphene.String()
    used = graphene.String()

    def mutate(self, info, to, subject, body):
        request = info.context

        if not request.user.is_authenticated:
            raise Exception("Authentication required")

        route = request.service_route.get("mailserver", "mock")

        if route == "real":
            res = try_real_send_email({
                "to": to,
                "subject": subject,
                "body": body,
            })
        else:
            res = mock_service.send_email(to, subject, body)

        return SendEmail(
            status=res.get("status", "sent"),
            used=route,
        )


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    send_email = SendEmail.Field()
