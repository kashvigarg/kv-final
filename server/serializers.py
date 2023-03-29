from rest_framework import serializers
from . import models

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        model = models.File
        fields = "__all__"