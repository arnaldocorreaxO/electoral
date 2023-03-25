from django.forms import *
from django import forms

from core.base.models import Parametro
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
===  OPERADOR    ===
==================== '''
class OperadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Operador
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Operador'}),
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
=========================
===  LOCAL VOTACION   ===
========================= '''
class LocalVotacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cod'].widget.attrs['autofocus'] = True

    class Meta:
        model = LocalVotacion
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Denominacion'}),
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
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        self.fields['tipo_voto'].queryset = TipoVoto.objects.filter(activo__exact=True)
        if usuario:
            self.fields['barrio'].queryset = Barrio.objects.filter(ciudad__distrito=usuario.distrito,activo__exact=True)
            self.fields['manzana'].queryset = Manzana.objects.filter(barrio__ciudad__distrito=usuario.distrito,activo__exact=True)
            self.fields['operador'].queryset = Operador.objects.filter(distrito=usuario.distrito,activo__exact=True)
        self.fields['ci'].widget.attrs['autofocus'] = True
    
    def set_readonly( self ):
        for field in self.fields:                
            self.fields[field].required = False
            self.fields[field].widget.attrs['disabled'] = 'disabled'
    
    class Meta:
        model = Elector
        fields = ['ci','nombre','apellido','ciudad','barrio','manzana','nro_casa','telefono',
                  'tipo_voto','local_votacion','seccional','operador']
        exclude = readonly_fields
        widgets = {
            'ci': forms.TextInput(attrs={'placeholder': 'Ingrese Cedula','readonly':'readonly'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese Nombre','readonly':'readonly'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ingrese Apellido','readonly':'readonly'}),
            'ciudad': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
            'barrio': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'manzana': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'tipo_voto': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
            'operador': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;' }),
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
    mesa = forms.ChoiceField()
    local_votacion = forms.ChoiceField()
    seccional = forms.ChoiceField()
    barrio = forms.ChoiceField()
    manzana = forms.ChoiceField()
    operador = forms.ChoiceField()
    tipo_voto = forms.ChoiceField()
    monto = forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        # print(usuario)
        super().__init__(*args, **kwargs)        
        self.fields['term'].widget.attrs['autofocus'] = True

        if usuario:
            #Mesa
            self.fields['mesa'] = forms.ChoiceField(choices=[
            (item['mesa'], item['mesa']) for item in Elector.objects.values('mesa')\
                                                                    .filter(distrito=usuario.distrito)\
                                                                    .extra(select={'int_mesa':'CAST(mesa AS INTEGER)'})\
                                                                    .distinct().order_by('int_mesa')])
            # Local de Votacion
            self.fields['local_votacion'] = forms.ChoiceField(choices=[
            (item.id, item) for item in LocalVotacion.objects.filter(ciudad__distrito=usuario.distrito,activo__exact=True)\
                                                             .order_by('id')])
            # Seccionales
            self.fields['seccional'] = forms.ChoiceField(choices=[
            (item.id, item) for item in Seccional.objects.filter(ciudad__distrito=usuario.distrito,activo__exact=True).order_by('denominacion')])
            # Barrios
            self.fields['barrio'] = forms.ChoiceField(choices=[
            (item.id, item.fullname) for item in Barrio.objects.filter(ciudad__distrito=usuario.distrito,activo__exact=True).order_by('id')])
            # Manzana
            self.fields['manzana'] = forms.ChoiceField(choices=[
            (item.id, item.fullname) for item in Manzana.objects.filter(barrio__ciudad__distrito=usuario.distrito,activo__exact=True).order_by('barrio__id','id')])
            # Operador
            self.fields['operador'] = forms.ChoiceField(choices=[
                (item.id, item) for item in Operador.objects.filter(distrito=usuario.distrito, activo__exact=True).order_by('denominacion')])
            # Tipo de Voto
            self.fields['tipo_voto'] = forms.ChoiceField(choices=[
                (item.id, item) for item in TipoVoto.objects.filter(activo__exact=True).order_by('id')])
            
            self.fields['local_votacion'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['mesa'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['seccional'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['barrio'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['manzana'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['operador'].widget.attrs.update({'class': 'form-control select2'})
            self.fields['tipo_voto'].widget.attrs.update({'class': 'form-control select2'})
    # Rango de fechas 
    date_range = forms.CharField()
    # Termino de busqueda 
    term = forms.CharField()
    
    
    # Ciudades
    ciudad = forms.ChoiceField(choices=[
    (item.id, item) for item in Ciudad.objects.filter(activo__exact=True).order_by('denominacion')])
    
    # Tipo de Voto
    tipo_voto = forms.ChoiceField(choices=[
    (item.id, item) for item in TipoVoto.objects.filter(activo__exact=True).order_by('denominacion')])
    
    # Monto Gs
    monto = forms.ChoiceField(widget=forms.RadioSelect,choices=[
    (item.valor,item.parametro) for item in Parametro.objects.filter(activo__exact=True,grupo__exact='MTO_GS_DIA_D').order_by('id')])

    

    PASOXPC_CHOICES = [
        ('','Todos'),
        ('S','YA Pasaron'),
        ('N','NO Pasaron'),
    ]
    pasoxpc = forms.ChoiceField(choices=PASOXPC_CHOICES)
    
    PASOXMV_CHOICES = [
        ('','Todos'),
        ('S','YA Votaron'),
        ('N','NO Votaron'),
    ]
    
    pasoxmv = forms.ChoiceField(choices=PASOXMV_CHOICES)

    PASOXGS_CHOICES = [
        ('','Todos'),
        ('S','YA Pasaron'),
        ('N','NO Pasaron'),
    ]
    
    pasoxgs = forms.ChoiceField(choices=PASOXGS_CHOICES)

    date_range.widget.attrs.update({'class': 'form-control','autocomplete':'off'})
    term.widget.attrs.update({'class': 'form-control','autocomplete':'off'})
    ciudad.widget.attrs.update({'class': 'form-control select2'})    
    tipo_voto.widget.attrs.update({'class': 'form-control select2'})
    pasoxmv.widget.attrs.update({'class': 'form-control select2'})
    pasoxpc.widget.attrs.update({'class': 'form-control select2'})
    # monto.widget.attrs.update({'class': 'inline'})
    
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