from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

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


@api_view(["GET"])
def get_project(request: Request, pk: int) -> Response:
    p = get_object_or_404(Project, pk=pk)
    serial = ProjectSerializer(p, many=False)
    return Response(serial.data)
