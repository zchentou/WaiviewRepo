# Generated by Django 3.0.7 on 2020-06-20 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stories', '0031_auto_20200620_0737'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='story_imgs', verbose_name='Picture')),
                ('title', models.CharField(blank=True, max_length=70, verbose_name='Optional Title for Picture')),
                ('picture_caption', models.CharField(blank=True, max_length=200, verbose_name='Optional Caption for Picture')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stories.Issue')),
                ('type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='artworks.Type')),
            ],
        ),
    ]
