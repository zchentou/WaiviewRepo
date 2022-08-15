# Generated by Django 3.0.7 on 2020-06-14 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_delete_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='issue',
            field=models.TextField(choices=[('COVID', 'COVID-19'), ('BLM', 'BlackLivesMatter')], default='COVID'),
        ),
    ]