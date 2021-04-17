import json
from django.db.models.aggregates import Count

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.electoral.models import Barrio, Elector, Manzana
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


class Rpt001ReportView(ModuleMixin, FormView):
    template_name = 'electoral/reports/rpt001.html'
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
                qs = Elector.objects.values('barrio__id','barrio__denominacion','manzana__cod','manzana__denominacion',) \
                        .extra(select = {'barrio__cod': 'CAST (electoral_elector.barrio_id AS INTEGER)'})\
                        .annotate(cant_manzana=Count(True)) \
                        .order_by('barrio__cod',
                                  'manzana__cod')
                # if len(start_date) and len(end_date):
                #     pass
                #     # search = search.filter(date_joined__range=[start_date, end_date])
                # for i in search:
                #     data.append(i.toJSON())
                print(qs.query)
                for i in qs:
                    item = {'barrio':f"({i['barrio__id']}) - {i['barrio__denominacion']}" ,\
                           'manzana':f"({i['barrio__id']} / {i['manzana__cod']}) - {i['manzana__denominacion']}",\
                           'cant_manzana': i['cant_manzana']
                           }
                    data.append(item)
                print(data)

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Barrios y Manzanas'
        return context