from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    titel = models.CharField(max_length=50)
    preis = models.FloatField()
    breite = models.FloatField()
    höhe = models.FloatField()
    farbe = models.CharField(max_length=30)
    material = models.CharField(max_length=30)
    beschreibung = models.TextField()
    datum = models.DateField(auto_now=False, auto_now_add=True)
    ist_verkauft = models.BooleanField(default=False)

    def __str__(self):
        return self.titel
    
    


class ProductImage(models.Model):
    produkt = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages/')

class HeaderGallery(models.Model):
    image = models.ImageField(upload_to='headerImages/')
    beschreibung = models.TextField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vorname = models.CharField(max_length=50, default="")
    nachname = models.CharField(max_length=50, default="")
    adresse = models.CharField(max_length=50, default="")
    plz = models.IntegerField(default=0)
    ort = models.CharField(max_length=50)
    agb = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Orders(models.Model):
    invoice = models.CharField(max_length=70)
    produkt = models.ManyToManyField(Product) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    betrag = models.CharField(max_length=50)
    status = models.CharField(max_length=25)
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} hat eine Bestellung bezahlt! Bestellungsnr: {self.invoice}"