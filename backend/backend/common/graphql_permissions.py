from functools import wraps

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        info = args[1]  # (self, info, ...)
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        if user.role != "admin":
            raise Exception("Admins only")

        return fn(*args, **kwargs)
    return wrapper
