# Generated by Django 2.2 on 2022-07-29 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0025_auto_20220729_2217'),
        ('chat', '0002_remove_room_userroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Plan')),
                ('userRoom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]