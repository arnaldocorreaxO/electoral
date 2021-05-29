from core.base.models import Reporte
import json
from django.db.models.aggregates import Count
from core.reports.jasperbase import JasperReportBase

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.electoral.models import Barrio, Elector, Manzana
from core.reports.forms import ReportForm, ReportFormElector001
from core.security.mixins import ModuleMixin

'''Reporte de Barrios y Manzanas con Codigo'''
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
                        .annotate(cant_elector=Count(True)) \
                        .order_by('barrio__cod',
                                  'manzana__cod')
                for i in qs:
                    item = {'barrio':f"({i['barrio__id']}) - {i['barrio__denominacion']}" ,\
                           'manzana':f"({i['barrio__id']} / {i['manzana__cod']}) - {i['manzana__denominacion']}",\
                           'cant_elector': i['cant_elector']
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




class RptElectoral001Config(JasperReportBase):
    report_name  = 'rpt_electoral001'
    
    


'''Electores por Barrios y Manzanas'''
class Rpt002ReportView(ModuleMixin, FormView):
    template_name = 'electoral/reports/rpt002.html'
    form_class = ReportFormElector001

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'report':
                data = []
                barrio = int(request.POST['barrio']) if request.POST['barrio'] else None
                manzana = int(request.POST['manzana']) if request.POST['manzana'] else None
                         
                report = RptElectoral001Config()     
                report.report_title = report_title = Reporte.objects.filter(nombre_reporte=report.report_name).first().titulo_reporte                        
                report.params['P_BARRIO_ID']= barrio
                report.params['P_MANZANA_ID']= manzana 
                
                return report.render_to_response()
               

            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Elector por Barrios y Manzanas'
        context['action'] = 'report'
        return context