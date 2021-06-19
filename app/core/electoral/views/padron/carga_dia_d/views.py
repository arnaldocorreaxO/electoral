import math
from django.db import transaction
from django.db.models.functions import Concat
from django.db.models.expressions import Value
from django.views.generic.base import TemplateView
from core.electoral.models import Manzana
from datetime import date, datetime
from core.reports.forms import ReportForm
import json

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from core.electoral.forms import Elector, CargaDiaDForm, ShearchForm
from core.security.mixins import ModuleMixin, PermissionMixin


class CargaDiaDListView(PermissionMixin, FormView):
	# model = Elector
	template_name = 'padron/carga_dia_d/list_carga_dia_d_elector_mv.html'
	permission_required = 'view_elector'
	form_class = ShearchForm
 
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'search':
				data = []
				term = request.POST['term']
				 
				if len(term):
					term1 = 0
					if term.isnumeric():
						term1 = term
					else:
						term = '%' + term.replace(' ','%') + '%'
					position = 1    
					qs = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
									 .extra(where=["ci = %s OR upper(nombre||' '|| apellido) LIKE upper(%s)"], params=[term1,term]) \
									 .order_by('fullname')[0:10]
					# print(qs.query)

					for i in qs:
						item = i.toJSON()
						item['position'] = position
						item['fullname'] = f"{item['apellido']}, {item['nombre']}"
						data.append(item)
						position += 1
					# print(data)
			elif action == 'search_pasoxmv':
				data = []          
				mesa = request.POST['mesa']
				local_votacion = request.POST['local_votacion']
				_start = request.POST['start']
				_length = request.POST['length']
				_search = request.POST['search[value]']

				_where = " '' = %s"           

				if len(_search):
					if _search.isnumeric():
						_where = " ci = %s"
					else:
						_search = '%' + _search.replace(' ','%') + '%'
						_where = " upper(nombre||' '|| apellido) LIKE upper(%s)"  
				
				if len(local_votacion):
					_where += f" AND local_votacion_id = '{local_votacion}'" 

				if len(mesa):
					_where += f" AND mesa = '{mesa}'"                
			  
				qs = Elector.objects.filter(pasoxmv='S')\
									.extra(where=[_where], params=[_search]) 

				# print(qs.query)
				total = qs.count()   

				if _start and _length:
					start = int(_start)
					length = int(_length)
					page = math.ceil(start / length) + 1
					per_page = length 

					qs = qs[start:start + length]                    
				
				for i in qs:
					item = i.toJSON()
					# item['position'] = position
					item['fullname'] = f"{item['apellido']}, {item['nombre']}"
					data.append(item)
					# position += 1   
				data = {'data': data,
						'page': page,  # [opcional]
						'per_page': per_page,  # [opcional]
						'recordsTotal': total,
						'recordsFiltered': total, }
			   
				# return JsonResponse(data,safe=False)
 
			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url'] = reverse_lazy('elector_create')
		context['title'] = 'Carga de Votos Mesa de Votacion'
		context['title2'] = 'Lista de Electores Mesa de Votación'
		return context


class CargaDiaDCreateView(PermissionMixin, CreateView):
	model = Elector
	template_name = 'padron/carga_dia_d/create.html'
	form_class = CargaDiaDForm
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
					data.append({'id': i.id, 'text': i.denominacion, 'data': i.barrio.toJSON()})
			else:
				data['error'] = 'No ha seleccionado ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['list_url'] = self.success_url
		context['title'] = 'Carga Día D - Veedor'
		context['action'] = 'add'
		return context


class CargaDiaDUpdateView(PermissionMixin, UpdateView):
	model = Elector
	template_name = 'padron/carga_dia_d/create.html'
	form_class = CargaDiaDForm
	success_url = reverse_lazy('carga_dia_d_list_mv')    
	permission_required = 'change_elector'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.opcion = kwargs['opcion']
		self.valor  = kwargs['valor']
		if self.opcion =='edit_pc':
			self.success_url = reverse_lazy('carga_dia_d_list_pc')
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
				elector = self.object
				if self.opcion == 'edit_pc':
					elector.pasoxpc = self.valor
				elif self.opcion == 'edit_mv':
					elector.pasoxmv = self.valor
				elector.save()
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
		context['title'] = 'Carga Día D - Elector'
		context['action'] = 'edit'
		return context


class CargaDiaDDeleteView(PermissionMixin, DeleteView):
	model = Elector
	template_name = 'padron/carga_dia_d/delete.html'
	success_url = reverse_lazy('carga_dia_d_list')
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

