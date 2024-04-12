from django import forms

from gestione.models import Libro


class ModificaLibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        exclude = ['data_prestito']
