# Generated by Django 4.1.4 on 2022-12-23 10:23

from django.db import migrations, models

import fireside.utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_room_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="uid",
            field=models.CharField(
                default=fireside.utils.utils.generate_uuid,
                editable=False,
                max_length=32,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
