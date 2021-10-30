from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=20)
    categories = models.ManyToManyField(Category)
    short_description = models.CharField(max_length=50)
    long_description = models.TextField(max_length=500)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name
