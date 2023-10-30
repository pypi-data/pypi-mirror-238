import jwt
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from AuthorizationResponse import AuthorizationResponse
from utils import file_utils


class Authorization:
    __AUTH = 'Authentication'

    @staticmethod
    def has_auth_token(request: HttpRequest) -> bool:
        return request.headers.get(Authorization.__AUTH) is not None

    def parce_token(self, request: HttpRequest) -> AuthorizationResponse:
        if not self.has_auth_token(request):
            raise PermissionDenied("global.auth.no_token")

        token_reader = file_utils.read_from_file("../../../token.jwt")
        decoded = jwt.decode(request.headers.get(Authorization.__AUTH), token_reader, algorithms=["HS256"])

        print(decoded)

        return AuthorizationResponse()
