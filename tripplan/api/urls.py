from django.urls import path

from api.views.project import create_project, process_project

urlpatterns = [
    path("project/", create_project, name="create_project"),
    path("project/<int:pk>/", process_project, name="process_project"),
]
