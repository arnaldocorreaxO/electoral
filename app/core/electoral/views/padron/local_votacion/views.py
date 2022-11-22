import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.electoral.forms import LocalVotacion, LocalVotacionForm
from core.security.mixins import PermissionMixin


class LocalVotacionListView(PermissionMixin, ListView):
    model = LocalVotacion
    template_name = 'padron/local_votacion/list.html'
    permission_required = 'view_localvotacion'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.distrito:
            return self.model.objects.filter(ciudad__distrito=self.request.user.distrito)            
        else:
            return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('local_votacion_create')
        context['title'] = 'Listado de Local de Votaciones'
        context['distrito'] = self.request.user.distrito.denominacion
        return context


class LocalVotacionCreateView(PermissionMixin, CreateView):
    model = LocalVotacion
    template_name = 'padron/local_votacion/create.html'
    form_class = LocalVotacionForm
    success_url = reverse_lazy('local_votacion_list')
    permission_required = 'add_localvotacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()            
            if type == 'denominacion':                
                if LocalVotacion.objects.filter(denominacion__iexact=obj):
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
        context['title'] = 'Nuevo registro de un Local de Votacion'
        context['action'] = 'add'
        return context


class LocalVotacionUpdateView(PermissionMixin, UpdateView):
    model = LocalVotacion
    template_name = 'padron/local_votacion/create.html'
    form_class = LocalVotacionForm
    success_url = reverse_lazy('local_votacion_list')
    permission_required = 'change_localvotacion'

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
                if LocalVotacion.objects.filter(denominacion__iexact=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Local de Votacion'
        context['action'] = 'edit'
        return context


class LocalVotacionDeleteView(PermissionMixin, DeleteView):
    model = LocalVotacion
    template_name = 'padron/local_votacion/delete.html'
    success_url = reverse_lazy('local_votacion_list')
    permission_required = 'delete_localvotacion'

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
