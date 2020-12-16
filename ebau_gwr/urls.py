from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("api/v1/", include("ebau_gwr.core.urls"),),
    path("api/v1/linker/", include("ebau_gwr.linker.urls"),),
]
