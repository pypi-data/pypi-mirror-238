import jwt
import requests
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest

from dennis_systems.core.shared_lib.auth.AuthorizationResponse import AuthorizationResponse
from dennis_systems.core.shared_lib.utils.utils import file_utils


class Authorization:
    __AUTH = 'Authentication'

    @staticmethod
    def has_auth_token(request: HttpRequest) -> bool:
        return request.headers.get(Authorization.__AUTH) is not None

    @staticmethod
    def parce_token(request: HttpRequest) -> AuthorizationResponse:
        if not Authorization.has_auth_token(request):
            raise PermissionDenied("global.auth.no_token")

        token_reader = file_utils.read_from_file("../../../token.jwt")
        decoded = jwt.decode(request.headers.get(Authorization.__AUTH), token_reader, algorithms=["HS256"])

        print(decoded)

        return AuthorizationResponse()

    @staticmethod
    def authorize(path, login, password):
        return requests.post(path, json={"login": login, "password": password}).json()
