# Generated by Django 5.0.1 on 2024-05-10 20:39

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_alter_chatroom_room_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="room_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=150, unique=True
            ),
        ),
    ]
