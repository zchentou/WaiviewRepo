# Generated by Django 3.0.7 on 2020-06-17 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20200617_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='occupation',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='default_img.jpg', upload_to='profile_imgs', verbose_name='Profile Picture'),
        ),
    ]