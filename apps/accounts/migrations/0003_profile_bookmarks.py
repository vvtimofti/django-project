# Generated by Django 5.0.1 on 2024-03-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_profile_profile_picture"),
        ("posts", "0013_remove_post_bookmarked_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bookmarks",
            field=models.ManyToManyField(
                blank=True, related_name="bookmark_users", to="posts.post"
            ),
        ),
    ]
