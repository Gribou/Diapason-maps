# Generated by Django 3.2.13 on 2022-06-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecategory',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='categories', to='files.StaticFile'),
        ),
    ]
