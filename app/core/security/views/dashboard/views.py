import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from config import settings
from core.security.forms import Dashboard, DashboardForm
from core.security.mixins import ModuleMixin


class DashboardView(ModuleMixin, FormView):
    template_name = 'dashboard/create.html'
    form_class = DashboardForm
    success_url = settings.LOGIN_REDIRECT_URL

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = DashboardForm(instance=self.get_object())
        return form

    def get_object(self, queryset=None):
        comps = Dashboard.objects.filter()
        if comps:
            return comps[0]
        return Dashboard()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                dashboard = self.get_object()
                dashboard.name = request.POST['name']
                dashboard.icon = request.POST['icon']
                if 'image-clear' in request.POST:
                    dashboard.remove_image()
                if 'image' in request.FILES:
                    dashboard.image = request.FILES['image']
                dashboard.layout = request.POST['layout']
                dashboard.navbar = request.POST['navbar']
                dashboard.brand_logo = request.POST['brand_logo']
                dashboard.sidebar = request.POST['sidebar']
                dashboard.card = request.POST['card']
                dashboard.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición del Dashboard'
        context['action'] = 'edit'
        return context
