# Generated by Django 3.1.6 on 2021-04-25 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20210425_1648'),
        ('interact', '0005_auto_20210424_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='post_parent',
            field=models.ForeignKey(db_column='post_parent', on_delete=django.db.models.deletion.CASCADE, related_name='like', to='post.post'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'followed'), name='unique_follow'),
        ),
    ]