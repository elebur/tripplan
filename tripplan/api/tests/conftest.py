import sys
from pathlib import Path

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient


sys.path.append(str(Path(__file__).resolve().parent))

class _JsonAPIClient(APIClient):
    """
    A simple wrapper to get rid of typing 'format="json"' in each
    POST request.
    """
    def post(self, path, data=None, format="json", content_type=None,
             follow=False, **extra) -> Response:
        return super().post(
            path,
            data=data,
            format=format,
            content_type=content_type,
            follow=follow,
            **extra,
        )


@pytest.fixture
def client():
    return _JsonAPIClient()
