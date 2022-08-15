# Generated by Django 3.0.7 on 2020-06-20 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0028_remove_story_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='picture',
            field=models.ImageField(blank=True, upload_to='story_imgs', verbose_name='Optional Picture'),
        ),
    ]