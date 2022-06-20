import pytest
from django.core.cache import cache
from pytest_factoryboy import register
from rest_framework.test import APIClient

from ebau_gwr.linker import factories as linker_factories
from ebau_gwr.oidc_auth.models import OIDCUser
from ebau_gwr.token_proxy import factories as token_proxy_factories

register(linker_factories.GWRLinkFactory)
register(token_proxy_factories.HousingStatCredsFactory)


@pytest.fixture
def admin_groups():
    return ["admin"]


@pytest.fixture
def admin_user(settings, admin_groups):
    return OIDCUser(
        "sometoken", {"sub": "admin", settings.OIDC_GROUPS_CLAIM: admin_groups}
    )


@pytest.fixture
def admin_client(db, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture(scope="function", autouse=True)
def _autoclear_cache():
    cache.clear()
