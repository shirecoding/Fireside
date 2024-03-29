# Generated by Django 4.1.4 on 2023-01-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fireside", "0009_remove_event_tpath_alter_eventhandler_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="fpath",
            field=models.CharField(
                help_text="Path to the function to be run (eg. path.to.function)",
                max_length=256,
                null=True,
                unique=True,
            ),
        ),
    ]
