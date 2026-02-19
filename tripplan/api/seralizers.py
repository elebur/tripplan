from core import models

from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Place
        fields = "__all__"
