import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from core.pos.forms import CompanyForm, Company
from core.security.mixins import ModuleMixin


class CompanyUpdateView(ModuleMixin, UpdateView):
    template_name = 'crm/company/create.html'
    form_class = CompanyForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            comp = self.get_object()
            comp.name = request.POST['name']
            comp.ruc = request.POST['ruc']
            comp.mobile = request.POST['mobile']
            comp.phone = request.POST['phone']
            comp.email = request.POST['email']
            comp.website = request.POST['website']
            comp.address = request.POST['address']
            if 'image' in request.FILES:
                comp.image = request.FILES['image']
            if 'image-clear' in request.POST:
                comp.remove_image()
            comp.desc = request.POST['desc']
            comp.iva = float(request.POST['iva'])
            comp.save()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Configuración de la Compañia'
        return context
