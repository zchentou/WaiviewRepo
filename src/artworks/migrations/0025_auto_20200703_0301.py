# Generated by Django 3.0.7 on 2020-07-03 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0024_auto_20200628_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='link_to_resource',
            field=models.URLField(max_length=1500, verbose_name='Link/URL to Resource'),
        ),
    ]