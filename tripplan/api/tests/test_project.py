import pytest
from rest_framework.status import HTTP_201_CREATED


@pytest.mark.django_db
class TestSuccessCreation:
    endpoint = "/api/project/"

    def test_with_all_data_provided(self, client):
        payload = {
            "name": "New Name",
            "description": "Description",
            "start_date": "2026-12-23",
            "initial_places": [
                2, 2147476052, 2147478067
            ]
        }
        resp = client.post(self.endpoint, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_without_initial_places(self, client):

        payload = {
            "name": "New Name",
            "description": "Description",
            "start_date": "2026-12-23",
        }
        resp = client.post(self.endpoint, payload)

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
        resp = client.post(self.endpoint, payload)

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
        resp = client.post(self.endpoint, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_only_name_provide(self, client):

        payload = {
            "name": "New Name",
        }
        resp = client.post(self.endpoint, payload)

        assert resp.text == '{"project_id":1}'
        assert resp.status_code == HTTP_201_CREATED

    def test_with_name_exactly_max_length(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestFailCreation:
    def test_creation_without_name(self, client):
        assert 1 == 2

    def test_name_longer_than_allowed(self, client):
        assert 1 == 2

    def test_creation_with_malformed_date(self, client):
        assert 1 == 2

    def test_creation_with_too_many_initial_places(self, client):
        assert 1 == 2

    def test_creation_with_duplicated_initial_places(self, client):
        assert 1 == 2

    def test_creation_with_invalid_initial_places(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestGetProject:
    def test_existing_project(self, client):
        assert 1 == 2

    def test_non_existing_project(self, client):
        assert 1 == 2

    def test_without_id(self, client):
        assert 1 == 2

@pytest.mark.django_db
class TestProjectDeletion:
    def test_success_deletion_project_without_places(self, client):
        assert 1 == 2

    def test_success_deletion_project_with_places(self, client):
        # Make sure ProjectPlace pairs deletion.
        assert 1 == 2

    def test_deletion_for_non_existing_project(self, client):
        assert 1 == 2

    def test_deletion_for_project_with_visited_places(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestProjectUpdating:
    def test_update_name(self, client):
        assert 1 == 2

    def test_update_description(self, client):
        assert 1 == 2

    def test_update_start_date(self, client):
        assert 1 == 2

    def test_update_malformed_start_date(self, client):
        assert 1 == 2

    def test_updating_non_existing_project(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestListProjects:
    def test_get_list_of_projects_for_one_project(self, client):
        assert 1 == 2

    def test_get_list_of_projects_for_multiple_projects(self, client):
        assert 1 == 2

    def test_get_list_of_projects_for_zero_projects(self, client):
        assert 1 == 2