# Generated by Django 4.2.1 on 2023-05-27 12:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Posts', '0003_remove_blockedprofile_users_blockedprofile_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 27, 14, 7, 36, 718572)),
        ),
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(max_length=200)),
                ('comment_timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.post')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
