from django.db import models
import uuid


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    short_description = models.CharField(max_length=64, default="", blank=True)
    long_description = models.TextField(max_length=4096, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    websocket = models.CharField(
        max_length=512, blank=True, null=True, help_text="eg. ws://127.0.0.1:8080/ws"
    )

    def __str__(self):
        return self.name


class GameInstance(models.Model):
    uid = models.CharField(
        default=uuid.uuid4, max_length=64, unique=True, primary_key=True
    )
    game = models.ForeignKey(Game, related_name="instances", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game.name}_{self.uid}"
