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
from core.security.mixins import PermissionMixin


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
                    position = 1               
                    for p in Elector.objects.filter(
                            Q(ci=term1) | Q(apellido__icontains=term) | Q(nombre__icontains=term)).order_by('apellido','nombre')[0:10]:
                        item = p.toJSON()
                        item['position'] = position
                        data.append(item)
                        position += 1
                    print(data)
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
                elector.pasoxpc = 'S'
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
