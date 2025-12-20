# scanner/schema.py
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from scanner.models import ScanLog
from scanner.service_selector import try_real_scan
from emails.mock_service import mock_service

from backend.common.graphql_permissions import login_required, admin_required

# ===================== TYPES =====================
class ScanLogType(DjangoObjectType):
    class Meta:
        model = ScanLog
        fields = (
            "id",
            "user",
            "sender",
            "subject",
            "body",
            "result",
            "confidence",
            "scanned_at",
        )

# ===================== QUERIES =====================
class Query(graphene.ObjectType):
    # Admin-only: see all emails
    scan_logs = graphene.List(
        ScanLogType,
        result=graphene.String(),
        limit=graphene.Int(default_value=50),
        offset=graphene.Int(default_value=0),
    )

    # User-only: see their own emails
    my_scan_logs = graphene.List(
        ScanLogType,
        limit=graphene.Int(default_value=50),
        offset=graphene.Int(default_value=0),
    )

    @login_required
    @admin_required
    def resolve_scan_logs(self, info, result=None, limit=50, offset=0):
        qs = ScanLog.objects.all().order_by("-scanned_at")
        if result:
            qs = qs.filter(result=result)
        return qs[offset:offset + limit]

    @login_required
    def resolve_my_scan_logs(self, info, limit=50, offset=0):
        user = info.context.user
        qs = ScanLog.objects.filter(user=user).order_by("-scanned_at")
        return qs[offset:offset + limit]

# ===================== MUTATIONS =====================
class ScanEmail(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        sender = graphene.String()
        subject = graphene.String()

    id = graphene.Int()
    result = graphene.String()
    confidence = graphene.Float()
    used = graphene.String()

    @login_required
    def mutate(self, info, body, sender=None, subject=None):
        user = info.context.user  # <-- Attach the user here

        # Decide which scanner to use
        route = info.context.service_route.get("scanner", "mock")

        if route == "real":
            scan = try_real_scan(body)
        else:
            scan = mock_service.scan_email(body)

        # Create ScanLog linked to the user
        log = ScanLog.objects.create(
            user=user,  # <-- important: assign user here
            sender=sender,
            subject=subject,
            body=body,
            result="malicious" if scan["malicious"] else "safe",
            confidence=scan["confidence"],
        )

        return ScanEmail(
            id=log.id,
            result=log.result,
            confidence=log.confidence,
            used=route,
        )


class Mutation(graphene.ObjectType):
    scan_email = ScanEmail.Field()

# ===================== SUBSCRIPTIONS (placeholder) =====================
class Subscription(graphene.ObjectType):
    new_scan = graphene.Field(ScanLogType)

    async def subscribe_new_scan(root, info):
        # Placeholder for Channels + Redis
        pass
