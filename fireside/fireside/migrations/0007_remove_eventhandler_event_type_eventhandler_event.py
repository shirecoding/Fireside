# Generated by Django 4.1.4 on 2023-01-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fireside", "0006_event_eventhandler"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventhandler",
            name="event_type",
        ),
        migrations.AddField(
            model_name="eventhandler",
            name="event",
            field=models.CharField(
                default="",
                help_text="The event which the event handler listens for.",
                max_length=256,
            ),
            preserve_default=False,
        ),
    ]
