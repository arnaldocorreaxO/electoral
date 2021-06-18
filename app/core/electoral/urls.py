from core.electoral.views.padron.departamento.views import *
from core.electoral.views.padron.distrito.views import *
from core.electoral.views.padron.seccional.views import *
from core.electoral.views.padron.pais.views import *
from core.electoral.views.padron.ciudad.views import *
from core.electoral.views.padron.barrio.views import *
from core.electoral.views.padron.manzana.views import *
from core.electoral.views.padron.tipo_voto.views import *
from core.electoral.views.padron.elector.views import *
from core.electoral.views.padron.carga_dia_d.views import *

from django.urls import path



urlpatterns = [
    # Departamento
    path('departamento', DepartamentoListView.as_view(), name='departamento_list'),
    path('departamento/add/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamento/update/<int:pk>/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('departamento/delete/<int:pk>/', DepartamentoDeleteView.as_view(), name='departamento_delete'),
    #Distrito
    path('distrito', DistritoListView.as_view(), name='distrito_list'),
    path('distrito/add/', DistritoCreateView.as_view(), name='distrito_create'),
    path('distrito/update/<int:pk>/', DistritoUpdateView.as_view(), name='distrito_update'),
    path('distrito/delete/<int:pk>/', DistritoDeleteView.as_view(), name='distrito_delete'),
    #Seccional
    path('seccional', SeccionalListView.as_view(), name='seccional_list'),
    path('seccional/add/', SeccionalCreateView.as_view(), name='seccional_create'),
    path('seccional/update/<int:pk>/', SeccionalUpdateView.as_view(), name='seccional_update'),
    path('seccional/delete/<int:pk>/', SeccionalDeleteView.as_view(), name='seccional_delete'),
    #Paises
    path('pais', PaisListView.as_view(), name='pais_list'),
    path('pais/add/', PaisCreateView.as_view(), name='pais_create'),
    path('pais/update/<int:pk>/', PaisUpdateView.as_view(), name='pais_update'),
    path('pais/delete/<int:pk>/', PaisDeleteView.as_view(), name='pais_delete'),
    #Ciudad
    path('ciudad', CiudadListView.as_view(), name='ciudad_list'),
    path('ciudad/add/', CiudadCreateView.as_view(), name='ciudad_create'),
    path('ciudad/update/<int:pk>/', CiudadUpdateView.as_view(), name='ciudad_update'),
    path('ciudad/delete/<int:pk>/', CiudadDeleteView.as_view(), name='ciudad_delete'),
    #Barrio
    path('barrio', BarrioListView.as_view(), name='barrio_list'),
    path('barrio/add/', BarrioCreateView.as_view(), name='barrio_create'),
    path('barrio/update/<int:pk>/', BarrioUpdateView.as_view(), name='barrio_update'),
    path('barrio/delete/<int:pk>/', BarrioDeleteView.as_view(), name='barrio_delete'),
    #Manzana
    path('manzana', ManzanaListView.as_view(), name='manzana_list'),
    path('manzana/add/', ManzanaCreateView.as_view(), name='manzana_create'),
    path('manzana/update/<int:pk>/', ManzanaUpdateView.as_view(), name='manzana_update'),
    path('manzana/delete/<int:pk>/', ManzanaDeleteView.as_view(), name='manzana_delete'),
    #Tipo Voto
    path('tipovoto', TipoVotoListView.as_view(), name='tipo_voto_list'),
    path('tipovoto/add/', TipoVotoCreateView.as_view(), name='tipo_voto_create'),
    path('tipovoto/update/<int:pk>/', TipoVotoUpdateView.as_view(), name='tipo_voto_update'),
    path('tipovoto/delete/<int:pk>/', TipoVotoDeleteView.as_view(), name='tipo_voto_delete'),
    #Elector
    path('elector', ElectorListView.as_view(), name='elector_list'),
    path('elector/add/', ElectorCreateView.as_view(), name='elector_create'),
    path('elector/update/<int:pk>/', ElectorUpdateView.as_view(), name='elector_update'),
    path('elector/delete/<int:pk>/', ElectorDeleteView.as_view(), name='elector_delete'),
    #Carga de Votos
    path('carga_dia_d_list_mv', CargaDiaDListView.as_view(), name='carga_dia_d_list_mv'),
    path('carga_dia_d_list_pc', CargaDiaDElectorView.as_view(), name='carga_dia_d_list_pc'),
    path('carga_dia_d/add/', CargaDiaDCreateView.as_view(), name='carga_dia_d_create'),
    path('carga_dia_d/update/<int:pk>/<opcion>/<valor>/', CargaDiaDUpdateView.as_view(), name='carga_dia_d_update'),
    path('carga_dia_d/delete/<int:pk>/', CargaDiaDDeleteView.as_view(), name='carga_dia_d_delete'),


    path('reporte', test_reporte, name='reporte_test'),

   ]
