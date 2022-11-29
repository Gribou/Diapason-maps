# Generated by Django 3.2.13 on 2022-04-20 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25, verbose_name='Intitulé')),
                ('slug', models.SlugField(unique=True, verbose_name='Identifiant')),
                ('depth', models.PositiveIntegerField(default=0, verbose_name='Profondeur')),
                ('metadata', models.JSONField(blank=True, null=True, verbose_name='Métadonnées')),
                ('mbtiles_file', models.FileField(blank=True, help_text='Importer un nouveau fichier pour générer de nouvelles tuiles', null=True, upload_to='import/', verbose_name='Fichier MBTiles')),
                ('show_by_default', models.BooleanField(default=False, verbose_name='Afficher par défault')),
            ],
            options={
                'verbose_name': 'Calque',
                'verbose_name_plural': 'Calques',
                'ordering': ['-depth', 'label'],
            },
        ),
    ]