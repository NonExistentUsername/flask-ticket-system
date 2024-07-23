from flask import Response, request
from pydantic import BaseModel, ValidationError


def model_middleware(model: type[BaseModel]):
    def decorator(func, *args, **kwargs):
        def wrapper():
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
