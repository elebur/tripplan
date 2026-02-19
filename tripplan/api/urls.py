from django.urls import path

from api.views.project import create_project, get_project

urlpatterns = [
    path("project/", create_project, name="create_project"),
    path("project/<int:pk>/", get_project, name="get_project"),
]