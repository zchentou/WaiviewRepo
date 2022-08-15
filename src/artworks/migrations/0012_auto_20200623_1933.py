# Generated by Django 3.0.7 on 2020-06-23 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0011_link_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='video',
            field=models.FileField(blank='True', upload_to='individual_vids', verbose_name='Video'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='picture',
            field=models.ImageField(blank='True', upload_to='individual_imgs', verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='picture_caption',
            field=models.CharField(blank=True, max_length=200, verbose_name='Optional Caption for Image/Video'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(blank=True, max_length=70, verbose_name='Optional Title for Image/Video'),
        ),
    ]
