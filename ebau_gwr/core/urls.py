from rest_framework.routers import SimpleRouter

from .views import ConstructionProjectView, SearchView

r = SimpleRouter(trailing_slash=False)

r.register(r"search", SearchView, basename="search")
r.register(
    r"construction_project", ConstructionProjectView, basename="construction-project"
)

urlpatterns = r.urls
