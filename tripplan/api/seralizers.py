from core import models

from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    initial_places = serializers.ListField(
        child=serializers.IntegerField(), required=False)

    class Meta:
        model = models.Project
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = ["artic_id"]


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectPlace
        fields = "__all__"
