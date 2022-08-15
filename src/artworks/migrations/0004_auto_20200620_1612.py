# Generated by Django 3.0.7 on 2020-06-20 16:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0003_topic_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='post Anonymously'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]