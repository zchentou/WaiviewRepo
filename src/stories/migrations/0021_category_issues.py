# Generated by Django 3.0.7 on 2020-06-19 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0020_category_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='issues',
            field=models.ManyToManyField(to='stories.Issue'),
        ),
    ]
