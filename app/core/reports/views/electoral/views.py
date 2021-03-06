import json
from config import settings

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


'''Reporte de Barrios y Manzanas con Codigo'''
class RptElectoral000ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_electoral000.html'
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
				# print(request.POST)
				seccional = request.POST.getlist('seccional[]') if 'seccional[]' in request.POST else ''
				barrio = request.POST.getlist('barrio[]') if 'barrio[]' in request.POST else ''
				manzana = request.POST.getlist('manzana[]') if 'manzana[]' in request.POST else ''
				# end_date = request.POST['end_date']
				_where = "1=1"
				if len(seccional):
					_where += f" AND electoral_elector.seccional_id IN {seccional}"
				if len(barrio):
					_where += f" AND electoral_elector.barrio_id IN {barrio}"
				if len(manzana):
					_where += f" AND electoral_elector.manzana_id IN {manzana}"
				_where = _where.replace('[','(').replace(']',')')
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
				data['error'] = 'No ha ingresado una opci??n'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Barrios y Manzanas'
		return context

class RptPadron001ReportView(ModuleMixin, FormView):
	template_name = 'electoral/reports/rpt_padron001.html'
	form_class = ReportForm

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		action = request.POST['action']
		data = {}
		print(request.POST)
		try:
			if action == 'report':
				data = []
				# local_votacion = int(request.POST['local_votacion']) if request.POST['local_votacion'] else None
				local_votacion = request.POST.getlist('local_votacion') if 'local_votacion' in request.POST else None
				# barrio = int(request.POST['barrio']) if request.POST['barrio'] else None
				barrio = request.POST.getlist('barrio') if 'barrio' in request.POST else None
				# tipo_voto = int(request.POST['tipo_voto']) if request.POST['tipo_voto'] else None	
				tipo_voto = request.POST.getlist('tipo_voto') if 'tipo_voto' in request.POST else None
				# Tipo de Voto I - INDECISO es igual a NO DEFINIDOS null ver query reporte		
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_padron001'
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				#PARAMETROS
				report.params['P_TITULO3'] = 'TRIBUNAL ELECTORAL PARTIDARIO'
				report.params['P_LOCAL_VOTACION_ID']= ",".join(local_votacion) if local_votacion else None
				report.params['P_BARRIO_ID'] =",".join(barrio) if barrio else None
				report.params['P_TIPO_VOTO_ID'] = ",".join(tipo_voto) if tipo_voto else None
				return report.render_to_response()

			else:
				data['error'] = 'No ha ingresado una opci??n'
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
		print(request.POST)
		try:
			if action == 'report':
				data = []
				local_votacion = request.POST.getlist('local_votacion') if 'local_votacion' in request.POST else None
				barrio = request.POST.getlist('barrio') if 'barrio' in request.POST else None
				manzana = request.POST.getlist('manzana') if 'manzana' in request.POST else None
				salto_pagina = request.POST.getlist('salto_pagina') if 'salto_pagina' in request.POST else None
				titulo_extra = request.POST.getlist('titulo_extra') if 'titulo_extra' in request.POST else ''						 
				#CONFIG				 
				report = JasperReportBase() 
				report.report_name  = 'rpt_electoral001'				
				
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				if len(titulo_extra):
					report.report_title = titulo_extra[0]
				#PARAMETROS                        
				report.params['P_LOCAL_VOTACION_ID']= ",".join(local_votacion) if local_votacion else None
				report.params['P_BARRIO_ID']= ",".join(barrio) if barrio else None
				report.params['P_MANZANA_ID']= ",".join(manzana) if manzana else None
				
				if not salto_pagina: 
					report.report_name  = 'rpt_electoral001_ss'

				return report.render_to_response()			   

			else:
				data['error'] = 'No ha ingresado una opci??n'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Elector por Barrios y Manzanas'
		context['action'] = 'report'
		return context

'''Electores por Barrios y Manzanas'''
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
			if action == 'report':
				data = []
				local_votacion = request.POST.getlist('local_votacion') if 'local_votacion' in request.POST else None
				barrio = request.POST.getlist('barrio') if 'barrio' in request.POST else None
				manzana = request.POST.getlist('manzana') if 'manzana' in request.POST else None
				salto_pagina = request.POST.getlist('salto_pagina') if 'salto_pagina' in request.POST else None
				titulo_extra = request.POST.getlist('titulo_extra') if 'titulo_extra' in request.POST else ''
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_electoral002'
				report.report_url = reverse_lazy(report.report_name)	
				
				report.report_title = Module.objects.filter(url=report.report_url).first().name  
				if len(titulo_extra):
					report.report_title = titulo_extra[0]
						                      
				#PARAMETROS                        
				report.params['P_LOCAL_VOTACION_ID']= ",".join(local_votacion) if local_votacion else None
				report.params['P_BARRIO_ID']= ",".join(barrio) if barrio else None
				report.params['P_MANZANA_ID']= ",".join(manzana) if manzana else None
				
				if not salto_pagina:
					report.report_name  = 'rpt_electoral002_ss'

				return report.render_to_response()			   

			else:
				data['error'] = 'No ha ingresado una opci??n'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Elector por Barrios y Manzanas'
		context['action'] = 'report'
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
				local_votacion = request.POST.getlist('local_votacion') if 'local_votacion' in request.POST else None
										 
				#CONFIG				 
				report = JasperReportBase()  
				report.report_name  = 'rpt_estadistica001'
				report.report_url = reverse_lazy(report.report_name)
				report.report_title = report_title = Module.objects.filter(url=report.report_url).first().name                        
				#PARAMETROS 
				report.params['P_LOCAL_VOTACION_ID']= ",".join(local_votacion) if local_votacion else None	
				
				return report.render_to_response()			   

			else:
				data['error'] = 'No ha ingresado una opci??n'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Reporte de Estadisticas Votos Positivos vs Negativos'
		context['action'] = 'report'
		return context
