# Generated by Django 5.0.1 on 2024-03-23 23:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0009_post_is_flagged_post_parent_post"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="content",
            new_name="post_content",
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
    ]
