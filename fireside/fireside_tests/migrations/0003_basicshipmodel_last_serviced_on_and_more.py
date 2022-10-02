# Generated by Django 4.0.5 on 2022-10-02 05:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("fireside_tests", "0002_basicshipmodel_activate_on_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="basicshipmodel",
            name="last_serviced_on",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="basicshipmodel",
            name="activate_on",
            field=models.DateTimeField(
                blank=True,
                help_text="When to activate model (If None, model is considered activate as long as `now` < `deactivate_on`)",
                null=True,
            ),
        ),
    ]
