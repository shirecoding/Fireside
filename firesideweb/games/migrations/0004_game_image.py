# Generated by Django 3.2.6 on 2021-10-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0003_alter_game_long_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="image",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]
