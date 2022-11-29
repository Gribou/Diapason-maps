# Generated by Django 3.2.13 on 2022-04-22 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shortcut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='Intitulé')),
                ('category', models.CharField(choices=[('AIRFIELD', 'Aérodrome'), ('MAP', 'Carte'), ('SECTOR', 'Secteur'), ('PHONE', 'Téléphone'), ('RADIO', 'Radio'), ('FILE', 'Fichier'), ('AZBA', 'AZBA'), ('HOME', 'Accueil'), ('SCHEDULE', 'Horaires')], max_length=100, verbose_name='Catégorie')),
                ('url', models.CharField(help_text='ex : /map', max_length=250, verbose_name='Chemin')),
            ],
            options={
                'verbose_name': 'Raccourci',
                'verbose_name_plural': 'Raccourcis',
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='ToolbarItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('shortcut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nav.shortcut')),
            ],
            options={
                'verbose_name': "Elément de la barre d'outils",
                'verbose_name_plural': "Barre d'outils",
            },
        ),
        migrations.CreateModel(
            name='HomePageItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('shortcut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nav.shortcut')),
            ],
            options={
                'verbose_name': "Elément de la page d'accueil",
                'verbose_name_plural': "Page d'accueil",
            },
        ),
    ]