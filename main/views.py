from django.shortcuts import render, HttpResponse
from .models import CategoriaProdotto, Prodotto


def home(request):
    return render(request, 'main/dashboard.html')


def categoria(request, id):
    ls = CategoriaProdotto.objects.get(id=id)
    products = ls.prodotto_set.all()
    return render(request, 'main/categoria.html', {'categoria': ls, 'prodotti': products})


def categorie(request):
    ls = CategoriaProdotto.objects.all()
    return render(request, 'main/categorie.html', {'categorie': ls})
