from django.forms import *
from django import forms
from .models import *
from core.base.forms import *

''' 
====================
=== DEPARTAMENTO ===
==================== '''

class DepartamentoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departamento
        fields = '__all__'
        exclude = readonly_fields
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
        self.fields['departamento'].widget.attrs['autofocus'] = True

    class Meta:
        model = Distrito
        fields = '__all__'
        exclude = readonly_fields
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
        self.fields['ciudad'].widget.attrs['autofocus'] = True

    class Meta:
        model = Seccional
        fields = '__all__'
        exclude = readonly_fields
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
        exclude = readonly_fields
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
        self.fields['pais'].widget.attrs['autofocus'] = True

    class Meta:
        model = Ciudad
        fields = '__all__'
        exclude = readonly_fields
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
        self.fields['ciudad'].widget.attrs['autofocus'] = True

    class Meta:
        model = Barrio
        fields = '__all__'
        exclude = readonly_fields
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
        self.fields['barrio'].widget.attrs['autofocus'] = True

    class Meta:
        model = Manzana
        fields = '__all__'
        exclude = readonly_fields
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
        exclude = readonly_fields
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
        self.fields['tipo_voto'].queryset = TipoVoto.objects.filter(activo__exact=True)
        self.fields['ci'].widget.attrs['autofocus'] = True
    
    def set_readonly( self ):
        for field in self.fields:                
            self.fields[field].required = False
            self.fields[field].widget.attrs['disabled'] = 'disabled'
    
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','ciudad','barrio','manzana','nro_casa','telefono',
                  'tipo_voto','local_votacion','seccional']
        exclude = readonly_fields
        widgets = {
            'ci': forms.TextInput(attrs={'placeholder': 'Ingrese Cedula','readonly':'readonly'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre','readonly':'readonly'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido','readonly':'readonly'}),
            'ciudad': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'tipo_voto': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'local_votacion': forms.Select(attrs={'class': 'form-control select2',
                                                  'style': 'width: 100%;',
                                                  'disabled':'disabled',
                                                  'selected' : 'selected'}),
            'seccional': forms.Select(attrs={'class': 'form-control select2',
                                            'style': 'width: 100%;',
                                            'disabled':'disabled',
                                            'selected' : 'selected' }),
            
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
        self.fields['tipo_voto'].queryset = TipoVoto.objects.filter(activo__exact=True)
        self.fields['barrio'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','ciudad','barrio','manzana','nro_casa','telefono',
                  'tipo_voto']
        exclude = readonly_fields
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['term'].widget.attrs['autofocus'] = True
    # Rango de fechas 
    date_range = forms.CharField()
    # Termino de busqueda 
    term = forms.CharField()
    # Local de Votacion
    local_votacion = forms.ChoiceField(choices=[
    (item.id, item.denominacion) for item in LocalVotacion.objects.all()])
    
    # Mesas
    mesa = forms.ChoiceField(choices=[
    (item['mesa'], item['mesa']) for item in Elector.objects.values('mesa')\
                                                            .extra(select={'int_mesa':'CAST(mesa AS INTEGER)'})\
                                                            .distinct().order_by('int_mesa')])
    # Ciudades
    ciudad = forms.ChoiceField(choices=[
    (item.id, item.denominacion) for item in Ciudad.objects.all().order_by('denominacion')])
    # Seccionales
    seccional = forms.ChoiceField(choices=[
    (item.id, item.denominacion) for item in Seccional.objects.all().order_by('denominacion')])
    # Barrios
    barrio = forms.ChoiceField(choices=[
    (item.id, item.denominacion) for item in Barrio.objects.all().order_by('denominacion')])
    # Ciudades
    manzana = forms.ChoiceField(choices=[
    (item.id, item.fullname) for item in Manzana.objects.all().order_by('denominacion')])

    date_range.widget.attrs.update({'class': 'form-control','autocomplete':'off'})
    term.widget.attrs.update({'class': 'form-control','autocomplete':'off'})
    local_votacion.widget.attrs.update({'class': 'form-control select2'})
    mesa.widget.attrs.update({'class': 'form-control select2'})
    ciudad.widget.attrs.update({'class': 'form-control select2'})
    seccional.widget.attrs.update({'class': 'form-control select2'})
    barrio.widget.attrs.update({'class': 'form-control select2'})
    manzana.widget.attrs.update({'class': 'form-control select2'})
    
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
        exclude = readonly_fields
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