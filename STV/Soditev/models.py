
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
from django.utils import timezone


# Modèle pour les personnes (Clients et Gérant)
class Personne(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=60)
    telephone = models.CharField(max_length=15)

# Modèle Stock géré par une personne
class Stock(models.Model):
    gerant = models.OneToOneField(Personne, on_delete=models.CASCADE)

    def __str__(self):
        return f"Stock géré par {self.gerant.user.username}"

# Modèle Product pour les produits en stock
class Product(models.Model):
    nom = models.CharField(max_length=50)
    quantite = models.IntegerField()  # Corrigé de 'quantité'
    categorie = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.ImageField(upload_to='products/', blank=True, null=True)  # Correction de 'ImageField'
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    seuil = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"Produit: {self.nom} - Quantité: {self.quantite} - Seuil: {self.seuil}"

    def verifier_seuil(self):
        """Vérifie si la quantité actuelle est inférieure au seuil."""
        return self.quantite < self.seuil

    def ajouter_stock(self, quantite):
        """Ajoute de la quantité au stock."""
        self.quantite += quantite
        self.save()

    def retirer_stock(self, quantite):
        """Retire de la quantité du stock."""
        if quantite <= self.quantite:
            self.quantite -= quantite
            self.save()
        else:
            raise ValueError("Quantité insuffisante en stock")

# Modèle Commerciaux
class Commerciaux(models.Model):
    STATUT = [
        ('ACTIF', 'Actif'),
        ('NON_ACTIF', 'Non-Actif')
    ]
    commerciaux = models.OneToOneField(Personne, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    commission = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True)
    statut = models.CharField(max_length=20, choices=STATUT, default='NON_ACTIF')
    score = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    vente = models.PositiveIntegerField()  # Quantité vendue
    produit = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Commerciaux: {self.commerciaux.user.username} - Statut: {self.statut}"


# Modèle des forfaits, géré par l'administrateur
class Forfait(models.Model):
    nom = models.CharField(max_length=50, unique=True)  # Nom du forfait
    prix = models.DecimalField(max_digits=12, decimal_places=2)  # Prix du forfait
    duree = models.PositiveIntegerField(default=1, help_text="Durée de l'abonnement en mois")  # Durée en mois

    def __str__(self):
        return f"{self.nom} - {self.prix} € pour {self.duree} mois"


# Modèle pour les promotions améliorées
class Promotion(models.Model):
    nom = models.CharField(max_length=50)
    rabais = models.DecimalField(max_digits=5, decimal_places=2, help_text="Pourcentage de réduction (ex : 20 pour 20%)")
    date_debut = models.DateField()
    date_fin = models.DateField()
    forfaits_concernes = models.ManyToManyField(Forfait, blank=True)  # Les forfaits concernés par cette promo
    acces_tous_programmes = models.BooleanField(default=False, help_text="Si activé, donne accès à tous les programmes")  # Accès à tous les programmes

    def est_active(self):
        """Vérifie si la promotion est active à la date actuelle."""
        today = timezone.now().date()
        return self.date_debut <= today <= self.date_fin

    def __str__(self):
        return f"Promotion {self.nom} - {self.rabais}% du {self.date_debut} au {self.date_fin}"


# Modèle Client
class Client(models.Model):
    client = models.OneToOneField(Personne, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.user.username

# Modèle pour les souscriptions
class Souscription(models.Model):
    TYPE = [
        ('ABONNEMENT', 'Abonnement'),
        ('REABONNEMENT', 'Réabonnement')
    ]

    STATUS = [
        ('EN_COURS', 'En Cours'),
        ('ACTIF', 'Actif'),
        ('FINI', 'Fini'),
    ]

    type = models.CharField(max_length=20, choices=TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default='EN_COURS')
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(blank=True, null=True)  # Calculée automatiquement
    forfait = models.ForeignKey(Forfait, on_delete=models.CASCADE)  # Choix du forfait
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, blank=True, null=True)  # Option promotionnelle

    def __str__(self):
        return f"Souscription {self.type} pour {self.client} - Forfait: {self.forfait.nom}"

    def calculer_prix_final(self):
        """Calcule le prix final en tenant compte des promotions, le cas échéant."""
        prix_final = self.forfait.prix
        if self.promotion and self.promotion.est_active():
            rabais = (self.promotion.rabais / 100) * prix_final
            prix_final -= rabais
        return prix_final

    def calculer_date_fin(self):
        """Calcule la date de fin en fonction de la durée du forfait."""
        return self.date_debut + timedelta(days=30 * self.forfait.duree)

    def save(self, *args, **kwargs):
        # Calculer la date de fin avant de sauvegarder
        if not self.date_fin:
            self.date_fin = self.calculer_date_fin()
        super().save(*args, **kwargs)



# Modèle Caisse
class Caisse(models.Model):
    caissier = models.OneToOneField(Personne, on_delete=models.CASCADE)
    compte = models.DecimalField(max_digits=12, decimal_places=2)
    commercant = models.ForeignKey(Commerciaux, on_delete=models.SET_NULL, blank=True, null=True)
    date_transaction = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Transaction par {self.caissier.user.username} - Compte: {self.compte}"


# Modèle Notification
class Notification(models.Model):
    titre = models.CharField(max_length=20)
    message = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

# Modèle Technicien
class Technicien(models.Model):
    STATUT = [
        ('ACTIF', 'Actif'),
        ('NON_ACTIF', 'Non-Actif')
    ]
    technicien = models.OneToOneField(Personne, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT, default='NON_ACTIF')
    disponibilite = models.DateField(blank= True , null= True)

    def __str__(self):
        return f"Technicien: {self.technicien.user.username} - Statut: {self.statut}"

# Modèle Tache
class Tache(models.Model):
    STATUS = [
        ('EN_COURS', 'En Cours'),
        ('FAIT', 'Fait')
    ]
    libelle = models.CharField(max_length=50)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='EN_COURS')
    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tâche: {self.libelle} - Statut: {self.status}"

# Modèle Commentaire
class Commentaire(models.Model):
    note = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
    avis = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire de {self.client.user.username} - Note: {self.note}"

# Modèle Chat
class Chat(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    voice_message = models.FileField(upload_to='voice_messages/', blank=True, null=True)
    media_file = models.FileField(upload_to='media_files/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chat entre {self.client.user.username} et {self.technicien.user.username}"