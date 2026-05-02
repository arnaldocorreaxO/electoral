from django.contrib import admin
from .models import *

# Register your models here.
class ModeloAdminBase(admin.ModelAdmin):
    readonly_fields = ['usu_insercion',
                       'fec_insercion',
                       'usu_modificacion',
                       'fec_modificacion',
                       ]
    list_display = ['__str__',
                    'get_name_usu_insercion',
                    'fec_insercion',
                    'get_name_usu_modificacion',
                    'fec_modificacion',
                    ]
class ParametroModelAdmin(ModeloAdminBase):
    list_display = ['grupo','parametro','descripcion','valor']
    search_fields = ['grupo','parametro','descripcion','valor']
    

admin.site.register(Parametro,ParametroModelAdmin)
admin.site.register(Modulo,ModeloAdminBase)
admin.site.register(Reporte,ModeloAdminBase)
