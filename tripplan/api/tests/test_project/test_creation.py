import pytest
from rest_framework.status import HTTP_201_CREATED

ENDPOINT = "/api/project/"


@pytest.mark.django_db
class TestSuccessCreation:
    def test_with_all_data_provided(self, client):

        payload = {
            "name": "New Name",
            "description": "Description",
            "start_date": "2026-12-23",
            "initial_places": [
                2, 2147476052, 2147478067
            ]
        }
        resp = client.post(ENDPOINT, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_without_initial_places(self, client):

        payload = {
            "name": "New Name",
            "description": "Description",
            "start_date": "2026-12-23",
        }
        resp = client.post(ENDPOINT, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_without_description(self, client):

        payload = {
            "name": "New Name",
            "start_date": "2026-12-23",
            "initial_places": [
                2, 2147476052, 2147478067
            ]
        }
        resp = client.post(ENDPOINT, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_without_start_date(self, client):

        payload = {
            "name": "New Name",
            "description": "Description",
            "initial_places": [
                2, 2147476052, 2147478067
            ]
        }
        resp = client.post(ENDPOINT, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_only_name_provide(self, client):

        payload = {
            "name": "New Name"
        }
        resp = client.post(ENDPOINT, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED