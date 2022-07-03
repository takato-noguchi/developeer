# Generated by Django 3.0.7 on 2022-06-17 14:10

import app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to=app.models.upload_course_path)),
                ('content', models.URLField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('learning_user', models.ManyToManyField(related_name='learning_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]
