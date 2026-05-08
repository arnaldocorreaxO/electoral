from django.forms import *
from django import forms
from django.db.models import Q

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
    # 1. DEFINICIÓN DE CAMPOS (Sin choices fijos para evitar el congelamiento)
    mesa = forms.ChoiceField(label="Mesa")
    local_votacion = forms.ChoiceField(label="Local de Votación")
    seccional = forms.ChoiceField(label="Seccional")
    barrio = forms.ChoiceField(label="Barrio")
    manzana = forms.ChoiceField(label="Manzana")
    operador = forms.ChoiceField(label="Operador")
    tipo_voto = forms.ChoiceField(label="Tipo de Voto")
    monto = forms.ChoiceField(label="Monto Gs")
    ciudad = forms.ChoiceField(label="Ciudad")
    
    # Campos de texto y fechas
    date_range = forms.CharField(label="Rango de Fechas")
    term = forms.CharField(label="Término de Búsqueda")

    # Opciones estáticas (Estas no cambian, pueden ir aquí)
    PASO_CHOICES = [('', 'Todos'), ('S', 'YA Pasaron'), ('N', 'NO Pasaron')]
    VOTO_CHOICES = [('', 'Todos'), ('S', 'YA Votaron'), ('N', 'NO Votaron')]
    
    pasoxpc = forms.ChoiceField(choices=PASO_CHOICES, label="Paso por PC")
    pasoxmv = forms.ChoiceField(choices=VOTO_CHOICES, label="Paso por MV")
    pasoxgs = forms.ChoiceField(choices=PASO_CHOICES, label="Paso por GS")

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario para filtrar por su distrito
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        
        # Foco automático en el buscador
        self.fields['term'].widget.attrs['autofocus'] = True

        # --- 2. CARGA DINÁMICA DE OPCIONES (Se ejecuta en cada petición) ---

        # Opciones que dependen del Distrito del Usuario
        if usuario:
            distrito = usuario.distrito
            
            self.fields['mesa'].choices = [('', '---')] + [
                (item['mesa'], item['mesa']) for item in Elector.objects.values('mesa')
                .filter(distrito=distrito)
                .extra(select={'int_mesa': 'CAST(mesa AS INTEGER)'})
                .distinct().order_by('int_mesa')
            ]

            self.fields['local_votacion'].choices = [('', '---')] + [
                (item.id, str(item)) for item in LocalVotacion.objects.filter(
                    ciudad__distrito=distrito, activo=True
                ).order_by('id')
            ]

            self.fields['seccional'].choices = [('', '---')] + [
                (item.id, str(item)) for item in Seccional.objects.filter(
                    ciudad__distrito=distrito, activo=True
                ).order_by('denominacion')
            ]

            self.fields['barrio'].choices = [('', '---')] + [
                (item.id, item.fullname) for item in Barrio.objects.filter(
                    ciudad__distrito=distrito, activo=True
                ).order_by('id')
            ]

            self.fields['manzana'].choices = [('', '---')] + [
                (item.id, item.fullname) for item in Manzana.objects.filter(
                    barrio__ciudad__distrito=distrito, activo=True
                ).order_by('barrio__id', 'id')
            ]

            self.fields['operador'].choices = [('', '---')] + [
                (item.id, str(item)) for item in Operador.objects.filter(
                    distrito=distrito, activo=True
                ).order_by('denominacion')
            ]

        # Opciones Generales (Se actualizan sin reiniciar el servidor)
        self.fields['ciudad'].choices = [('', '---')] + [
            (item.id, str(item)) for item in Ciudad.objects.filter(activo=True).order_by('denominacion')
        ]

        self.fields['tipo_voto'].choices = [('', '---')] + [
            (item.id, str(item)) for item in TipoVoto.objects.filter(activo=True).order_by('id')
        ]

        self.fields['monto'].choices = [('', '---')] + [
            (item.valor, item.parametro) for item in Parametro.objects.filter(
                activo=True, grupo='MTO_GS_DIA_D'
            ).order_by('id')
        ]

        # --- 3. APLICACIÓN DE ESTILOS Y ATRIBUTOS ---
        for name, field in self.fields.items():
            if name in ['date_range', 'term']:
                field.widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control select2',
                    'style': 'width: 100%;'
                })
    
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