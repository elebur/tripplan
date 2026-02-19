from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    start_date = models.DateField(null=True)



class Place(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=128, null=True)
    artic_id = models.BigIntegerField(null=True)
    notes = models.TextField(null=True)
    visited = models.BooleanField(default=False)
