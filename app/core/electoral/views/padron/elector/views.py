import math
from core.base.models import Parametro
from core.reports.jasperbase import JasperReportBase
from core.electoral.models import Barrio, Ciudad, Manzana, TipoVoto
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
				
				local_votacion = request.POST['local_votacion']
				mesa = request.POST['mesa']				
				seccional = request.POST['seccional']
				operador = request.POST['operador']

				ciudad = request.POST['ciudad']
				barrio = request.POST['barrio']
				manzana = request.POST['manzana']
				tipo_voto = request.POST['tipo_voto']		

				pasoxpc = request.POST['pasoxpc']
				pasoxmv = request.POST['pasoxmv']

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
						if _column_number == '8': #Hacemos esto por que en el datatable edad es un campo calculado
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
				_order.append('id') # Siempre ordenamos por id para evitar problemas con la paginación y manterner un orden consistente aunque se repitan valores en los campos ordenados
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
				if len(local_votacion):
					_where += f" AND electoral_elector.local_votacion_id = '{local_votacion}'"
				if len(operador):
					_where += f" AND electoral_elector.operador_id = '{operador}'"
				if len(mesa):
					_where += f" AND electoral_elector.mesa = '{mesa}'"
				if len(tipo_voto):
					_where += f" AND electoral_elector.tipo_voto_id = '{tipo_voto}'"
				if len(pasoxpc):
					_where += f" AND COALESCE(electoral_elector.pasoxpc,'N') = '{pasoxpc}'"
				if len(pasoxmv):
					_where += f" AND COALESCE(electoral_elector.pasoxmv,'N') = '{pasoxmv}'"

				# if len(pasoxmv):
				# 	_where += f" AND COALESCE(electoral_elector.tipo_voto_id,0) <> 11 \
				# 				 AND COALESCE(electoral_elector.pasoxmv,'N') = '{pasoxmv}'"
				
				qs = Elector.objects.filter(distrito=request.user.distrito)\
									.extra(where=[_where], params=[_search])\
									.order_by(*_order)

				if len(start_date) and len(end_date):
					start_date = datetime.strptime(start_date, '%Y-%m-%d')
					qs = qs.filter(fecha_nacimiento__month=start_date.month,
								   fecha_nacimiento__day__exact=start_date.day)

				total = qs.count()
				# print(qs.query)
				
				if _start and _length:
					start = int(_start)
					length = int(_length)
					page = math.ceil(start / length) + 1
					per_page = length
				
				if _length== '-1':
					qs = qs[start:]
				else:
					qs = qs[start:start + length]

				# position = start + 1
				
				# 1. Obtenemos las descripciones de los parámetros una sola vez
				# Creamos un diccionario: {'VOTO1': 'Elecciones 2018', 'VOTO2': 'Municipales 2021', ...}
				nombres_votos = {p.parametro: p.descripcion for p in Parametro.objects.filter(parametro__in=['VOTO1', 'VOTO2', 'VOTO3', 'VOTO4', 'VOTO5'])}
				data = []

				for i in qs:
					item = i.toJSON()
					
					# Definimos las clases de color para el botón
					# btn-dark es negro, btn-danger-dark es el rojo fuerte que definiremos en CSS
					colores_config = {
						'voto5': 'btn-success',      # Verde
						'voto4': 'btn-warning',      # Amarillo
						'voto3': 'btn-orange',       # Naranja
						'voto2': 'btn-danger',       # Rojizo
						'voto1': 'btn-danger-dark',  # Rojo fuerte
					}
					
					btn_class = 'btn-dark'  # Por defecto: Voto 0 (Negro / Sin historial)
					historial = []

					# AGREGAR ENCABEZADO AL HISTORIAL
					# Usamos una clase o estilo para que parezca un header
					header_html = "<div style='border-bottom: 1px solid #ccc; margin-bottom: 5px; padding-bottom: 3px;'><b>HISTORIAL DE VOTOS</b></div>"
		
					# Buscamos de mayor a menor
					for n in range(5, 0, -1):
						cod_campo = f'voto{n}'
						valor = getattr(i, cod_campo, None)
						
						# Obtenemos la descripción real desde nuestro diccionario (si no existe, usamos el código)
						nombre_eleccion = nombres_votos.get(cod_campo.upper(), cod_campo.upper())

						if valor == 'S':
							# Si es el primer 'S' que encontramos, define el color del botón
							if btn_class == 'btn-dark':
								btn_class = colores_config.get(cod_campo)
							# Añadimos al historial con color VERDE
							historial.append(f"<span style='color: #28a745;'>●</span> <b>{nombre_eleccion}:</b> SI")
							
						elif valor == 'N':
							# Añadimos al historial con color ROJO (pero no afecta al color del botón)
							historial.append(f"<span style='color: #dc3545;'>●</span> <b>{nombre_eleccion}:</b> NO")

					item['btn_class'] = btn_class
					item['tooltip_votos'] = header_html + "<br>".join(historial) if historial else "Sin historial de votos"
					
					data.append(item)

				data = {'data': data,
						'page': page,  # [opcional]
						'per_page': per_page,  # [opcional]
						'recordsTotal': total,
						'recordsFiltered': total, }
				
			elif action == 'search_select2':
				field = request.POST.get('field')
				term = request.POST.get('term', '')
				results = []
				
				if field == 'ciudad':
					# Buscamos por denominación O por ID exacto (si es numérico)
					query = Q(denominacion__icontains=term)
					if term.isdigit():
						query |= Q(id=term)
						
					qs = Ciudad.objects.filter(query)[:10]
					# Usamos str(x) para que el texto mostrado sea el que define tu __str__ en el modelo
					results = [{'id': x.id, 'text': str(x)} for x in qs]

				elif field == 'barrio':
					# Buscamos por denominación O por ID exacto (si es numérico)
					query = Q(denominacion__icontains=term)
					if term.isdigit():
						query |= Q(id=term)
						
					qs = Barrio.objects.filter(query)[:10]
					# Usamos str(x) para que el texto mostrado sea el que define tu __str__ en el modelo
					results = [{'id': x.id, 'text': str(x)} for x in qs]
					
				elif field == 'manzana':
					barrio_id = request.POST.get('barrio_id')
					
					# Buscamos por denominación O por el campo 'cod' (o 'codigo')
					query = Q(denominacion__icontains=term)
					if term: # Si el término no está vacío
						# Cambia 'cod' por el nombre exacto de tu campo en el modelo Manzana
						query |= Q(cod__icontains=term) 
						if term.isdigit():
							query |= Q(id=term)

					qs = Manzana.objects.filter(query)
					
					if barrio_id:
						qs = qs.filter(barrio_id=barrio_id)
						
					results = [{'id': x.id, 'text': str(x)} for x in qs[:10]]

				# No olvides mantener aquí tu bloque de tipo_voto
				elif field == 'tipo_voto':
					query = Q(cod__icontains=term)
					if term.isdigit():
						query |= Q(id=term)
					qs = TipoVoto.objects.filter(query,activo__exact=True)[:15]
					results = [{'id': x.id, 'text': str(x)} for x in qs]
					
				return JsonResponse(results, safe=False)
			
			elif action == 'quick_update':
				try:
					elector = Elector.objects.get(pk=request.POST.get('id'))
					field = request.POST.get('field')
					val = request.POST.get('value')
					print(val)
					
					if field == 'ciudad':
						elector.ciudad_id = val if val else None

					elif field == 'barrio':
						# Si cambia el barrio, el ID de la manzana DEBE ser None
						elector.barrio_id = val if val else None
						elector.manzana_id = None 
						
					elif field == 'manzana':
						elector.manzana_id = val if val else None
						
					elif field == 'tipo_voto':
						elector.tipo_voto_id = val if val else None
					
					elif field == 'nro_casa':
						elector.nro_casa = val if val else None
						
					elector.save()
					return JsonResponse({'status': 'ok'})
				except Exception as e:
					return JsonResponse({'error': str(e)})
			else:
				data['error'] = 'No ha ingresado una opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['create_url'] = reverse_lazy('elector_create')
		context['form'] = ShearchForm(usuario=self.request.user)
		context['title'] = 'Listado de Electores'
		context['distrito'] = self.request.user.distrito.denominacion
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
				data = [{'id': '', 'text': '(Todos)'}]	
				barrio_list = None	
				# print(request.POST)				
				if 'id' in request.POST:
					barrio_list = [request.POST['id'] if 'id' in request.POST else None]

				elif 'id[]' in request.POST:
					barrio_list = request.POST.getlist('id[]') if 'id[]' in request.POST else None
	
				if barrio_list:
					# qs = Manzana.objects.filter(barrio_id__in=barrio_list)
					# print(qs.query)
					for i in Manzana.objects.filter(barrio_id__in=barrio_list):			
						data.append({'id': i.id, 'text': str(i), 'data': i.barrio.toJSON()})
				# print(data)
			
			elif action == 'search_mesa_id':
				data = [{'id': '', 'text': '(Todos)'}]				
				local_votacion_list = [request.POST['id'] if 'id' in request.POST else None]
				if local_votacion_list is None:
					local_votacion_list = [request.POST.getlist('id[]') if 'id[]' in request.POST else '']	
				for i in Elector.objects.values('mesa')\
										.filter(distrito=self.request.user.distrito,local_votacion_id__in=local_votacion_list)\
										.extra(select={'int_mesa':'CAST(mesa AS INTEGER)'})\
										.distinct().order_by('int_mesa'):			
					data.append({'id': i['mesa'], 'text': i['mesa'], 'data': i})
				
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
				form = ElectorForm(usuario=self.request.user,instance=elector)
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
