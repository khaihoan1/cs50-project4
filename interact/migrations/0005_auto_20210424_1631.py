# Generated by Django 3.1.6 on 2021-04-24 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interact', '0004_auto_20210422_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='comment_parent',
            new_name='comment_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reply',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]