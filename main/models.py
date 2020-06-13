from django.db import models
from datetime import datetime


# Create your models here.

class Inventario(models.Model):
    """Inventario generale"""
    prodotto = models.ForeignKey('Prodotto', on_delete=models.CASCADE)
    categoria = models.ForeignKey('CategoriaProdotto', on_delete=models.CASCADE)
    is_alive = models.BooleanField(default=True)
    barcode = models.CharField(max_length=20, default='', blank=True)
    data = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.categoria.has_barcode:
            print('@@@@@@@@@@@@@@@@@@@ barcode available')
            save_multiple(self.categoria, self.prodotto)
        return super(Inventario, self).save(*args, **kwargs)

# class Barcode(models.Model):
#     """modello barcode"""
#     inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
def save_multiple(categoria, prodotto):
    with open('/home/lucio/PycharmProjects/RIS/main/static/barcode.csv', 'r') as barcode_file:
        for line in barcode_file:
            new = Inventario(prodotto=prodotto, categoria=categoria, barcode=line)
            new.save()


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
    # barcode = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name
