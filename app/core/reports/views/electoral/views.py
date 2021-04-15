import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.electoral.models import Elector
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ElectorReportView(ModuleMixin, FormView):
    template_name = 'electoral/elector_barrio_manzana/report.html'
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = Elector.objects.filter(barrio__exact=1)
                if len(start_date) and len(end_date):
                    pass
                    # search = search.filter(date_joined__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Elector por Barrios y Manzanas'
        return context
