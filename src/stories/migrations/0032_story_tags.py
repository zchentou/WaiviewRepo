# Generated by Django 3.0.7 on 2020-06-21 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0031_auto_20200620_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='tags',
            field=models.CharField(default='', max_length=100, verbose_name='Tags (eg., recovery, detroitprotest ...)'),
            preserve_default=False,
        ),
    ]
