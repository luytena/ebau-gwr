from rest_framework.routers import SimpleRouter

from .views import SearchView

r = SimpleRouter(trailing_slash=False)

r.register(r"search", SearchView, basename="search")

urlpatterns = r.urls
