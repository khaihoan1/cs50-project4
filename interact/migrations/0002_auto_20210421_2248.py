# Generated by Django 3.1.6 on 2021-04-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interact', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='user',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='reply',
            name='timestamp',
            field=models.TimeField(auto_now=True),
        ),
    ]
