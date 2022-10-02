from django.db import models
from fireside.models import Model, ActivatableModel

# Create your models here.
class BasicShipModel(Model, ActivatableModel):
    type = models.CharField(max_length=255, default="Basic", help_text="Ship type.")
    name = models.CharField(max_length=255, blank=False, help_text="Ship name.")
    last_serviced_on = models.DateTimeField(auto_now_add=True)
