from django.db import models


# Create your models here.

class CategoriaProdotto(models.Model):
    """Categorie per i prodotti"""
    name = models.CharField(max_length=200)
    has_barcode = models.BooleanField()
    unit = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Prodotto(models.Model):
    """Prodotti da inventario"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoriaProdotto, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
