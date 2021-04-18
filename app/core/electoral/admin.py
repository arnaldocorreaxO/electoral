from django.contrib import admin
# Register your models here.
from .models import Elector
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from core.electoral.models import Elector,Padgral
from core.electoral.forms import *

# ElectorForm = select2_modelform(Elector, attrs={'width': '250px'})

'''PAIS'''
class PaisAdmin(admin.ModelAdmin):
    class Meta:
        model= Pais


''' 
====================
===   ELECTOR    ===
==================== '''
class ElectorResource(resources.ModelResource):
    class Meta:
        model = Elector
        fields = '__all__'

class ElectorAdmin(ImportExportModelAdmin):
    form = ElectorForm
    resource_class = ElectorResource

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
        verbose_name_plural = 'Electores Barrio Manzanas'
        proxy = True

class ElectorResources2(resources.ModelResource):
    class Meta:
        model = Elector2
        fields = ('ci', 'nombre', 'apellido','telefono','barrio','manzana','nro_casa',)


class ElectorAdmin2(ImportExportModelAdmin):
    resource_class = ElectorResources2  
    form = ElectorForm2 
    readonly_fields = ('ci','nombre','apellido','edad')   
    list_display =['ci','nombre','apellido','telefono','barrio','manzana','nro_casa','edad']
    # list_editable =['telefono','barrio','manzana','nro_casa'] #Consume muchos recursos (tarda mucho la consulta)
    list_filter =['ciudad','seccional','barrio','manzana','tipo_voto']
    search_fields =['ci','nombre','apellido']
    list_display_links = ['ci','nombre','apellido']
    
    # ordering = ['seccional','-barrio','manzana','nro_casa']
    
    def edad(self,obj):
        return obj.get_edad()
    edad.short_description = 'Edad'

''' 
====================
===   ELECTOR3   ===
==================== '''
class Elector3(Elector):
    class Meta:
        verbose_name = 'Electores Preferencia de Votos'
        verbose_name_plural = 'Electores Preferencia de Votos'
        proxy = True

class ElectorResources3(resources.ModelResource):
    class Meta:
        model = Elector3
        fields = '__all__'


class ElectorAdmin3(ImportExportModelAdmin):
    resource_class = ElectorResources3 
    form = ElectorForm2 
    readonly_fields = ('ci','nombre','apellido','edad')   
    list_display =['ci','nombre','apellido','tipo_voto','manzana','nro_casa','edad']
    list_editable =['tipo_voto'] #Consume muchos recursos (tarda mucho la consulta)
    list_filter =['ciudad','seccional','barrio','manzana','tipo_voto']
    search_fields =['ci','nombre','apellido']
    list_display_links = ['ci','nombre','apellido']
    
    # ordering = ['seccional','-barrio','manzana','nro_casa']
    
    def edad(self,obj):
        return obj.get_edad()
    edad.short_description = 'Edad'
    

''' 
=======================
=== REGISTRAR ADMIN ===
======================= '''
admin.site.register(Elector, ElectorAdmin)
admin.site.register(Elector2, ElectorAdmin2)
admin.site.register(Elector3, ElectorAdmin3)
admin.site.register(Padgral, PadGralAdmin)
admin.site.register(Pais, PaisAdmin)