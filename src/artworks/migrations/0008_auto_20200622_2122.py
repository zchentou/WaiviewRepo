# Generated by Django 3.0.7 on 2020-06-22 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0007_auto_20200621_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='position',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='position',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]