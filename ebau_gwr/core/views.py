from requests import HTTPError
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from .formatters import delivery, getConstructionProject
from .hs_client import HousingStatClient


class ValidateViewMixin:
    def validate(self, request):
        for param in self.required_params:
            if param not in request.GET:
                raise ValidationError(f'Missing query param "{param}"')


class SearchView(ValidateViewMixin, ListModelMixin, GenericViewSet):
    filter_backends = []
    serializer_class = serializers.ConstructionProjectsListSerializer
    required_params = ("dept_no", "hs_token")

    def get_queryset(self):
        data = dict(self.request.GET.items())
        dept_no = data["dept_no"]
        hs_token = data["hs_token"]
        xml = delivery(getConstructionProject=getConstructionProject(dept_no, data))
        xml = xml.toxml(encoding="utf-8")

        # TODO: the housing stat api does not support version 2 yet
        xml = xml.replace(b"eCH-0216/2", b"eCH-0216/1")

        hsc = HousingStatClient(auth_token=hs_token)
        resp = hsc.get(query=xml)
        data_list = resp.getConstructionProjectResponse.constructionProjectsList
        return data_list

    def list(self, request, *args, **kwargs):
        self.validate(request)
        try:
            return super().list(request, *args, **kwargs)
        except HTTPError as e:
            return Response(
                status=e.response.status_code,
                data={"hs_error": e.response.content.decode()},
            )


class ConstructionProjectView(ValidateViewMixin, RetrieveModelMixin, GenericViewSet):
    filter_backends = []
    serializer_class = serializers.ConstructionProjectsCompleteSerializer
    lookup_field = "eproid"
    required_params = ("hs_token",)

    def get_object(self):
        data = dict(self.request.GET.items())
        hs_token = data["hs_token"]
        eproid = self.kwargs["eproid"]

        hsc = HousingStatClient(auth_token=hs_token)
        resp = hsc.get(path=f"constructionprojects/{eproid}")
        return resp.constructionProjectCompleteResponse

    def retrieve(self, request, *args, **kwargs):
        self.validate(request)
        try:
            return super().retrieve(request, *args, **kwargs)
        except HTTPError as e:
            return Response(
                status=e.response.status_code,
                data={"hs_error": e.response.content.decode()},
            )
