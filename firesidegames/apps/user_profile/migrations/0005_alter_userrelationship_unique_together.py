# Generated by Django 3.2.6 on 2022-01-01 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_profile", "0004_alter_userrelationship_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="userrelationship",
            unique_together={("user_profile", "other_profile", "relationship_type")},
        ),
    ]
