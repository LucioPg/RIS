from django.shortcuts import render, HttpResponse
from .models import CategoriaProdotto, Prodotto
from .forms import CreaCategoria


def home(request):
    return render(request, 'main/dashboard.html')


def categoria(request, id):
    ls = CategoriaProdotto.objects.get(id=id)
    products = ls.prodotto_set.all()
    return render(request, 'main/categoria.html', {'categoria': ls, 'prodotti': products})


def categorie(request):
    ls = CategoriaProdotto.objects.all()
    return render(request, 'main/categorie.html', {'categorie': ls})

def categorie_create(request):
    if request.method == "POST":
        form = CreaCategoria(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            unit = form.cleaned_data["unit"]
            barcode = form.cleaned_data["barcode"]
            categoria = CategoriaProdotto(name=name, unit=unit, has_barcode=barcode)
            categoria.save()
            form = CreaCategoria()
    else:
        form = CreaCategoria()
    return render(request, 'main/categorie_create.html', {'form': form})
