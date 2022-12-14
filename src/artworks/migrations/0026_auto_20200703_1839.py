# Generated by Django 3.0.7 on 2020-07-03 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0025_auto_20200703_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='topic',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.Topic'),
        ),
        migrations.AlterField(
            model_name='link',
            name='type',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.Type', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='topic',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.Topic'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='type',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artworks.Type', verbose_name='Category'),
        ),
    ]
