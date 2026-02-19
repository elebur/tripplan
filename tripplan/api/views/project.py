from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.seralizers import ProjectSerializer
from api.views.services import validate_and_cache_initial_places
from core.models import Place, Project, ProjectPlace


@api_view(["GET"])
def list_projects(request: Request) -> Response:
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_project(request: Request) -> Response:
    serializer = ProjectSerializer(data=request.data)

    status_code = status.HTTP_400_BAD_REQUEST

    if not serializer.is_valid():
        return Response({"details": serializer.errors}, status=status_code)
    init_places = serializer.validated_data.pop("initial_places", None)
    if init_places:
        success, details = validate_and_cache_initial_places(init_places)
        if not success:
            return Response({"details": details}, status=status_code)

    project = serializer.save()

    if init_places:
        project_with_places = [
            ProjectPlace(project=project, place=Place.objects.get(artic_id=pl_id)) for pl_id in init_places
        ]

        ProjectPlace.objects.bulk_create(project_with_places)

    status_code = status.HTTP_201_CREATED
    result = {"project_id": serializer.data["id"]}


    return Response(result, status=status_code)


@csrf_exempt
def process_project(request: Request, pk) -> Response | HttpResponseNotAllowed:
    if request.method == "GET":
        return get_project(request, pk)
    if request.method == "DELETE":
        return delete_project(request, pk)
    if request.method == "PUT":
        return update_project(request, pk)

    msg = f"""{{"detail": "Method \\"{request.method}\\" not allowed."}}"""
    return HttpResponseNotAllowed(content=msg, permitted_methods=("GET", "POST", "PUT"))


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


@api_view(["PUT"])
def update_project(request: Request, pk: int) -> Response:
    project = get_object_or_404(Project, pk=pk)
    serializer = ProjectSerializer(project, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
