# Generated by Django 3.0.7 on 2020-06-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0035_auto_20200622_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='issue',
            name='position',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]