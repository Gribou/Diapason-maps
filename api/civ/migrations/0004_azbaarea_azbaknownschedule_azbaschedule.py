# Generated by Django 4.1.2 on 2022-11-04 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('civ', '0003_delete_azbamap'),
    ]

    operations = [
        migrations.CreateModel(
            name='AzbaArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25, verbose_name='Intitulé')),
                ('airac', models.DateField(verbose_name='Cycle AIRAC')),
            ],
            options={
                'verbose_name': 'Zone RTBA',
                'verbose_name_plural': 'Zones RTBA',
                'ordering': ['-airac', 'label'],
            },
        ),
        migrations.CreateModel(
            name='AzbaKnownSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_to', models.DateTimeField()),
            ],
            options={
                'ordering': ['-up_to'],
            },
        ),
        migrations.CreateModel(
            name='AzbaSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_time', models.DateTimeField(verbose_name="Début d'activité")),
                ('deactivation_time', models.DateTimeField(verbose_name="Fin d'activité")),
                ('azba', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='civ.azbaarea')),
            ],
            options={
                'verbose_name': 'Activité AZBA',
                'verbose_name_plural': 'Planification AZBA',
                'ordering': ['activation_time', '-deactivation_time'],
            },
        ),
    ]