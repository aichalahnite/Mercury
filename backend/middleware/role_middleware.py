from django.http import JsonResponse

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        required_role = getattr(request, "required_role", None)

        if required_role:
            user = request.user
            if not user.is_authenticated or user.role != required_role:
                return JsonResponse({"error": "Forbidden"}, status=403)

        return self.get_response(request)
