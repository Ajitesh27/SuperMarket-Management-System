# Generated by Django 2.2.2 on 2019-07-18 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deleted',
        ),
    ]
