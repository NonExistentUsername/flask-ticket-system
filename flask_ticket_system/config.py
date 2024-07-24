import os


def get_secret_key() -> str:
    return os.environ.get("SECRET_KEY", "secret")
