# Generated by Django 3.0.7 on 2020-06-23 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0014_auto_20200623_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='media_type',
        ),
    ]