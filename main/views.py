from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CategoriaProdotto, Prodotto
from .forms import CreaCategoria, CreaProdotto, ElencoProdotti, ProdottoUpdate




@login_required(login_url='login')
def home(request):
    return render(request, 'main/dashboard.html')

@login_required(login_url='login')
def categoria(request, id):
    ls = CategoriaProdotto.objects.get(id=id)
    products = ls.prodotto_set.all()
    return render(request, 'main/categoria.html', {'categoria': ls, 'prodotti': products})

@login_required(login_url='login')
def prodotto(request, id):
    prodotto = Prodotto.objects.get(id=id)
    context = {
        'id': id,
        'categoria': prodotto.category,
        'nome': prodotto.name,
        'qnt': prodotto.qnt,
        'barcode': prodotto.barcode,
        }
    return render(request, 'main/prodotto.html', context)

@login_required(login_url='login')
def categorie(request):

    ls = CategoriaProdotto.objects.all()
    return render(request, 'main/categorie.html', {'categorie': ls})

@login_required(login_url='login')
def categorie_create(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = CreaCategoria(request.POST)
            print(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                unit = form.cleaned_data["unit"]
                barcode = form.cleaned_data["barcode"]
                categoria = CategoriaProdotto(name=name, unit=unit, has_barcode=barcode)
                categoria.save()
                form = CreaCategoria()
        else:
            form = CreaCategoria()
    else:
        return render(request, 'main/not_allowed.html')
    return render(request, 'main/categorie_create.html', {'form': form})

@login_required(login_url='login')
def prodotto_create(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CreaProdotto(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                barcode = form.cleaned_data['barcode']
                qnt = form.cleaned_data['qnt']
                category = form.cleaned_data['category']
                prodotto = Prodotto(name=name, barcode=barcode, qnt=qnt, category=category)
                if 'SalvaProdotto' in request.POST:
                    prodotto.save()
                form = CreaProdotto()
        else:
            form = CreaProdotto()
    else:
        return render(request, 'main/not_allowed.html')
    return render(request, 'main/prodotto_create.html', {'form': form})

def prodotti(request):
    if request.method == 'GET':
        categoria = min([cat.id for cat in CategoriaProdotto.objects.all()])
        prodotti = Prodotto.objects.filter(category=categoria)
        context = {
            'categorie': CategoriaProdotto.objects.all(),
            'categoria': categoria,
            'prodotti': prodotti,
        }
        return render(request, 'main/prodotti.html', context)
    # else:
    #     form = ElencoProdotti(request.POST)
    #     if form.is_valid():
    #         categoria = form.cleaned_data['categoria']
    #         prodotti = Prodotto.objects.filter(category=categoria)
    #         context = {
    #             'categorie': CategoriaProdotto.objects.all(),
    #             'categoria': categoria,
    #             'prodotti': prodotti,
    #         }
    #         return render(request, 'main/prodotti.html', context)



def prodotto_update(request, id):
    instance = get_object_or_404(Prodotto, id=id)
    form = ProdottoUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(f'/prodotto/{id}')
    return render(request, 'main/prodotto_create.html', {'form': form})