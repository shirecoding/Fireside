from django.db import models
from fireside.models import Model

# Create your models here.
class BasicShipModel(Model):
    type = models.CharField(max_length=255, default="Basic", help_text="Ship type.")
    name = models.CharField(max_length=255, blank=False, help_text="Ship name.")
