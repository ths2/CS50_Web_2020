# Generated by Django 3.1 on 2021-10-14 13:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20211014_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
