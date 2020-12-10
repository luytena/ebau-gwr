import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from ebau_gwr.core.tests.mock_xml import xml_data


def test_search_view(admin_client, requests_mock, snapshot):
    requests_mock.get(
        f"{settings.HS_BASE_URI}/constructionprojects",
        content=xml_data("getConstructionProjectResponse"),
    )
    url = reverse("search-list")
    resp = admin_client.get(url, {"dept_no": 134200, "hs_token": "token"})
    snapshot.assert_match(resp.json())


@pytest.mark.parametrize("missing_param", ["dept_no", "hs_token"])
def test_search_view_400(admin_client, missing_param):
    url = reverse("search-list")
    data = {"dept_no": 134200, "hs_token": "token"}
    data.pop(missing_param)
    resp = admin_client.get(url, data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == [f'Missing query param "{missing_param}"']


@pytest.mark.parametrize(
    "status_code,msg",
    [
        (400, "You should feel bad!"),
        (
            400,
            '<?xml version="1.0" encoding="UTF-8"?><errors><error>Construction project does not found</error></errors>',
        ),
        (500, "I should feel bad!"),
        (401, "These are not the droids you're looking for"),
    ],
)
def test_search_view_external_error(admin_client, requests_mock, status_code, msg):
    requests_mock.get(
        f"{settings.HS_BASE_URI}/constructionprojects",
        status_code=status_code,
        text=msg,
    )
    url = reverse("search-list")
    resp = admin_client.get(url, {"dept_no": 134200, "hs_token": "token"})
    assert resp.status_code == status_code
    assert resp.json() == {"hs_error": msg}


def test_construction_project_view(admin_client, requests_mock, snapshot):
    requests_mock.get(
        f"{settings.HS_BASE_URI}/constructionprojects/193052735",
        content=xml_data("constructionProjectCompleteResponse"),
    )
    url = reverse("construction-project-detail", args=["193052735"])
    resp = admin_client.get(url, {"hs_token": "token"})
    assert resp.status_code == status.HTTP_200_OK
    snapshot.assert_match(resp.json())


@pytest.mark.parametrize(
    "status_code,msg",
    [
        (400, "You should feel bad!"),
        (500, "I should feel bad!"),
        (401, "These are not the droids you're looking for"),
    ],
)
def test_construction_project_view_external_error(
    admin_client, requests_mock, status_code, msg
):
    requests_mock.get(
        f"{settings.HS_BASE_URI}/constructionprojects/193052735",
        status_code=status_code,
        text=msg,
    )
    url = reverse("construction-project-detail", args=["193052735"])
    resp = admin_client.get(url, {"hs_token": "token"})
    assert resp.status_code == status_code
    assert resp.json() == {"hs_error": msg}
