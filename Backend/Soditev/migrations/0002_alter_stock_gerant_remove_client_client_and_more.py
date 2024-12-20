# Generated by Django 5.1.2 on 2024-10-25 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Soditev', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='gerant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='client',
            name='client',
        ),
        migrations.RemoveField(
            model_name='technicien',
            name='technicien',
        ),
        migrations.AlterField(
            model_name='caisse',
            name='caissier',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='commerciaux',
            name='commerciaux',
        ),
        migrations.AddField(
            model_name='client',
            name='adresse',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AddField(
            model_name='client',
            name='telephone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commerciaux',
            name='adresse',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AddField(
            model_name='commerciaux',
            name='telephone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='commerciaux',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stock',
            name='adresse',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AddField(
            model_name='stock',
            name='telephone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='technicien',
            name='adresse',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AddField(
            model_name='technicien',
            name='telephone',
            field=models.CharField(default=None, max_length=15),
        ),
        migrations.AddField(
            model_name='technicien',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='caisse',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Soditev.client'),
        ),
        migrations.AlterField(
            model_name='commerciaux',
            name='commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='commerciaux',
            name='vente',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantite',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='Personne',
        ),
    ]
