from django.db import models
import uuid


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    @property
    def uid(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=64, unique=True)
    categories = models.ManyToManyField(Category)
    short_description = models.CharField(max_length=64)
    long_description = models.TextField(max_length=4096)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    @property
    def uid(self):
        return self.name


class GameInstance(models.Model):
    uid = models.CharField(default=uuid.uuid4, max_length=64, unique=True)
    game = models.ForeignKey(Game, related_name="instances", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game.name}_{self.uid}"
