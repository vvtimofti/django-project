# Generated by Django 5.0.1 on 2024-04-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0027_post_reposted_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="views_count",
            field=models.IntegerField(default=0),
        ),
    ]
