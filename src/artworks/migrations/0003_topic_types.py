# Generated by Django 3.0.7 on 2020-06-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0002_auto_20200620_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='types',
            field=models.ManyToManyField(to='artworks.Type'),
        ),
    ]