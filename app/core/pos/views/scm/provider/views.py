import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Provider, ProviderForm
from core.security.mixins import PermissionMixin


class ProviderListView(PermissionMixin, ListView):
    model = Provider
    template_name = 'scm/provider/list.html'
    permission_required = 'view_provider'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('provider_create')
        context['title'] = 'Listado de Proveedores'
        return context


class ProviderCreateView(PermissionMixin, CreateView):
    model = Provider
    template_name = 'scm/provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'add_provider'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Provider.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if Provider.objects.filter(email=obj):
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
        context['title'] = 'Nuevo registro de un Proveedor'
        context['action'] = 'add'
        return context


class ProviderUpdateView(PermissionMixin, UpdateView):
    model = Provider
    template_name = 'scm/provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'change_provider'

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
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'mobile':
                if Provider.objects.filter(mobile=obj).exclude(id=id):
                    data['valid'] = False
            elif type == 'email':
                if Provider.objects.filter(email=obj).exclude(id=id):
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
        context['title'] = 'Edición de un Proveedor'
        context['action'] = 'edit'
        return context


class ProviderDeleteView(PermissionMixin, DeleteView):
    model = Provider
    template_name = 'scm/provider/delete.html'
    success_url = reverse_lazy('provider_list')
    permission_required = 'delete_provider'

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
