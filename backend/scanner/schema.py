import graphene
from graphene_django import DjangoObjectType
from scanner.models import ScanLog
from scanner.service_selector import try_real_scan
from emails.mock_service import mock_service

from common.graphql_auth import require_admin

# =====================
# TYPES
# =====================

class ScanLogType(DjangoObjectType):
    class Meta:
        model = ScanLog
        fields = (
            "id",
            "sender",
            "subject",
            "result",
            "confidence",
            "scanned_at",
        )

# =====================
# QUERIES
# =====================
class Query(graphene.ObjectType):
    scan_logs = graphene.List(
        ScanLogType,
        result=graphene.String(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    def resolve_scan_logs(self, info, result=None, limit=50, offset=0):
    # 🔐 ROLE CHECK (HERE)
    require_admin(info.context.user)

    qs = ScanLog.objects.all().order_by("-scanned_at")

    if result:
        qs = qs.filter(result=result)

    return qs[offset : offset + limit]

# =====================
# MUTATIONS
# =====================

class ScanEmail(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        sender = graphene.String()
        subject = graphene.String()

    id = graphene.Int()
    result = graphene.String()
    confidence = graphene.Float()
    used = graphene.String()

    def mutate(self, info, body, sender=None, subject=None):
        request = info.context

        if not request.user.is_authenticated:
            raise Exception("Authentication required")

        route = request.service_route.get("scanner", "mock")

        if route == "real":
            scan = try_real_scan(body)
        else:
            scan = mock_service.scan_email(body)

        log = ScanLog.objects.create(
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
