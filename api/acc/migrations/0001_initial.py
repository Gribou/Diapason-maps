# Generated by Django 3.2.11 on 2022-03-03 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Antenna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nom')),
                ('latitude', models.IntegerField(default=0, verbose_name='Latitude')),
                ('longitude', models.IntegerField(default=0, verbose_name='Longitude')),
            ],
            options={
                'verbose_name': 'Antenne Radio',
                'verbose_name_plural': 'Antennes Radio',
            },
        ),
        migrations.CreateModel(
            name='ControlCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Centre de contrôle')),
                ('rank', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
            ],
            options={
                'verbose_name': 'Centre de contrôle',
                'verbose_name_plural': 'Centres de contrôle',
                'ordering': ['rank', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SectorFrequency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(max_length=7, verbose_name='Fréquence')),
                ('frequency_type', models.CharField(choices=[('V', 'VHF'), ('U', 'UHF')], max_length=3, verbose_name='Type de fréquence')),
                ('is833', models.BooleanField(default=True, verbose_name='Est 8.33kHz')),
            ],
            options={
                'verbose_name': 'Fréquence',
                'verbose_name_plural': 'Fréquences',
                'ordering': ['frequency'],
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2, verbose_name='Nom')),
                ('hidden', models.BooleanField(default=False, verbose_name='Ne pas montrer')),
                ('airac', models.DateField(verbose_name='Cycle AIRAC')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Mise à jour')),
                ('control_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sectors', to='acc.controlcenter')),
                ('frequencies', models.ManyToManyField(blank=True, default=None, related_name='sectors', to='acc.SectorFrequency')),
                ('main_antenna', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_sectors', to='acc.antenna', verbose_name='Antenne principale')),
                ('secondary_antenna', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondary_sectors', to='acc.antenna', verbose_name='Antenne secondaire')),
            ],
            options={
                'verbose_name': 'Secteur',
                'verbose_name_plural': 'Secteurs',
                'ordering': ['control_center', 'name'],
            },
        ),
    ]