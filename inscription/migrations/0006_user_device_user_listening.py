# Generated by Django 4.1.2 on 2022-12-05 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0005_alter_user_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='listening',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]