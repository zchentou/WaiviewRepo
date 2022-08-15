# Generated by Django 3.0.7 on 2020-06-18 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0019_auto_20200617_1654'),
        ('pages', '0003_auto_20200618_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='story',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stories.Story'),
        ),
    ]
