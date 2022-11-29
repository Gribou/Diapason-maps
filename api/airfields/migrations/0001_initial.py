# Generated by Django 3.2.11 on 2022-03-02 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airfield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nom')),
                ('icao_code', models.CharField(max_length=4, unique=True, verbose_name='Code OACI')),
                ('latitude', models.IntegerField(default=0, verbose_name='Latitude')),
                ('longitude', models.IntegerField(default=0, verbose_name='Longitude')),
                ('elevation', models.IntegerField(default=0, verbose_name='Altitude ft')),
                ('category', models.CharField(default=0, max_length=100)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Mise à jour')),
            ],
            options={
                'verbose_name': 'Aérodrome',
                'verbose_name_plural': 'Aérodromes',
                'ordering': ['icao_code', 'name'],
            },
        ),
        migrations.CreateModel(
            name='AirfieldMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airac', models.DateField(verbose_name='Cycle AIRAC')),
                ('name', models.CharField(max_length=250, verbose_name='Nom')),
                ('pdf', models.FileField(blank=True, max_length=251, upload_to='', verbose_name='PDF')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Mise à jour')),
                ('airfield', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='airfields.airfield')),
            ],
            options={
                'verbose_name': 'Carte',
                'verbose_name_plural': 'Cartes',
                'ordering': ['-airac', 'airfield__icao_code', 'name'],
                'unique_together': {('name', 'airfield')},
            },
        ),
    ]