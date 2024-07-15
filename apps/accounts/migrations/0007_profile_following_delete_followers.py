# Generated by Django 5.0.1 on 2024-04-09 21:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_profile_bio_alter_profile_display_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="following",
            field=models.ManyToManyField(
                blank=True, related_name="followers", to="accounts.profile"
            ),
        ),
        migrations.DeleteModel(
            name="Followers",
        ),
    ]
