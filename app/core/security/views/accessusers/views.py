import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, TemplateView

from core.security.mixins import PermissionMixin
from core.security.models import AccessUsers


class UsersListView(PermissionMixin, TemplateView):
    template_name = 'accessusers/list.html'
    permission_required = 'view_accessusers'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                search = AccessUsers.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['start_date']
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for a in search:
                    data.append(a.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Accesos de los usuarios'
        return context


class UsersDeleteView(PermissionMixin, DeleteView):
    model = AccessUsers
    template_name = 'accessusers/delete.html'
    success_url = reverse_lazy('accessusers_list')
    permission_required = 'delete_accessusers'

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
