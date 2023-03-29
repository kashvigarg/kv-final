from django.db import models

# Create your models here.
class File(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=100)