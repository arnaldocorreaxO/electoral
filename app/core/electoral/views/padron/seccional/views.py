import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.electoral.forms import Seccional, SeccionalForm
from core.security.mixins import PermissionMixin


class SeccionalListView(PermissionMixin, ListView):
    model = Seccional
    template_name = 'padron/seccional/list.html'
    permission_required = 'view_seccional'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('seccional_create')
        context['title'] = 'Listado de Seccionales'
        return context


class SeccionalCreateView(PermissionMixin, CreateView):
    model = Seccional
    template_name = 'padron/seccional/create.html'
    form_class = SeccionalForm
    success_url = reverse_lazy('seccional_list')
    permission_required = 'add_seccional'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if Seccional.objects.filter(denominacion__iexact=obj):
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
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Seccional'
        context['action'] = 'add'
        return context


class SeccionalUpdateView(PermissionMixin, UpdateView):
    model = Seccional
    template_name = 'padron/seccional/create.html'
    form_class = SeccionalForm
    success_url = reverse_lazy('seccional_list')
    permission_required = 'change_seccional'

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
                if Seccional.objects.filter(denominacion__iexact=obj).exclude(id=id):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                return self.validate_data()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Seccional'
        context['action'] = 'edit'
        return context


class SeccionalDeleteView(PermissionMixin, DeleteView):
    model = Seccional
    template_name = 'padron/seccional/delete.html'
    success_url = reverse_lazy('seccional_list')
    permission_required = 'delete_seccional'

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
