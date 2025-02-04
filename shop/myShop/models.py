from django.db import models

# Create your models here.
class Product(models.Model):
    titel = models.CharField(max_length=50)
    preis = models.FloatField()
    beschreibung = models.TextField()
    datum = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.titel


class ProductImage(models.Model):
    produkt = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productImages/')

    

