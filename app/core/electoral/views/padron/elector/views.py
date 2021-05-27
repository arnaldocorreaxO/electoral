import math
from core.reports.jasperbase import JasperReportBase
from core.electoral.models import Manzana
from datetime import date, datetime
from core.reports.forms import ReportForm
import json

from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from core.electoral.forms import Elector, ElectorForm
from core.security.mixins import PermissionMixin


class ElectorListView(PermissionMixin, FormView):
	# model = Elector
	template_name = 'padron/elector/list.html'
	permission_required = 'view_elector'
	form_class = ReportForm
 
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'search':
				data = []
				start_date = request.POST['start_date']
				end_date = request.POST['end_date']

				_start = request.POST['start']
				_length = request.POST['length']
				_search = request.POST['search[value]']

				# print(request.POST)
				_where = "'' = %s"
				if len(_search):
					if _search.isnumeric():
						_where = " ci = %s"
					else:
						_search = '%' + _search.replace(' ', '%') + '%'
						_where = " upper(nombre||' '|| apellido) LIKE upper(%s)"
						# _where += " OR upper(barrio||' '|| manzana) LIKE upper(%s)"
						# _where += " OR upper(edad) LIKE upper(%s)"
				print(_where)
				qs = Elector.objects.filter()\
									.extra(where=[_where], params=[_search])

				if len(start_date) and len(end_date):
					# search = search.filter(fecha_nacimiento__range=[start_date, end_date])
					# print(today.month)
					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					qs = qs.filter(fecha_nacimiento__month=start_date.month,
								   fecha_nacimiento__day__exact=start_date.day)

				total = qs.count()

				if _start and _length:
					start = int(_start)
					length = int(_length)
					page = math.ceil(start / length) + 1
					per_page = length

					qs = qs[start:start + length]

				position = 1
				for i in qs:
					item = i.toJSON()
					item['position'] = position
					data.append(item)
					position += 1

				data = {'data': data,
						'page': page,  # [opcional]
						'per_page': per_page,  # [opcional]
						'recordsTotal': total,
						'recordsFiltered': total, }
			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url'] = reverse_lazy('elector_create')
		context['title'] = 'Listado de electores'
		return context


class ElectorCreateView(PermissionMixin, CreateView):
	model = Elector
	template_name = 'padron/elector/create.html'
	form_class = ElectorForm
	success_url = reverse_lazy('elector_list')
	permission_required = 'add_elector'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def validate_data(self):
		data = {'valid': True}
		try:
			
			type = self.request.POST['type']
			obj = self.request.POST['obj'].strip()            
			if type == 'denominacion':                
				if Elector.objects.filter(denominacion__iexact=obj):
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
			elif action == 'search_manzana_id':
				data = [{'id': '', 'text': '------------'}]
				for i in Manzana.objects.filter(barrio_id=request.POST['id']):			
					data.append({'id': i.id, 'text': str(i), 'data': i.barrio.toJSON()})
			else:
				data['error'] = 'No ha seleccionado ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['list_url'] = self.success_url
		context['title'] = 'Nuevo registro de un elector'
		context['action'] = 'add'
		return context


class ElectorUpdateView(PermissionMixin, UpdateView):
	model = Elector
	template_name = 'padron/elector/create.html'
	form_class = ElectorForm
	success_url = reverse_lazy('elector_list')
	permission_required = 'change_elector'

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
				if Elector.objects.filter(name__iexact=obj).exclude(id=id):
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
			elif action == 'search_manzana_id':
				data = [{'id': '', 'text': '------------'}]
				for i in Manzana.objects.filter(barrio_id=request.POST['id']):
					data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
			else:
				data['error'] = 'No ha seleccionado ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['list_url'] = self.success_url
		context['title'] = 'Edición de un elector'
		context['action'] = 'edit'
		return context


class ElectorDeleteView(PermissionMixin, DeleteView):
	model = Elector
	template_name = 'padron/elector/delete.html'
	success_url = reverse_lazy('elector_list')
	permission_required = 'delete_elector'

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


def test_reporte(request):
	# debemos obtener nuestro objeto classroom haciendo la consulta a la base de datos
	report = JasperReportBase()
	report.report_name ='rpt_001'
	return report.render_to_response()
