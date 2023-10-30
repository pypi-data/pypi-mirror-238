from dennis_systems.core.shared_lib.auth.Authorization import Authorization
from django.core import serializers
from django.http import JsonResponse, HttpRequest

from dennis_systems.core.shared_lib.entity.BaseModel import BaseModel
from dennis_systems.core.shared_lib.service.DefaultService import DefaultService


class ApiDefault:
    __service: DefaultService

    def list(self, request: HttpRequest,  limit: int, page: int) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.list(limit, page))
        pass

    def save(self, item: BaseModel, request: HttpRequest) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(serializers.serialize("xml", self.getService().save(item).objects.all()), safe=False)

    def delete(self, request: HttpRequest, item: BaseModel) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.delete(item))

    def get(self, request : HttpRequest,  id: int) -> JsonResponse:
        self.check_token(request);
        return JsonResponse(self.__service.get(id), safe=False)

    def getService(self):
        return self.__service

    @staticmethod
    def toModel(model):
        return JsonResponse(model)
    @staticmethod
    def check_token(request: HttpRequest) -> None:
        if not Authorization.has_auth_token(request):
            print('not token')
        else:
            print('token_found')
            Authorization.parce_token(request)
