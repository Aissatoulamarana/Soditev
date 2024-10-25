# Generated by Django 5.1.2 on 2024-10-23 18:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Forfait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=12)),
                ('duree', models.PositiveIntegerField(default=1, help_text="Durée de l'abonnement en mois")),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('quantite', models.IntegerField()),
                ('categorie', models.CharField(max_length=50)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=12)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('description', models.TextField(blank=True, null=True)),
                ('seuil', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.client')),
            ],
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=60)),
                ('telephone', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Commerciaux',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=12, null=True)),
                ('statut', models.CharField(choices=[('ACTIF', 'Actif'), ('NON_ACTIF', 'Non-Actif')], default='NON_ACTIF', max_length=20)),
                ('score', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)])),
                ('vente', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('commerciaux', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Soditev.personne')),
                ('produit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Soditev.product')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Soditev.personne'),
        ),
        migrations.CreateModel(
            name='Caisse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compte', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date_transaction', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Soditev.client')),
                ('commercant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Soditev.commerciaux')),
                ('caissier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Soditev.personne')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('rabais', models.DecimalField(decimal_places=2, help_text='Pourcentage de réduction (ex : 20 pour 20%)', max_digits=5)),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('acces_tous_programmes', models.BooleanField(default=False, help_text='Si activé, donne accès à tous les programmes')),
                ('forfaits_concernes', models.ManyToManyField(blank=True, to='Soditev.forfait')),
            ],
        ),
        migrations.CreateModel(
            name='Souscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ABONNEMENT', 'Abonnement'), ('REABONNEMENT', 'Réabonnement')], max_length=20)),
                ('status', models.CharField(choices=[('EN_COURS', 'En Cours'), ('ACTIF', 'Actif'), ('FINI', 'Fini')], default='EN_COURS', max_length=20)),
                ('date_debut', models.DateField(auto_now_add=True)),
                ('date_fin', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.client')),
                ('forfait', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.forfait')),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Soditev.promotion')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gerant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Soditev.personne')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Soditev.stock'),
        ),
        migrations.CreateModel(
            name='Technicien',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('statut', models.CharField(choices=[('ACTIF', 'Actif'), ('NON_ACTIF', 'Non-Actif')], default='NON_ACTIF', max_length=20)),
                ('disponibilite', models.DateField(blank=True, null=True)),
                ('technicien', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Soditev.personne')),
            ],
        ),
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('status', models.CharField(choices=[('EN_COURS', 'En Cours'), ('FAIT', 'Fait')], default='EN_COURS', max_length=20)),
                ('technicien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.technicien')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('avis', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.client')),
                ('technicien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.technicien')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('voice_message', models.FileField(blank=True, null=True, upload_to='voice_messages/')),
                ('media_file', models.FileField(blank=True, null=True, upload_to='media_files/')),
                ('is_read', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.client')),
                ('technicien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Soditev.technicien')),
            ],
        ),
    ]
