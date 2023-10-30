import jwt
import requests
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.http import JsonResponse

from dennis_systems.core.shared_lib.auth.AuthorizationResponse import AuthorizationResponse


class Authorization:
    __AUTH = 'Authorization'

    @staticmethod
    def has_auth_token(request: HttpRequest) -> bool:
        res =  request.headers.get(Authorization.__AUTH) is not None
        if not res:
            raise PermissionDenied
        return True

    @staticmethod
    def parce_token(request: HttpRequest) -> AuthorizationResponse:
        if not Authorization.has_auth_token(request):
           raise PermissionDenied("global.auth.no_token")

        item = str(request.headers.get(Authorization.__AUTH)).replace('Bearer ', '')
        token_reader = settings.AUTH_KEY
        decoded = jwt.decode(item, token_reader, algorithms=["RS7518"],   options={"verify_signature": False})

        print(decoded)

        return AuthorizationResponse()

    @staticmethod
    def authorize(path, login, password):
        return JsonResponse(requests.post(path, json={"login": login, "password": password},verify=False).json())
