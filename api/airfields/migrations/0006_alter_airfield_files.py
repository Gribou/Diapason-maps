# Generated by Django 3.2.13 on 2022-06-06 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_alter_filecategory_files'),
        ('airfields', '0005_auto_20220424_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airfield',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='airfields', to='files.StaticFile'),
        ),
    ]
