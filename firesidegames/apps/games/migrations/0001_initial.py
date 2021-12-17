# Generated by Django 3.2.6 on 2021-12-17 14:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=64, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "categories",
            },
        ),
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=64, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("short_description", models.CharField(max_length=64)),
                ("long_description", models.TextField(max_length=4096)),
                ("image", models.ImageField(blank=True, upload_to="")),
                ("categories", models.ManyToManyField(to="games.Category")),
            ],
        ),
        migrations.CreateModel(
            name="GameInstance",
            fields=[
                (
                    "uid",
                    models.CharField(
                        default=uuid.uuid4,
                        max_length=64,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="instances",
                        to="games.game",
                    ),
                ),
            ],
        ),
    ]
