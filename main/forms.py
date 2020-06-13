from django import forms
from main.models import CategoriaProdotto, Prodotto, Inventario
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Reset


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

            Submit('submit', 'Salva'),
            Reset('submit', 'Reset')
        )


class CreaProdotto(forms.Form):
    """Form per la creazione di un prodotto"""
    name = forms.CharField(label='Nome', max_length=200)
    # barcode_list = ['aaaa','fffff']
    # barcode = forms.CharField(label='Barcode', max_length=20)
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
            # 'barcode',
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


class AddItem(forms.Form):
    """ Aggiunge un item all'inventario"""

#     category = forms.ModelChoiceField(queryset=CategoriaProdotto.objects.all(), label='categoria', widget=forms.Select)
#     prodotto = forms.ModelChoiceField(queryset=Prodotto.objects.filter(category=category), label='prodotto', widget=forms.Select)
#     barcode = forms.CharField(max_length=20)

class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventario
        # fields = ('categoria', 'prodotto', 'barcode')
        fields = ('categoria', 'prodotto', 'barcode', 'id')

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        # self.barcode_list = set()
        self.fields['prodotto'].queryset = Prodotto.objects.none()
        # self.fields['barcode'].widget = forms.HiddenInput() # il campo barcode è stato reso invisibile
        # self.fields['id'].widget = forms.HiddenInput() # il campo id è stato reso invisibile
        if 'categoria' in self.data:
            try:
                category_id = int(self.data.get('categoria'))
                self.fields['prodotto'].queryset = Prodotto.objects.filter(category=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['prodotto'].queryset = self.instance.categoria.prodotto_set.order_by('name')