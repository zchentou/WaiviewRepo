# Generated by Django 3.0.7 on 2020-06-17 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0017_auto_20200616_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='anonymous',
            field=models.BooleanField(),
        ),
    ]