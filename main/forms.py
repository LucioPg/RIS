from django import forms
from main.models import CategoriaProdotto, Prodotto

class CreaCategoria(forms.Form):
    """Form per la creazione di una nuova categoria prodotti."""
    name = forms.CharField(label='Nome', max_length=200)
    barcode = forms.BooleanField(required=False, initial=True)
    unit = forms.IntegerField(initial=1)

class CreaProdotto(forms.Form):
    """Form per la creazione di un prodotto"""
    name = forms.CharField(label='Nome', max_length=200)
    barcode = forms.CharField(label='Barcode', max_length=20)
    # ls = [categoria.name for categoria in CategoriaProdotto.objects.all()]
    # category = forms.ChoiceField(choices=ls)
    category = forms.ModelChoiceField(queryset=CategoriaProdotto.objects.all(), label='categoria', widget=forms.Select)

class ElencoProdotti(forms.Form):
    """Form per elencare i prodotti"""
    category = forms.ModelChoiceField(queryset=CategoriaProdotto.objects.all(), label='categoria', widget=forms.Select)
    # name = forms.CharField(label='Nome', max_length=200)
    # barcode = forms.CharField(label='Barcode', max_length=20)
    # qnt = forms.IntegerField(label='Quantità', initial=1)

class ProdottoUpdate(forms.ModelForm):
    class Meta:
        model = Prodotto
        fields = [
            'name',
            'barcode',
            'category'
        ]
