from rest_framework import serializers
from . import models
from server.models import File

class UploadSerializer(serializers.Serializer):
    class Meta:
        model = File
        fields = {'file'}