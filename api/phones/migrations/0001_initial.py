# Generated by Django 3.2.11 on 2022-03-05 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelephoneCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nom')),
                ('rank', models.IntegerField(default=0, verbose_name='Rang')),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['rank', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Telephone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nom')),
                ('telephone_number', models.CharField(max_length=7, verbose_name='Numéro abrégé')),
                ('isExterior', models.BooleanField(default=True, verbose_name='Numéro extérieur')),
                ('isCDS', models.BooleanField(blank=True, default=True, null=True, verbose_name='Montrer CDS')),
                ('isW', models.BooleanField(blank=True, default=True, null=True, verbose_name='Montrer Zone Ouest')),
                ('isE', models.BooleanField(blank=True, default=True, null=True, verbose_name='Montrer Zone Est')),
                ('alias', models.CharField(blank=True, default=None, max_length=256, null=True, verbose_name='Alias')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Mise à jour')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telephones', related_query_name='telephone', to='phones.telephonecategory')),
            ],
            options={
                'verbose_name': 'Téléphone',
                'verbose_name_plural': 'Téléphones',
                'ordering': ['category', 'name', 'telephone_number'],
            },
        ),
    ]
