from django.db import models
from datetime import datetime


# Create your models here.

class Inventario(models.Model):
    """Inventario generale"""
    prodotto = models.ForeignKey('Prodotto', on_delete=models.CASCADE)
    categoria = models.ForeignKey('CategoriaProdotto', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)

class CategoriaProdotto(models.Model):
    """Categorie per i prodotti"""
    name = models.CharField(max_length=200)
    has_barcode = models.BooleanField()
    unit = models.IntegerField(default=1)
    # total_prd = models.IntegerField(default=0)
    #
    # def clean(self):
    #     self.total_prd = self.prds.objects.all()

    def __str__(self):
        return self.name

# class Inventario(models.Model):
#     """Quantità dei prodotti."""


class Prodotto(models.Model):
    """Prodotti da inventario"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoriaProdotto, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name
