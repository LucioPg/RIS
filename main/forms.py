from django import forms

class CreaCategoria(forms.Form):
    """Form per la creazione di una nuova categoria prodotti."""
    name = forms.CharField(label='Nome', max_length=200)
    barcode = forms.BooleanField(required=False, initial=True)
    unit = forms.IntegerField(initial=1)
