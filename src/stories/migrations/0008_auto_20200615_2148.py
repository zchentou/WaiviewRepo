# Generated by Django 3.0.7 on 2020-06-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0007_story_category_to_write_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='name',
            field=models.CharField(default='Example', max_length=50),
        ),
    ]
