from django.contrib.admin.options import ModelAdmin
from django.db.models.base import Model
from core.electoral.forms import *
from core.electoral.models import Elector, Padgral
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Elector
from core.base.models import *
# ElectorForm = select2_modelform(Elector, attrs={'width': '250px'})

''' 
====================
===   ELECTOR    ===
==================== '''
class ElectorResource(resources.ModelResource):
    class Meta:
        model = Elector        

class ElectorAdmin(ImportExportModelAdmin):
    # form = ElectorForm
    resource_class = ElectorResource
    list_per_page = 25
    search_fields =['ci','nombre','apellido']
    list_filter =['ciudad','seccional','barrio','manzana','tipo_voto']
    
    '''Filtrar solo los tipos de votos activos'''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tipo_voto':
            kwargs["queryset"] = TipoVoto.objects.filter(activo__exact=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

''' 
====================
===   PADGRAL    ===
==================== '''
class PadGralResource(resources.ModelResource):
    class Meta:
        model = Padgral

class PadGralAdmin(ImportExportModelAdmin):
    resource_class = PadGralResource


# @admin.register(Elector2)
''' 
====================
===   ELECTOR2    ===
==================== '''
#Registrar el mismo modelo varias veces hay que hacer un proxy
class Elector2(Elector):    
    class Meta:
        verbose_name = 'Electores Barrio Manzana'
        verbose_name_plural = 'Electores Barrios Manzanas'
        proxy = True

class ElectorResources2(resources.ModelResource):
    class Meta:
        model = Elector2
        fields = ('ci', 'nombre', 'apellido','telefono','barrio','manzana','nro_casa',)


class ElectorAdmin2(ImportExportModelAdmin):
    resource_class = ElectorResources2  
    form = ElectorForm2 
    readonly_fields = ('ci','nombre','apellido','edad')   
    list_display =['ci','nombre','apellido','edad','telefono','get_cod_tipo_voto','manzana','nro_casa']
    # list_editable =['telefono','barrio','manzana','nro_casa'] #Consume muchos recursos (tarda mucho la consulta)
    list_filter =['ciudad','seccional','mesa','barrio','manzana','tipo_voto']
    search_fields =['ci','nombre','apellido']
    list_display_links = ['ci','nombre','apellido']
    list_per_page = 25
    # ordering = ['seccional','-barrio','manzana','nro_casa']

   
    def edad(self,obj):
        return obj.get_edad()
    edad.short_description = 'Edad'
    edad.admin_order_field = 'edad'
    
    
    def get_cod_tipo_voto(self,obj):
        return obj.tipo_voto.cod if obj.tipo_voto else None
    get_cod_tipo_voto.short_description = 'Tipo Voto'

    '''Filtrar solo los tipos de votos activos'''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tipo_voto':
            kwargs["queryset"] = TipoVoto.objects.filter(activo__exact=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


''' 
====================
===   ELECTOR3   ===
==================== '''
class Elector3(Elector):
    class Meta:
        verbose_name = 'Electores Preferencia de Votos y Nro Casa'
        verbose_name_plural = 'Electores Preferencia de Votos y Nro Casa'
        proxy = True

class ElectorResources3(resources.ModelResource):
    class Meta:
        model = Elector3
        fields = '__all__'


class ElectorAdmin3(ImportExportModelAdmin):
    resource_class = ElectorResources3 
    form = ElectorForm2 
    readonly_fields = ('ci','nombre','apellido','edad')   
    list_display =['orden','ci','nombre','apellido','edad','tipo_voto','manzana','nro_casa']
    list_editable =['tipo_voto','nro_casa'] #Consume muchos recursos (tarda mucho la consulta)
    list_filter =['ciudad','seccional','barrio','manzana','tipo_voto','mesa']
    search_fields =['ci','nombre','apellido']
    list_display_links = ['ci','nombre','apellido']
    list_per_page = 25
    # ordering = ['seccional','-barrio','manzana','nro_casa']

    def edad(self,obj):
        return obj.get_edad()
    edad.short_description = 'Edad'
    edad.admin_order_field = 'edad'
    
    '''Filtrar solo los tipos de votos activos'''
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tipo_voto':
            kwargs["queryset"] = TipoVoto.objects.filter(activo__exact=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    

''' 
=======================
=== REGISTRAR ADMIN ===
======================= '''
admin.site.register(LocalVotacion, ModelAdmin)
admin.site.register(Elector, ElectorAdmin)
admin.site.register(Elector2, ElectorAdmin2)
admin.site.register(Elector3, ElectorAdmin3)
admin.site.register(Padgral, PadGralAdmin)


