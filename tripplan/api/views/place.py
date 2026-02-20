from tripplan.settings import MAX_ALLOWED_PLACES_PER_PROJECT
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.seralizers import PlaceSerializer, ProjectPlaceSerializer
from api.views.services import fetch_and_cache_single_place
from core.models import Place, Project, ProjectPlace


@api_view(["POST"])
def create_place(request: Request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)

    serializer = PlaceSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    place = fetch_and_cache_single_place(serializer.validated_data["artic_id"])
    if not place:
        return Response(
            {"details": "Invalid place ID"}, status=status.HTTP_400_BAD_REQUEST)

    if ProjectPlace.objects.select_related("project", "place").filter(project=project, place=place).exists():
        msg = f"project<{project.id}> already has this place"
        return Response({"details": msg}, status=status.HTTP_400_BAD_REQUEST)

    if ProjectPlace.objects.select_related("project").filter(project=project).count() >= MAX_ALLOWED_PLACES_PER_PROJECT:
        msg = f"project<{project.id}> already has maximum allowed places."
        return Response({"details": msg}, status=status.HTTP_400_BAD_REQUEST)

    ProjectPlace.objects.create(project=project, place=place)

    return Response(
        {"project_id": project.id, "place_id": place.id}, status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def list_places(request: Request, project_id: int):
    places = ProjectPlace.objects.select_related("place", "project").filter(project__id=project_id)
    serializer = ProjectPlaceSerializer(places, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def update_notes(request: Request, project_id: int, place_id: int) -> Response:
    input_data_serializer = ProjectPlaceSerializer(data=request.data, many=False)
    if not input_data_serializer.is_valid():
        return Response(
            {"details": input_data_serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    obj = get_object_or_404(ProjectPlace, project__id=project_id, place__id=place_id)
    obj.notes = input_data_serializer.validated_data["notes"]
    obj.save()
    serializer = ProjectPlaceSerializer(obj, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)
