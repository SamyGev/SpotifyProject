# Generated by Django 4.1.2 on 2022-12-05 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0006_user_device_user_listening'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='device',
        ),
        migrations.RemoveField(
            model_name='user',
            name='listening',
        ),
    ]