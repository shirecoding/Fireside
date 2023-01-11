# Generated by Django 4.1.4 on 2023-01-10 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fireside", "0004_remove_taskpreset_args"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskpreset",
            name="kwargs",
            field=models.JSONField(
                blank=True, default=dict, help_text="Input kwargs for the task"
            ),
        ),
    ]
