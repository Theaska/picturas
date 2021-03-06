# Generated by Django 2.2.4 on 2019-08-24 15:42

import blog.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_birth', models.DateField(null=True)),
                ('about', models.TextField(blank=True, max_length=500)),
                ('avatar', models.ImageField(default='default/anonymous.png', storage=blog.storage.OverwriteStorage(), upload_to=users.models.user_avatar_path)),
                ('friends', models.ManyToManyField(blank=True, to='users.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
