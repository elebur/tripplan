from django.urls import path

from api.views.project import create_project, list_projects, process_project
from api.views.place import create_place

urlpatterns = [
    path("project/", create_project, name="create_project"),
    path("projects/", list_projects, name="list_projects"),
    path("project/<int:pk>/", process_project, name="process_project"),
    path("project/<int:project_id>/place/", create_place, name="create_place"),
]
