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
===    PAIS    ===
==================== '''
class PaisForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Pais
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
===  TIPO VOTO   ===
==================== '''
class TipoVotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cod'].widget.attrs['autofocus'] = True

    class Meta:
        model = TipoVoto
        fields = '__all__'
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una TipoVoto'}),
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
        self.fields['tipo_voto'].queryset = TipoVoto.objects.filter(estado__exact=True)
        self.fields['ci'].widget.attrs['autofocus'] = True
    
    def set_readonly( self ):
        for field in self.fields:                
            self.fields[field].required = False
            self.fields[field].widget.attrs['disabled'] = 'disabled'
    
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','ciudad','barrio','manzana','nro_casa','telefono',
                  'tipo_voto']

        widgets = {
            'ci': forms.TextInput(attrs={'placeholder': 'Ingrese Cedula','readonly':'readonly'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre','readonly':'readonly'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido','readonly':'readonly'}),
            'ciudad': forms.Select(attrs={'class': 'form-control select2',}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', }),
            'tipo_voto': forms.Select(attrs={'class': 'form-control select2', }),
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
        self.fields['tipo_voto'].queryset = TipoVoto.objects.filter(estado__exact=True)
        self.fields['barrio'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','ciudad','barrio','manzana','nro_casa','telefono',
                  'tipo_voto']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido'}),
            'ciudad': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'manzana': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
            'tipo_voto': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 250px;'}),
        }
    
''' 
====================
===   SHEARCH    ===
==================== '''
class ShearchForm(forms.Form):
    term = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))


''' 
====================
=== CARGA DIA D  ===
==================== '''
class CargaDiaDForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.set_readonly()
    
    def set_readonly( self ):
        for field in self.fields:                
            self.fields[field].required = False
            self.fields[field].widget.attrs['readonly'] = 'readonly'
        
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','pasoxmv','pasoxpc']
        # widgets = {
        #     'ci': forms.TextInput(attrs={'placeholder': 'Ingrese Cedula','readonly':'readonly'}),
        #     'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre','readonly':'readonly'}),
        #     'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido','readonly':'readonly'}),
        #     'ciudad': forms.Select(attrs={'class': 'form-control select2',}),
        #     'barrio': forms.Select(attrs={'class': 'form-control select2', }),
        #     'manzana': forms.Select(attrs={'class': 'form-control select2', }),
        #     'tipo_voto': forms.Select(attrs={'class': 'form-control select2', }),
        # }

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