# Generated by Django 4.1.5 on 2023-01-24 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fireside", "0010_alter_task_fpath"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="mpath",
            field=models.CharField(
                help_text="Import path to the `BaseModel` which represents the data type of the `Event`",
                max_length=256,
                null=True,
            ),
        ),
    ]
