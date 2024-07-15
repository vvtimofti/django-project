# Generated by Django 5.0.1 on 2024-04-09 21:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_profile_following_delete_followers"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="following",
            field=models.ManyToManyField(
                blank=True, related_name="followers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
