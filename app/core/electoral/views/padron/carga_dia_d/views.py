from django.db import transaction
from django.db.models.functions import Concat
from django.db.models.expressions import Value
from django.views.generic.base import TemplateView
from core.electoral.models import Manzana
from datetime import date, datetime
from core.reports.forms import ReportForm
import json

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from core.electoral.forms import Elector, CargaDiaDForm, ShearchForm
from core.security.mixins import ModuleMixin, PermissionMixin


class CargaDiaDListView(PermissionMixin, FormView):
    # model = Elector
    template_name = 'padron/carga_dia_d/list.html'
    permission_required = 'view_elector'
    form_class = ShearchForm
 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                term = request.POST['term']
                 
                if len(term):
                    term1 = 0
                    if term.isnumeric():
                        term1 = term
                    else:
                        term = '%' + term.replace(' ','%') + '%'
                    position = 1    
                    # q = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
                    #                  .filter( Q(ci=term1) | Q(fullname__icontains=term)) \
                    #                  .extra(where=['ci = %s OR upper(nombre|| " "|| apellido) LIKE upper(%s)'], params=[term1,term]) \
                    #                  .order_by('fullname')[0:10].query
                    qs = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
                                     .extra(where=['ci = %s OR upper(nombre|| " "|| apellido) LIKE upper(%s)'], params=[term1,term]) \
                                     .order_by('fullname')[0:10]
                    # print(qs.query)

                    for i in qs:
                        item = i.toJSON()
                        item['position'] = position
                        item['fullname'] = f"{item['apellido']}, {item['nombre']}"
                        data.append(item)
                        position += 1
                    # print(data)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('elector_create')
        context['title'] = 'Carga de Votos Electores'
        return context


class CargaDiaDCreateView(PermissionMixin, CreateView):
    model = Elector
    template_name = 'padron/carga_dia_d/create.html'
    form_class = CargaDiaDForm
    success_url = reverse_lazy('elector_list')
    permission_required = 'add_elector'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if Elector.objects.filter(denominacion__iexact=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'search_manzana_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Manzana.objects.filter(barrio_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Carga Día D - Veedor'
        context['action'] = 'add'
        return context


class CargaDiaDUpdateView(PermissionMixin, UpdateView):
    model = Elector
    template_name = 'padron/carga_dia_d/create.html'
    form_class = CargaDiaDForm
    success_url = reverse_lazy('carga_dia_d_list')
    permission_required = 'change_elector'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            id = self.get_object().id
            if type == 'denominacion':
                if Elector.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                elector = self.object
                # elector.pasoxmv = 'S'
                elector.pasoxmv = 'S'
                # data = self.get_form().save()
                elector.save()
            elif action == 'edit_pc':
                elector = self.object
                elector.pasoxpc = 'S'
                # data = self.get_form().save()
                elector.save()
            elif action == 'validate_data':
                return self.validate_data()
            elif action == 'search_manzana_id':
                data = [{'id': '', 'text': '------------'}]
                for i in Manzana.objects.filter(barrio_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Carga Día D - Veedor'
        context['action'] = 'edit'
        return context


class CargaDiaDDeleteView(PermissionMixin, DeleteView):
    model = Elector
    template_name = 'padron/carga_dia_d/delete.html'
    success_url = reverse_lazy('carga_dia_d_list')
    permission_required = 'delete_elector'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context



class CargaElectorDiaDView(ModuleMixin, TemplateView):
    template_name = 'padron/carga_dia_d/carga_dia_d_elector.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search_elector':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Elector.objects.exclude(id__in=ids).order_by('apellido','nombre')
                if len(term):
                    search = search.filter(apellido__icontains=term)
                    search = search[0:10]
                for i in search:
                    item = i.toJSON()
                    item['value'] = '{} / {}'.format(i.nombre, i.apellido)
                    data.append(item)
            elif action == 'create':
                with transaction.atomic():
                    productsjson = json.loads(request.POST['products'])
                    for p in productsjson:
                        product = Elector.objects.get(pk=p['id'])
                        product.stock = int(p['newstock'])
                        product.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carga Día D Puesto de Control'
        return context