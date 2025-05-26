import jwt
from pydantic import BaseModel, Field
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config.settings import env


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        print("Estas ingresando por el middleware de autenticacion")

class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    ...