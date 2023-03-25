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


class CargaDiaDListView(PermissionMixin,FormView):
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
				local_votacion = request.POST['local_votacion']
				mesa = request.POST['mesa']				
				 
				if len(term):
					#Busqueda por Local Votacion, Mesa y Orden (maximo 3 digitos)
					if len(term) <= 3:
						position = 1    
						qs = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
										.filter(distrito=request.user.distrito)\
										.extra(where=["local_votacion_id = %s AND  mesa = %s AND orden =%s"], params=[local_votacion,mesa,term]) \
										.order_by('fullname')[0:10]
					else:
						# Busqueda por Nro. de Cedula y/o Nombre o Apellido
						term1 = 0
						if term.isnumeric():
							term1 = term
						else:
							term = '%' + term.replace(' ','%') + '%'
						position = 1    
						qs = Elector.objects.annotate(fullname=Concat('nombre', Value(' '), 'apellido')) \
										.filter(distrito=request.user.distrito)\
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
			  
				qs = Elector.objects.filter(distrito=request.user.distrito,pasoxmv='S')\
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
		context['form'] = ShearchForm(usuario=self.request.user)
		context['create_url'] = reverse_lazy('elector_create')
		context['title'] = 'Carga de Votos Mesa de Votacion'
		context['title2'] = 'Lista de Electores Mesa de Votación'
		context['distrito'] = self.request.user.distrito.denominacion
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
				if Elector.objects.filter(distrito=self.request.user.distrito,denominacion__iexact=obj):
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
		context['distrito'] = self.request.user.distrito.denominacion
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
		self.monto  = kwargs['monto']
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
				if Elector.objects.filter(distrito=self.request.user.distrito,name__iexact=obj).exclude(id=id):
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
					self.success_url = reverse_lazy('carga_dia_d_list_pc')    
				elif self.opcion == 'edit_mv':
					elector.pasoxmv = self.valor
					self.success_url = reverse_lazy('carga_dia_d_list_mv')    
				elif self.opcion == 'edit_gs':
					elector.pasoxpc = self.valor
					elector.pasoxgs = self.valor
					elector.monto = self.monto
					self.success_url = reverse_lazy('carga_dia_d_list_gs')    
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
		context['distrito'] = self.request.user.distrito.denominacion
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
									 .filter(distrito=request.user.distrito)\
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
				
				qs = Elector.objects.filter(distrito=request.user.distrito,pasoxpc='S',usu_modificacion=request.user)\
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
					elector.pasoxpc = 'S'
					elector.save()

					local_votacion_alerts_class = 'alert alert-danger'

					if elector.local_votacion.id == 1:
						local_votacion_alerts_class = 'alert alert-ligth'
					if elector.local_votacion.id == 2:
						local_votacion_alerts_class = 'alert alert-warning'
					if elector.local_votacion.id == 3:
						local_votacion_alerts_class = 'alert alert-success'
					if elector.local_votacion.id == 4:
						local_votacion_alerts_class = 'alert alert-secondary'
					if elector.local_votacion.id == 5:
						local_votacion_alerts_class = 'alert alert-primary'
					if elector.local_votacion.id == 6:
						local_votacion_alerts_class = 'alert alert-info'
					if elector.local_votacion.id == 7:
						local_votacion_alerts_class = 'alert alert-dark'

					local_votacion_alerts = f'<div class="{local_votacion_alerts_class}" role="alert">\
					{elector.local_votacion}\
					</div>'

					info = f"CI: <b> {elector.ci} </b> <br>"
					info += f"{elector.nombre}, {elector.apellido} <br>"
					info += '<b> VOTA EN </b>  <br> '
					info += f"{local_votacion_alerts}"
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
		context['distrito'] = self.request.user.distrito.denominacion
		return context


class CargaDiaDElectorViewGs(PermissionMixin, FormView):
	# model = Elector
	template_name = 'padron/carga_dia_d/list_carga_dia_d_elector_gs.html'
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
									 .filter(distrito=request.user.distrito)\
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
			elif action == 'search_pasoxgs':
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
				
				qs = Elector.objects.filter(distrito=request.user.distrito,pasoxgs='S',usu_modificacion=request.user)\
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
			
			elif action == 'edit_pasoxgs':                                
				id = request.POST['id']
				monto = request.POST['monto']
				elector = Elector.objects.get(id=id)
				if elector.pasoxgs=='S':
					info =  f"MESA: <b> {elector.mesa} </b> ORDEN: <b> {elector.orden} </b> <br>" 
					info += f"CI: <b> {elector.ci} </b> <br>"
					info += f"{elector.nombre}, {elector.apellido} <br>"
					info += '<b> VOTA EN </b>  <br> ' 
					info += f"{elector.local_votacion} <br> <br>"                    
					info += "<b>=====> YA PASÓ  POR PC <i class='fas fa-dollar-sign'></i> <===== </b> <br>"
					data['error'] = info
				else:
					elector.pasoxpc = 'S'
					elector.pasoxgs = 'S'
					elector.monto = monto
					elector.save()

					local_votacion_alerts_class = 'alert alert-danger'

					if elector.local_votacion.id == 1:
						local_votacion_alerts_class = 'alert alert-ligth'
					if elector.local_votacion.id == 2:
						local_votacion_alerts_class = 'alert alert-warning'
					if elector.local_votacion.id == 3:
						local_votacion_alerts_class = 'alert alert-success'
					if elector.local_votacion.id == 4:
						local_votacion_alerts_class = 'alert alert-secondary'
					if elector.local_votacion.id == 5:
						local_votacion_alerts_class = 'alert alert-primary'
					if elector.local_votacion.id == 6:
						local_votacion_alerts_class = 'alert alert-info'
					if elector.local_votacion.id == 7:
						local_votacion_alerts_class = 'alert alert-dark'

					local_votacion_alerts = f'<div class="{local_votacion_alerts_class}" role="alert">\
					{elector.local_votacion}\
					</div>'

					info = f"CI: <b> {elector.ci} </b> <br>"
					info += f"{elector.nombre}, {elector.apellido} <br>"
					info += '<b> VOTA EN </b>  <br> '
					info += f"{local_votacion_alerts}"
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
		context['title'] = 'Carga de Electores Puesto de Control GS'
		context['distrito'] = self.request.user.distrito.denominacion
		return context
