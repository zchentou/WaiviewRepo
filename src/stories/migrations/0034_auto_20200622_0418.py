# Generated by Django 3.0.7 on 2020-06-22 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0033_auto_20200622_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='tags',
            field=models.CharField(blank=True, max_length=100, verbose_name='Tags (eg., recovery, nurse, detroitprotest, collegestudent ...) (separate with commas)'),
        ),
    ]
