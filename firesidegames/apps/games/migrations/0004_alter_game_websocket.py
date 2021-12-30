# Generated by Django 3.2.6 on 2021-12-30 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0003_game_websocket"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="websocket",
            field=models.CharField(
                blank=True,
                help_text="eg. ws://127.0.0.1:8080/ws",
                max_length=512,
                null=True,
            ),
        ),
    ]
