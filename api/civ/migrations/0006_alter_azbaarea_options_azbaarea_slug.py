# Generated by Django 4.1.2 on 2022-11-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('civ', '0005_azbaarea_boundaries_azbaarea_ceiling_azbaarea_floor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='azbaarea',
            options={'ordering': ['-airac', 'label'], 'verbose_name': 'Zone réglementée', 'verbose_name_plural': 'Zones réglementées'},
        ),
        migrations.AddField(
            model_name='azbaarea',
            name='slug',
            field=models.CharField(default='?', max_length=25, verbose_name='Identifiant'),
            preserve_default=False,
        ),
    ]
