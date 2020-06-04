from django.db import models


# Create your models here.

class CategoriaProdotto(models.Model):
    """Categorie per i prodotti"""
    name = models.CharField(max_length=200)
    has_barcode = models.BooleanField()
    unit = models.IntegerField(default=1)
    total_prd = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# class Inventario(models.Model):
#     """Quantità dei prodotti."""


class Prodotto(models.Model):
    """Prodotti da inventario"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoriaProdotto, on_delete=models.CASCADE)
    qnt = models.IntegerField(default=0)
    barcode = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name
