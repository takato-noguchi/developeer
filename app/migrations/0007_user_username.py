# Generated by Django 2.2 on 2022-06-30 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_course_postuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=50),
        ),
    ]
