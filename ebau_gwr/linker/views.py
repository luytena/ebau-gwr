from rest_framework_json_api import pagination, parsers, renderers, views

from . import models, serializers
from .filters import GWRLinkFilterSet


class GWRLinkViewSet(views.ModelViewSet):
    serializer_class = serializers.GWRLinkSerializer
    queryset = models.GWRLink.objects.all()
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.JSONParser,)
    filterset_class = GWRLinkFilterSet
    pagination_class = pagination.JsonApiPageNumberPagination
