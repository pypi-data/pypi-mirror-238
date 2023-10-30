from functools import wraps


def validate_id_or_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id_or_name = kwargs.get("id_or_name", args[1] if len(args) > 1 else None)
        if not id_or_name:
            raise ValueError("Either the id or name must be provided.")
        return func(*args, **kwargs)

    return wrapper


def validate_id(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id = kwargs.get("id", args[1] if len(args) > 1 else None)
        if not id:
            raise ValueError("The id must be provided.")
        return func(*args, **kwargs)

    return wrapper


def validate_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name", args[1] if len(args) > 1 else None)
        if not name:
            raise ValueError("The name must be provided.")
        return func(*args, **kwargs)

    return wrapper


def validate_id_or_name_alt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        id_or_name = kwargs.get("id_or_name", args[2] if len(args) > 2 else None)
        if not id_or_name:
            raise ValueError("Either the id or name must be provided.")
        return func(*args, **kwargs)

    return wrapper
