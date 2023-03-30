from rest_framework import serializers
from . import models
from server.models import File

class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = File
        fields = "__all__"
