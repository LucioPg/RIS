from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CategoriaProdotto, Prodotto, Inventario
from .forms import CreaCategoria, CreaProdotto, ElencoProdotti, ProdottoUpdate, CategoriaProdottoUpdate, AddItem, InventoryForm




@login_required(login_url='login')
def home(request):
    return render(request, 'main/dashboard.html')
    # return render(request, 'main/test_dashboard.html')

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
        # 'qnt': prodotto.qnt,
        # 'barcode': prodotto.barcode,
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
    # if True:
        if request.method == 'POST':
            form = CreaProdotto(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                # barcode = form.cleaned_data['barcode']
                category = form.cleaned_data['category']
                # prodotto = Prodotto(name=name, barcode=barcode, category=category)
                prodotto = Prodotto(name=name, category=category)
                if 'SalvaProdotto' in request.POST:
                    prodotto.save()
                form = CreaProdotto()
        else:
            form = CreaProdotto()
    else:
        return render(request, 'main/not_allowed.html')
    return render(request, 'main/prodotto_create.html', {'form': form})

@login_required(login_url='login')
def prodotti(request):
    if request.method == 'GET':
        cat_min_list = [cat.id for cat in CategoriaProdotto.objects.all()]
        if cat_min_list:
            categoria = min(cat_min_list)
        else:
            categoria = None
        prodotti = Prodotto.objects.filter(category=categoria)
        context = {
            'categorie': CategoriaProdotto.objects.all(),
            'categoria': categoria,
            'prodotti': prodotti,
        }
        return render(request, 'main/prodotti.html', context)



@login_required(login_url='login')
def prodotto_delete(request, id):
    instance = get_object_or_404(Prodotto, id=id)
    if instance:
        instance.delete()
        categoria = min([cat.id for cat in CategoriaProdotto.objects.all()])
        prodotti = Prodotto.objects.filter(category=categoria)
        context = {
            'categorie': CategoriaProdotto.objects.all(),
            'categoria': categoria,
            'prodotti': prodotti,
        }
        return render(request, 'main/prodotti.html', context)

@login_required(login_url='login')
def prodotto_update(request, id):
    instance = get_object_or_404(Prodotto, id=id)
    print(request)
    form = ProdottoUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(f'/prodotto/{id}')
    return render(request, 'main/prodotto_create.html', {'form': form})

@login_required(login_url='login')
def categoria_update(request, id):
    instance = get_object_or_404(CategoriaProdotto, id=id)
    print(request)
    form = CategoriaProdottoUpdate(request.POST or None, instance=instance)
    print(form)
    if form.is_valid():
        form.save()
        return redirect(f'/categoria/{id}')
    return render(request, 'main/categorie_create.html', {'form': form})

@login_required(login_url='login')
def categoria_delete(request, id):
    instance = get_object_or_404(CategoriaProdotto, id=id)
    if instance:
        instance.delete()
        # categoria = min([cat.id for cat in CategoriaProdotto.objects.all()])
        # prodotti = Prodotto.objects.filter(category=categoria)
        context = {
            'categorie': CategoriaProdotto.objects.all(),
            'categoria': categoria,
            'prodotti': prodotti,
        }
        # return render(request, 'main/categorie.html', context)
        return render(request, 'main/categorie.html')

# @login_required(login_url='login')
# def add_inv_item(request):
#     if request.user.is_superuser:
#         # if True:
#         if request.method == 'POST':
#             form = AddItem(request.POST)
#             if form.is_valid():
#                 prodotto = form.cleaned_data['prodotto']
#                 barcode = form.cleaned_data['barcode']
#                 category = form.cleaned_data['category']
#                 prodotto = Prodotto(name=name, category=category)
#                 if 'SalvaProdotto' in request.POST:
#                     prodotto.save()
#                 form = CreaProdotto()
#         else:
#             form = CreaProdotto()
#     else:
#         return render(request, 'main/not_allowed.html')
#     return render(request, 'main/prodotto_create.html', {'form': form})

class InventarioCreateView(CreateView):
    model = Inventario
    # fields = ('categoria', 'prodotto', 'barcode')
    form_class = InventoryForm
    # context_object_name = 'inventario'
    success_url = reverse_lazy('categoria_changelist')


class InventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventoryForm
    # fields = ('categoria', 'prodotto', 'barcode')
    success_url = reverse_lazy('categoria_changelist')


class InventarioListView(ListView):
    model = Inventario
    # fields = ('categoria', 'prodotto', 'barcode')
    # success_url = reverse_lazy('categoria_changelist')
    context_object_name = 'inventario'

def ajax_load_products(request):
    category_id = request.GET.get('categoria')
    products = Prodotto.objects.filter(category=category_id).order_by('name')
    return render(request, 'main/prod_dropdown_list_options.html', {'products': products})

