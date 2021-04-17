from django.forms import *
from django import forms
from .models import *

''' 
====================
=== DEPARTAMENTO ===
==================== '''

class DepartamentoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departamento
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Departamento'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===   DISTRITO   ===
==================== '''
class DistritoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod'].widget.attrs['autofocus'] = True

    class Meta:
        model = Distrito
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Distrito'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===   SECCIONAL  ===
==================== '''
class SeccionalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod'].widget.attrs['autofocus'] = True

    class Meta:
        model = Seccional
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Seccional'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===    CIUDAD    ===
==================== '''
class CiudadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ciudad
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Ciudad'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===    BARRIO    ===
==================== '''
class BarrioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Barrio
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Barrio'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
''' 
====================
===    MANZANA   ===
==================== '''
class ManzanaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Manzana
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Manzana'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' 
====================
===   ELECTOR    ===
==================== '''
class ElectorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs['autofocus'] = True

    class Meta:
        model = Elector
        fields = '__all__'

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido'}),
            'departamento': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'distrito': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'seccional': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'manzana': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
''' 
====================
===   ELECTOR2    ===
==================== '''
class ElectorForm2(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barrio'].widget.attrs['autofocus'] = True

    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','barrio','manzana','nro_casa','telefono',]
        
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido'}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'manzana': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            # 'barrio': apply_select2(forms.Select),
            # 'manzana': apply_select2(forms.Select),
        }

