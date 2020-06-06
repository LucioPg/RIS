from django import forms
from main.models import CategoriaProdotto, Prodotto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field


class CustomCheckbox(Field):
    template = 'main/custom_checkbox.html'

class CreaCategoria(forms.Form):
    """Form per la creazione di una nuova categoria prodotti."""
    name = forms.CharField(label='Nome', max_length=200)
    barcode = forms.BooleanField(required=False, initial=True)
    unit = forms.IntegerField(initial=1, label='Unità')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            'name',
            CustomCheckbox('barcode'),
            'unit',
        )


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

class CategoriaProdottoUpdate(forms.ModelForm):
    class Meta:
        model = CategoriaProdotto
        fields = [
            'name',
            'has_barcode',
            'unit'
        ]
        labels = {
            'name': 'Nome',
            'has_barcode': 'Barcode',
            'unit': 'Unità'
        }