class CargaDiaDElectorView(PermissionMixin, FormView):
	# model = Elector
	template_name = 'padron/carga_dia_d/list_carga_dia_d_elector_pc.html'
	permission_required = 'view_elector'
	form_class = ShearchForm
 
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'search_elector':
				data = []
				term = request.POST['term']
				 
				if len(term):
					term1 = 0
					if term.isnumeric():
						term1 = term
					else:
						term = '%' + term.replace(' ','%') + '%'
					position = 1    
					
					qs = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
									 .extra(where=["ci = %s OR upper(nombre||' '|| apellido) LIKE upper(%s)"], params=[term1,term]) \
									 .order_by('fullname')[0:10]
					# print(qs.query)

					for i in qs:
						item = i.toJSON()
						item['position'] = position
						item['fullname'] = f"{item['apellido']}, {item['nombre']}"
						item['value'] = '{} , {}'.format(i.nombre, i.apellido)
						data.append(item)
						position += 1
					# print(data)
			elif action == 'search_pasoxpc':
				data = []          
				_start = request.POST['start']
				_length = request.POST['length']
				_search = request.POST['search[value]']

				_order = []
				
				for i in range(4):
					_column_order = f'order[{i}][column]'
					# print('Column Order:',_column_order)
					if _column_order in request.POST:					
						_column_number = request.POST[_column_order]
						# print('Column Number:',_column_number)					
						if _column_number == '3': #Hacemos esto por que en el datatable está fullname
							_order.append('apellido')
							_order.append('nombre')
						else:
							_order.append(request.POST[f'columns[{_column_number}][data]'].split(".")[0])
					if f'order[{i}][dir]' in request.POST:
						_dir = request.POST[f'order[{i}][dir]']
						if (_dir=='desc'):
							_order[i] = f"-{_order[i]}"
	
						  
				_where = "'' = %s"
				if len(_search):
					if _search.isnumeric():
						_where = " ci = %s"
					else:
						_search = '%' + _search.replace(' ','%') + '%'
						_where = " upper(nombre||' '|| apellido) LIKE upper(%s)"  
				
				qs = Elector.objects.filter(pasoxpc='S',usu_modificacion=request.user)\
									.extra(where=[_where], params=[_search])\
									.order_by(*_order) 
				total = qs.count()   

				if _start and _length:
					start = int(_start)
					length = int(_length)
					page = math.ceil(start / length) + 1
					per_page = length 

					qs = qs[start:start + length]                    
				
				for i in qs:
					item = i.toJSON()
					# item['position'] = position
					item['fullname'] = f"{item['apellido']}, {item['nombre']}"
					data.append(item)
					# position += 1   
				data = {'data': data,
						'page': page,  # [opcional]
						'per_page': per_page,  # [opcional]
						'recordsTotal': total,
						'recordsFiltered': total, }
			   
				# return JsonResponse(data,safe=False)
			
			elif action == 'edit_pasoxpc':                                
				id = request.POST['id']
				elector = Elector.objects.get(id=id)
				if elector.pasoxpc=='S':
					info =  f"MESA: <b> {elector.mesa} </b> ORDEN: <b> {elector.orden} </b> <br>" 
					info += f"CI: <b> {elector.ci} </b> <br>"
					info += f"{elector.nombre}, {elector.apellido} <br>"
					info += '<b> VOTA EN </b>  <br> ' 
					info += f"{elector.local_votacion} <br> <br>"                    
					info += '<b>=====> YA PASÓ POR PC <===== </b> <br>'              
					data['error'] = info
				else:
					elector.pasoxpc='S'
					elector.save()
					info = f"CI: <b> {elector.ci} </b> <br>"
					info += f"{elector.nombre}, {elector.apellido} <br>"
					info += '<b> VOTA EN </b>  <br> ' 
					info += f"{elector.local_votacion} <br> <br>"
					info += f"MESA: <b> {elector.mesa} </b> ORDEN: <b> {elector.orden} </b>"                
					data['info'] = info
					

			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url'] = reverse_lazy('elector_create')
		context['title'] = 'Carga de Electores Puesto de Control'
		return context

# class CargaDiaDElectorView(ModuleMixin, TemplateView):
#     template_name = 'padron/carga_dia_d/list_carga_dia_d_elector_pc.html'

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         action = request.POST['action']
#         try:
#             if action == 'search_elector':
#                 data = []
#                 # ids = json.loads(request.POST['ids'])
#                 term = request.POST['term']
#                 # search = Elector.objects.exclude(id__in=ids).order_by('apellido','nombre')
#                 if len(term):
#                     term1 = 0
#                     if term.isnumeric():
#                         term1 = term
#                     else:
#                         term = '%' + term.replace(' ','%') + '%'

#                     search = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
#                                             .extra(where=["ci = %s OR upper(nombre||' '|| apellido) LIKE upper(%s)"], params=[term1,term]) \
#                                             .order_by('fullname')[0:10]
				 
#                 for i in search:
#                     item = i.toJSON()
#                     item['value'] = '{} , {}'.format(i.nombre, i.apellido)
#                     data.append(item)
#             elif action == 'create':
#                 with transaction.atomic():
#                     electoresjson = json.loads(request.POST['electores'])
#                     print(electoresjson)
#                     for e in electoresjson:
#                         elector = Elector.objects.get(pk=e['id'])
#                         elector.pasoxpc = 'S'
#                         elector.save()
#             else:
#                 data['error'] = 'No ha ingresado una opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return HttpResponse(json.dumps(data), content_type='application/json')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Carga Día D Puesto de Control'
#         return context
