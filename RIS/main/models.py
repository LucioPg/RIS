from django.db import models


# Create your models here.

class CategoriaProdotto(models.Model):
    """Categorie per i prodotti"""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Prodotto(models.Model):
    """Prodotti da inventario"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoriaProdotto, on_delete=models.CASCADE)
    has_barcode = models.BooleanField(default=True)

    def __str__(self):
        return self.name
