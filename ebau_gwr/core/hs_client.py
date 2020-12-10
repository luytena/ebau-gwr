import logging
from base64 import urlsafe_b64encode
from hashlib import sha256

import requests
from django.conf import settings
from django.core.cache import cache
from pyxb import IncompleteElementContentError, UnprocessedElementContentError

from ebau_gwr.core.schema.ech_0216_2_0 import CreateFromDocument

logger = logging.getLogger(__name__)


class _HousingStatSession:
    """ContextManager for handling cached `requests.Session()`."""

    def __init__(self, token):
        if isinstance(token, str):
            token = token.encode()
        _hash = sha256(token)
        _id = urlsafe_b64encode(_hash.digest()).decode()
        self.key = f"housing_stat_session_{_id}"
        self.session = cache.get(self.key, requests.session())

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            cache.set(self.key, self.session, 7200)


class HousingStatClient:
    def __init__(self, auth_token, base_uri=settings.HS_BASE_URI):
        self.auth_token = auth_token
        self.base_uri = base_uri

    def _request(self, method_name, *args, **kwargs):
        with _HousingStatSession(self.auth_token) as session:
            response = getattr(session, method_name)(*args, **kwargs)
        response.raise_for_status()
        return response

    def _fix_housing_stat_response(self, content: bytes):
        """
        Fix housing stat api responses.

        The housing stat API has bugs that make it impossible to validate it's responses
        against the schema. Here we fix them, so it's at least valid.
        """
        # Fix wrong schema version in namespace definition
        content = content.replace(b"eCH-0216/1", b"eCH-0216/2")
        # Fix empty volume should be nil or omitted
        content = content.replace(b"<ns2:volume/>\n", b"")
        # Fix empty otherID could be omitted, can't be nil
        content = content.replace(
            b'<ns2:otherID xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>\n',
            b"",
        )
        # Fix empty otherID could be nil or omitted
        content = content.replace(b"<ns2:dateOfConstruction/>\n", b"")
        # Fix typeOfPermit: 0 not allowed
        content = content.replace(b"<ns2:typeOfPermit>0</ns2:typeOfPermit>\n", b"")
        # Fix coordinates: could be omitted
        content = content.replace(b"<ns2:coordinates/>\n", b"")
        return content

    def get(self, path="constructionprojects", query=None, headers=None):
        if headers is None:
            headers = {}
        headers["token"] = self.auth_token
        if query is not None:
            headers["query"] = query
        url = "/".join([self.base_uri, path])
        response = self._request("get", url, headers=headers)

        # TODO: the housing stat api does not deliver valid XML yet
        content = self._fix_housing_stat_response(response.content)

        try:
            data = CreateFromDocument(content)
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
        ) as e:  # pragma: no cover
            # TODO: correctly report errors back
            logger.error(e.details())
            raise
        return data
