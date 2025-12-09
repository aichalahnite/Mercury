import time
import logging
logger = logging.getLogger("gateway_logger")

class ResponseLoggingMiddleware:
    """
    Logs every request:
        - user
        - role
        - path
        - duration
        - trace_id
        - selected service (from Layer B)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)

        duration = round((time.time() - start) * 1000, 2)

        logger.info({
            "trace_id": getattr(request, "trace_id", None),
            "user": request.user.username if request.user.is_authenticated else "anon",
            "role": getattr(request.user, "role", None) if request.user.is_authenticated else None,
            "path": request.path,
            "services": getattr(request, "service_route", {}),
            "status": response.status_code,
            "duration_ms": duration,
        })

        return response
