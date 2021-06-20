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

from core.electoral.forms import Elector, ElectorForm, ShearchForm
from core.security.mixins import PermissionMixin

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.contrib.auth.decorators import permission_required

class ElectorListView(PermissionMixin, FormView):
	# model = Elector
	template_name = 'padron/elector/list.html'
	permission_required = 'view_elector'
	form_class = ShearchForm
 
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		# print(request.POST)
		try:
			if action == 'search':
				data = []
				term = request.POST['term']
				start_date = request.POST['start_date']
				end_date = request.POST['end_date']
				ciudad = request.POST['ciudad']
				seccional = request.POST['seccional']
				barrio = request.POST['barrio']
				manzana = request.POST['manzana']
				mesa = request.POST['mesa']

				_start = request.POST['start']
				_length = request.POST['length']
				_search = request.POST['search[value]']
								
				# _order = ['barrio','manzana','nro_casa'] debe enviarse ya el orden desde el datatable para default
				_order = []
				# print(request.POST)
				#range(start, stop, step)
				for i in range(9): 
					_column_order = f'order[{i}][column]'
					# print('Column Order:',_column_order)
					if _column_order in request.POST:					
						_column_number = request.POST[_column_order]
						# print('Column Number:',_column_number)
						if _column_number == '9': #Hacemos esto por que en el datatable edad es un campo calculado
							_order.append('fecha_nacimiento')
						elif _column_number == '2': #Hacemos esto por que en el datatable fullname es un campo calculado
							_order.append('apellido')
							_order.append('nombre')
						else:			
							_order.append(request.POST[f'columns[{_column_number}][data]'].split(".")[0])
					if f'order[{i}][dir]' in request.POST:
						_dir = request.POST[f'order[{i}][dir]']
						if (_dir=='desc'):
							_order[i] = f"-{_order[i]}"
				# print('Order:', _order)
				if len(term):
					_search = term

				_where = "'' = %s"
				if len(_search):
					if _search.isnumeric():
						_where = " ci = %s"
					else:
						_search = '%' + _search.replace(' ', '%') + '%'
						_where = " upper(nombre||' '|| apellido) LIKE upper(%s)"
				
				if len(ciudad):
					_where += f" AND electoral_elector.ciudad_id = '{ciudad}'"
				if len(seccional):
					_where += f" AND electoral_elector.seccional_id = '{seccional}'"
				if len(barrio):
					_where += f" AND electoral_elector.barrio_id = '{barrio}'"
				if len(manzana):
					_where += f" AND electoral_elector.manzana_id = '{manzana}'"
				if len(mesa):
					_where += f" AND electoral_elector.mesa = '{mesa}'"
				
				qs = Elector.objects.filter()\
									.extra(where=[_where], params=[_search])\
									.order_by(*_order)

				if len(start_date) and len(end_date):
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

				position = start + 1
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
		context['title'] = 'Listado de Electores'
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
	
	# Este usamos para el modal 	
	def get(self, request, *args, **kwargs):
		data = {}				
		try:	
			if request.user.has_perm('electoral.change_elector'):			
				pk = kwargs['pk']
				elector = get_object_or_404(Elector, pk=pk)
				form = ElectorForm(instance=elector)
				context = self.get_context_data()
				context['form'] = form
				self.template_name = 'padron/elector/create_modal.html'
				context['action_url'] = reverse_lazy('elector_update', kwargs={'pk': pk})
				data['html_form'] = render_to_string(self.template_name, context, request=request)
			else:
				data['error'] = 'No tiene permisos para editar'
		
		except Exception as e:
			data['error'] = str(e)
		# print(data['html_form'])
		return HttpResponse(json.dumps(data), content_type='application/json')
		#return  JsonResponse(data)

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
