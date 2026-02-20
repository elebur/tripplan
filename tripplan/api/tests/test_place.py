import pytest


@pytest.mark.django_db
class TestCreation:
    def test_creation(self, client):
        assert 1 == 2

    def test_duplicated_place(self, client):
        assert 1 == 2

    def test_more_than_allowed(self, client):
        assert 1 == 2

    def test_invalid_place_artic_id(self, client):
        assert 1 == 2

    def test_for_non_existing_project(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestGetSingleRecord:
    def test_get(self, client):
        assert 1 == 2

    def test_non_existing_project(self, client):
        assert 1 == 2


    def test_non_existing_place(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestGetList:
    def test_one_place(self, client):
        assert 1 == 2

    def test_multiple_places(self, client):
        assert 1 == 2

    def test_non_existing_project(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestUpdateNote:
    def test_update(self, client):
        assert 1 == 2

    def test_without_body(self, client):
        assert 1 == 2

    def test_empty_note_text(self, client):
        assert 1 == 2

    def test_non_existing_project(self, client):
        assert 1 == 2

    def test_non_existing_place(self, client):
        assert 1 == 2


@pytest.mark.django_db
class TestToggleVisited:
    def test_from_false_to_true(self, client):
        assert 1 == 2

    def test_from_true_to_false(self, client):
        assert 1 == 2

    def test_non_existing_project(self, client):
        assert 1 == 2

    def test_non_existing_place(self, client):
        assert 1 == 2
