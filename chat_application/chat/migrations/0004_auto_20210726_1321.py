# Generated by Django 3.2.5 on 2021-07-26 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_alter_roommodel_room_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagemodel',
            name='user_name',
        ),
        migrations.AddField(
            model_name='messagemodel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
