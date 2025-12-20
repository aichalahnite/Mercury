from functools import wraps


def login_required(fn):
    """
    Ensures the user is authenticated in GraphQL resolvers
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        info = args[1]  # (self, info, ...)
        user = info.context.user

        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    """
    Ensures the user is authenticated AND admin
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = info.context.user

        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        if getattr(user, "role", None) != "admin":
            raise Exception("Admins only")

        return fn(*args, **kwargs)

    return wrapper
