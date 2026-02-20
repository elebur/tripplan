from django.urls import path

from api.views.project import create_project, list_projects, process_project
from api.views.place import (
    get_place,
    create_place,
    update_notes,
    list_places,
    toggle_visited,
)

urlpatterns = [
    path("project/", create_project, name="create_project"),
    path("projects/", list_projects, name="list_projects"),
    path("project/<int:pk>/", process_project, name="process_project"),
    path("project/<int:project_id>/place/", create_place, name="create_place"),
    path(
        "project/<int:project_id>/place/<int:place_id>/",
        get_place,
        name="get_place"
    ),
    path("project/<int:project_id>/places/", list_places, name="list_places"),
    path(
        "project/<int:project_id>/place/<int:place_id>/notes/",
        update_notes,
        name="update_notes"
    ),
    path(
        "project/<int:project_id>/place/<int:place_id>/visit/",
        toggle_visited,
        name="toggle_visited"
    ),
]
