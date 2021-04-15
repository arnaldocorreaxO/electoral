from core.electoral.views.padron.departamento.views import *
from core.electoral.views.padron.distrito.views import *
from core.electoral.views.padron.seccional.views import *
from core.electoral.views.padron.ciudad.views import *
from core.electoral.views.padron.barrio.views import *
from core.electoral.views.padron.manzana.views import *
from core.electoral.views.padron.elector.views import *
from django.urls import path



urlpatterns = [
    # Departamento
    path('padron/departamento', DepartamentoListView.as_view(), name='departamento_list'),
    path('padron/departamento/add/', DepartamentoCreateView.as_view(), name='departamento_create'),
    path('padron/departamento/update/<int:pk>/', DepartamentoUpdateView.as_view(), name='departamento_update'),
    path('padron/departamento/delete/<int:pk>/', DepartamentoDeleteView.as_view(), name='departamento_delete'),
    #Distrito
    path('padron/distrito', DistritoListView.as_view(), name='distrito_list'),
    path('padron/distrito/add/', DistritoCreateView.as_view(), name='distrito_create'),
    path('padron/distrito/update/<int:pk>/', DistritoUpdateView.as_view(), name='distrito_update'),
    path('padron/distrito/delete/<int:pk>/', DistritoDeleteView.as_view(), name='distrito_delete'),
    #Seccional
    path('padron/seccional', SeccionalListView.as_view(), name='seccional_list'),
    path('padron/seccional/add/', SeccionalCreateView.as_view(), name='seccional_create'),
    path('padron/seccional/update/<int:pk>/', SeccionalUpdateView.as_view(), name='seccional_update'),
    path('padron/seccional/delete/<int:pk>/', SeccionalDeleteView.as_view(), name='seccional_delete'),
    #Ciudad
    path('padron/ciudad', CiudadListView.as_view(), name='ciudad_list'),
    path('padron/ciudad/add/', CiudadCreateView.as_view(), name='ciudad_create'),
    path('padron/ciudad/update/<int:pk>/', CiudadUpdateView.as_view(), name='ciudad_update'),
    path('padron/ciudad/delete/<int:pk>/', CiudadDeleteView.as_view(), name='ciudad_delete'),
    #Barrio
    path('padron/barrio', BarrioListView.as_view(), name='barrio_list'),
    path('padron/barrio/add/', BarrioCreateView.as_view(), name='barrio_create'),
    path('padron/barrio/update/<int:pk>/', BarrioUpdateView.as_view(), name='barrio_update'),
    path('padron/barrio/delete/<int:pk>/', BarrioDeleteView.as_view(), name='barrio_delete'),
    #Manzana
    path('padron/manzana', ManzanaListView.as_view(), name='manzana_list'),
    path('padron/manzana/add/', ManzanaCreateView.as_view(), name='manzana_create'),
    path('padron/manzana/update/<int:pk>/', ManzanaUpdateView.as_view(), name='manzana_update'),
    path('padron/manzana/delete/<int:pk>/', ManzanaDeleteView.as_view(), name='manzana_delete'),
    #Elector
    path('padron/elector', ElectorListView.as_view(), name='elector_list'),
    path('padron/elector/add/', ElectorCreateView.as_view(), name='elector_create'),
    path('padron/elector/update/<int:pk>/', ElectorUpdateView.as_view(), name='elector_update'),
    path('padron/elector/delete/<int:pk>/', ElectorDeleteView.as_view(), name='elector_delete'),

   ]
