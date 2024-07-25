from flask import Response, request
from pydantic import BaseModel, ValidationError


def model_middleware(model: type[BaseModel]):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = request.data
            try:
                model_instance = model.model_validate_json(data, strict=True)
            except ValidationError as e:
                return Response(str(e.json()), status=400)
            except Exception as e:
                return Response(f"Internal server error: {str(e)}", status=500)
            return func(model_instance, *args, **kwargs)

        return wrapper

    return decorator


def authorization_middleware(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response("Unauthorized", status=401)
        return func(token, *args, **kwargs)

    return wrapper
