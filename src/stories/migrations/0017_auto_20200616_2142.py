# Generated by Django 3.0.7 on 2020-06-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0016_story_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='comment Anonymously'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reply',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='reply Anonymously'),
            preserve_default=False,
        ),
    ]
