from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import CategoriaProdotto, Prodotto, Inventario
from .forms import CreaCategoria, CreaProdotto, ElencoProdotti, ProdottoUpdate, CategoriaProdottoUpdate, AddItem, InventoryForm
from django.views.decorators.csrf import csrf_exempt
from proxy.views import proxy_view
import os

@csrf_exempt
def myview(request, path=None):
    if not path:
        path = 'sta'
    path = os.path.join(path,'Things')
    # extra_requests_args = {...}
    print(request.user)
    print(request.GET)
    for x in request.GET:
        print(x)
    extra_requests_args = {}
    remoteurl = 'http://192.168.43.127:8081/' + path
    return proxy_view(request, remoteurl, extra_requests_args)
    # return proxy_view(request, remoteurl, {})

# urlpatterns = patterns(
# 	...
# 	url('proxy/(?P<path>.*)', myview),
# 	...
# )




@login_required(login_url='login')
def home(request):
    return render(request, 'main/dashboard.html')
    # return render(request, 'main/test_dashboard.html')

def logout(request):
    return render(request, 'main/logout.html')

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


class BarcodeIterator:
    ''' Iterator class '''

    def __init__(self, barcodes):
        # Team object reference
        self._barcodes = barcodes
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < len(self._barcodes): # Check if junior members are fully iterated or not
            result = self._barcodes[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration

class Barcodes:
    # barcode_list = set()
    barcode_list =  {'8032089001236','8032089001237', '8032089001238'}

    def clear(self):
        self.barcode_list.clear()

    def add(self, x):
        self.barcode_list.add(x)

    def remove(self, x):
        self.barcode_list.remove(x)

    def __iter__(self):
        return BarcodeIterator(list(self.barcode_list))

@login_required(login_url='login')
def prodotto_create(request, barcode_list=Barcodes()):
    # barcode_list = {'8032089001236','8032089001237', '8032089001238'}
    barcode_list = barcode_list
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
    return render(request, 'main/prodotto_create.html', {'form': form, 'barcode_list': barcode_list})

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

class InventarioAutoAdd(CreateView):
    model = Inventario
    # fields = ('categoria', 'prodotto', 'barcode')
    form_class = InventoryForm
    template_name = 'main/inventario_auto_add.html'
    # context_object_name = 'inventario'


class InventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventoryForm
    # fields = ('categoria', 'prodotto', 'barcode')
    success_url = reverse_lazy('categoria_changelist')


class InventarioListView(ListView):
    model = Inventario
    # fields = ('categoria', 'prodotto', 'barcode')
    # success_url = reverse_lazy('categoria_changelist')
    paginate_by = 10
    queryset = Inventario.objects.all()
    context_object_name = 'inventario'
    ordering = ['data']
    q_dict = {
        'searchCat': 'categoria__name',
        'searchPro': 'prodotto__name',
        'searchBar': 'barcode',
    }
    def get_queryset(self):
        # query_cat = self.request.GET.get('searchCat')
        # query_pro = self.request.GET.get('searchPro')
        # query_bar = self.request.GET.get('searchBar')
        # if query_cat:
        #     object_list = self.model.objects.filter(categoria__name__icontains=query_cat)
        #     if object_list:
        #         return object_list
        #     else:
        #         object_list = self.model.objects.none()
        # else:
        #     object_list = self.model.objects.all()
        # return object_list
        for search in self.q_dict:
            if search in self.request.GET:
                return self.query_obj(search)
        return self.query_obj('')


    # todo da migliorare (concatenare i filtri
    def query_obj(self, obj):
        query_obj = self.request.GET.get(obj)
        if query_obj:
            fil = {f'{self.q_dict[obj]}__icontains': query_obj}
            object_list = self.model.objects.filter(**fil)
            if object_list:
                return object_list
            else:
                object_list = self.model.objects.none()
        else:
            object_list = self.model.objects.all()
        return object_list

# @login_required(login_url='login')
# def inventario_delete_item(request, id):
#     instance = get_object_or_404(Inventario, id=id)
#     if instance:
#         instance.delete()
#         # categoria = min([cat.id for cat in CategoriaProdotto.objects.all()])
#         # prodotti = Prodotto.objects.filter(category=categoria)
#         # return render(request, 'main/categorie.html', context)
#         return render(request, 'main/inventario_list.html')

class InventarioDelete(DeleteView):
    model = Inventario
    form_class = InventoryForm
    context_object_name = 'inventario'
    success_url = reverse_lazy('categoria_changelist')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def ajax_load_products(request):
    category_id = request.GET.get('categoria')
    products = Prodotto.objects.filter(category=category_id).order_by('name')
    return render(request, 'main/prod_dropdown_list_options.html', {'products': products})

def testview(request):

    return render(request, 'test/test.html')
    # return HttpResponse(test)

