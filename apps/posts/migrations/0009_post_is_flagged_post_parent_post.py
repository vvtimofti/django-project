# Generated by Django 5.0.1 on 2024-03-21 23:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0008_alter_comment_post_key"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_flagged",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="post",
            name="parent_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replies",
                to="posts.post",
            ),
        ),
    ]
