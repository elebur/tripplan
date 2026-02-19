from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.seralizers import ProjectSerializer
from core.models import Project


@api_view(["POST"])
def create_project(request: Request) -> Response:
    serializer = ProjectSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        status_code = status.HTTP_201_CREATED
        result = {"project_id": serializer.data["id"]}
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        result = {"details": serializer.errors}

    return Response(result, status=status_code)


@csrf_exempt
def process_project(request: Request, pk) -> Response | HttpResponseNotAllowed:
    if request.method == "GET":
        return get_project(request, pk)
    if request.method == "DELETE":
        return delete_project(request, pk)

    msg = f"""{{"detail": "Method \\"{request.method}\\" not allowed."}}"""
    return HttpResponseNotAllowed(content=msg, permitted_methods=("GET", "POST"))


@api_view(["GET"])
def get_project(request: Request, pk: int) -> Response:
    p = get_object_or_404(Project, pk=pk)
    serial = ProjectSerializer(p, many=False)
    return Response(serial.data)


@api_view(["DELETE"])
def delete_project(request: Request, pk: int) -> Response:
    project = get_object_or_404(Project, pk=pk)
    project_id = project.id
    if project.places.filter(visited = True).exists():
        msg = (f"The project<{project_id}> cannot be deleted because it has "
               "places that were visited")
        raise ValidationError({"details": msg}, code=status.HTTP_409_CONFLICT)

    project.delete()
    return Response({"details": f"The project<{project_id}> has been deleted."})
