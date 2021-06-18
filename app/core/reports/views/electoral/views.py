import json

from core.electoral.models import Elector
from core.reports.forms import ReportForm
from core.reports.jasperbase import JasperReportBase
from core.security.mixins import ModuleMixin
from core.security.models import Module
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

class RptPadron001ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_padron001.html'
	form_class = ReportForm

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		action = request.POST['action']
		data = {}
		try:
			if action == 'report':
				data = []
				local_votacion = int(request.POST['local_votacion']) if request.POST['local_votacion'] else None
				barrio = int(request.POST['barrio']) if request.POST['barrio'] else None
				tipo_voto = int(request.POST['tipo_voto']) if request.POST['tipo_voto'] else None	
				# Tipo de Voto I - INDECISO es igual a NO DEFINIDOS null ver query reporte		
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_padron001'
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				#PARAMETROS
				report.params['P_TITULO3'] = 'TRIBUNAL ELECTORAL PARTIDARIO'
				report.params['P_LOCAL_VOTACION_ID']= local_votacion
				report.params['P_BARRIO_ID'] = barrio
				report.params['P_TIPO_VOTO_ID'] = tipo_voto
				return report.render_to_response()

			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Padron'
		context['action'] = 'report'
		return context


'''Electores por Barrios y Manzanas'''
class RptElectoral001ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_electoral001.html'
	form_class = ReportForm

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
						 
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_electoral001'
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				#PARAMETROS                        
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


'''Reporte de Barrios y Manzanas con Codigo'''
class RptElectoral002ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_electoral002.html'
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
				print(request.POST)
				seccional = request.POST['seccional']
				barrio = request.POST['barrio']
				manzana = request.POST['manzana']
				# end_date = request.POST['end_date']
				_where = "1=1"
				if len(seccional):
					_where += f" AND electoral_elector.seccional_id = '{seccional}'"
				if len(barrio):
					_where += f" AND electoral_elector.barrio_id = '{barrio}'"
				if len(manzana):
					_where += f" AND electoral_elector.manzana_id = '{manzana}'"
				print(_where)
				qs = Elector.objects.values('barrio__id','barrio__denominacion','manzana__cod','manzana__denominacion',) \
						.extra(select = {'barrio__cod': 'CAST (electoral_elector.barrio_id AS INTEGER)'})\
						.annotate(cant_elector=Count(True)) \
						.extra(where=[_where])\
						.order_by('barrio__cod',
								  'manzana__cod')
				for i in qs:
					item = {'barrio':f"({i['barrio__id']}) - {i['barrio__denominacion']}" ,\
						   'manzana':f"({i['barrio__id']} / {i['manzana__cod']}) - {i['manzana__denominacion']}",\
						   'cant_elector': i['cant_elector']
						   }
					data.append(item)
				# print(data)
			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Barrios y Manzanas'
		return context


'''Estadistica de Votos Positivos vs Negativos'''
class RptEstadistica001ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_estadistica001.html'
	form_class = ReportForm

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		action = request.POST['action']
		data = {}
		try:
			if action == 'report':
				data = []
				local_votacion = int(request.POST['local_votacion']) if request.POST['local_votacion'] else None
										 
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_estadistica001'
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				#PARAMETROS 
				report.params['P_LOCAL_VOTACION_ID']= local_votacion				
				
				return report.render_to_response()			   

			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Estadisticas Votos Positivos vs Negativos'
		context['action'] = 'report'
		return context