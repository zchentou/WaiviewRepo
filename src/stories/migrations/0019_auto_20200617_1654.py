# Generated by Django 3.0.7 on 2020-06-17 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0018_auto_20200617_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='anonymous',
            field=models.BooleanField(),
        ),
    ]
