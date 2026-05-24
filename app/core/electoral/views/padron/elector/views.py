# 1. Standard Library imports
import json
import math
from datetime import date, datetime

# 2. Django imports
from django.contrib.auth.decorators import permission_required
from django.db.models import IntegerField, Q
from django.db.models.functions import Cast
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import FormView

# 3. Local Apps imports (Core / Base / Electoral / Reports)
from core.base.models import Parametro
from core.electoral.forms import Elector, ElectorForm, ShearchForm
from core.electoral.models import Barrio, Ciudad, LocalVotacion, Manzana, TipoVoto
from core.reports.forms import FormFilterGenerarPDFMesa, ReportForm
from core.reports.jasperbase import JasperReportBase
from core.security.mixins import PermissionMixin


class ElectorListView(PermissionMixin, FormView):
    # model = Elector
    template_name = "padron/elector/list.html"
    permission_required = "view_elector"
    form_class = ShearchForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST["action"]
        # print(request.POST)
        try:
            # if action == "search":
            #     data = []
            #     term = request.POST["term"]
            #     start_date = request.POST["start_date"]
            #     end_date = request.POST["end_date"]

            #     local_votacion = request.POST["local_votacion"]
            #     mesa = request.POST["mesa"]
            #     seccional = request.POST["seccional"]
            #     operador = request.POST["operador"]

            #     ciudad = request.POST["ciudad"]
            #     barrio = request.POST["barrio"]
            #     manzana = request.POST["manzana"]
            #     tipo_voto = request.POST["tipo_voto"]

            #     pasoxpc = request.POST["pasoxpc"]
            #     pasoxmv = request.POST["pasoxmv"]

            #     _start = request.POST["start"]
            #     _length = request.POST["length"]
            #     _search = request.POST["search[value]"]

            #     # _order = ['barrio','manzana','nro_casa'] debe enviarse ya el orden desde el datatable para default
            #     _order = []
            #     # print(request.POST)
            #     # range(start, stop, step)
            #     for i in range(9):
            #         _column_order = f"order[{i}][column]"
            #         # print('Column Order:',_column_order)
            #         if _column_order in request.POST:
            #             _column_number = request.POST[_column_order]
            #             # print('Column Number:',_column_number)
            #             if (
            #                 _column_number == "10"
            #             ):  # Hacemos esto por que en el datatable edad es un campo calculado
            #                 _order.append("fecha_nacimiento")
            #             elif (
            #                 _column_number == "4"
            #             ):  # Hacemos esto por que en el datatable fullname es un campo calculado
            #                 _order.append("apellido")
            #                 _order.append("nombre")
            #             else:
            #                 _order.append(
            #                     request.POST[f"columns[{_column_number}][data]"].split(
            #                         "."
            #                     )[0]
            #                 )
            #         if f"order[{i}][dir]" in request.POST:
            #             _dir = request.POST[f"order[{i}][dir]"]
            #             if _dir == "desc":
            #                 _order[i] = f"-{_order[i]}"
            #     # print('Order:', _order)
            #     _order.append(
            #         "id"
            #     )  # Siempre ordenamos por id para evitar problemas con la paginación y manterner un orden consistente aunque se repitan valores en los campos ordenados
            #     if len(term):
            #         _search = term

            #     _where = "'' = %s"
            #     if len(_search):
            #         if _search.isnumeric():
            #             _where = " ci = %s"
            #         else:
            #             _search = "%" + _search.replace(" ", "%") + "%"
            #             _where = " upper(nombre||' '|| apellido) LIKE upper(%s)"

            #     if len(ciudad):
            #         _where += f" AND electoral_elector.ciudad_id = '{ciudad}'"
            #     if len(seccional):
            #         _where += f" AND electoral_elector.seccional_id = '{seccional}'"
            #     if len(barrio):
            #         _where += f" AND electoral_elector.barrio_id = '{barrio}'"
            #     if len(manzana):
            #         _where += f" AND electoral_elector.manzana_id = '{manzana}'"
            #     if len(local_votacion):
            #         _where += (
            #             f" AND electoral_elector.local_votacion_id = '{local_votacion}'"
            #         )
            #     if len(operador):
            #         _where += f" AND electoral_elector.operador_id = '{operador}'"
            #     if len(mesa):
            #         _where += f" AND electoral_elector.mesa = '{mesa}'"
            #     if len(tipo_voto):
            #         _where += f" AND electoral_elector.tipo_voto_id = '{tipo_voto}'"
            #     if len(pasoxpc):
            #         _where += (
            #             f" AND COALESCE(electoral_elector.pasoxpc,'N') = '{pasoxpc}'"
            #         )
            #     if len(pasoxmv):
            #         _where += (
            #             f" AND COALESCE(electoral_elector.pasoxmv,'N') = '{pasoxmv}'"
            #         )

            #     # if len(pasoxmv):
            #     # 	_where += f" AND COALESCE(electoral_elector.tipo_voto_id,0) <> 11 \
            #     # 				 AND COALESCE(electoral_elector.pasoxmv,'N') = '{pasoxmv}'"

            #     qs = (
            #         Elector.objects.filter(distrito=request.user.distrito)
            #         .extra(where=[_where], params=[_search])
            #         .order_by(*_order)
            #     )

            #     if len(start_date) and len(end_date):
            #         start_date = datetime.strptime(start_date, "%Y-%m-%d")
            #         qs = qs.filter(
            #             fecha_nacimiento__month=start_date.month,
            #             fecha_nacimiento__day__exact=start_date.day,
            #         )

            #     total = qs.count()
            #     # print(qs.query)

            #     if _start and _length:
            #         start = int(_start)
            #         length = int(_length)
            #         page = math.ceil(start / length) + 1
            #         per_page = length

            #     if _length == "-1":
            #         qs = qs[start:]
            #     else:
            #         qs = qs[start : start + length]

            #     # position = start + 1

            #     # 1. Obtenemos las descripciones de los parámetros una sola vez
            #     # Creamos un diccionario: {'VOTO1': 'Elecciones 2018', 'VOTO2': 'Municipales 2021', ...}
            #     nombres_votos = {
            #         p.parametro: p.descripcion
            #         for p in Parametro.objects.filter(
            #             parametro__in=["VOTO1", "VOTO2", "VOTO3", "VOTO4", "VOTO5"]
            #         )
            #     }
            #     data = []

            #     for i in qs:
            #         item = i.toJSON()

            #         # Definimos las clases de color para el botón
            #         # btn-dark es negro, btn-danger-dark es el rojo fuerte que definiremos en CSS
            #         colores_config = {
            #             "voto5": "btn-success",  # Verde
            #             "voto4": "btn-warning",  # Amarillo
            #             "voto3": "btn-orange",  # Naranja
            #             "voto2": "btn-danger",  # Rojizo
            #             "voto1": "btn-danger-dark",  # Rojo fuerte
            #         }

            #         btn_class = (
            #             "btn-dark"  # Por defecto: Voto 0 (Negro / Sin historial)
            #         )
            #         historial = []

            #         # AGREGAR ENCABEZADO AL HISTORIAL
            #         # Usamos una clase o estilo para que parezca un header
            #         header_html = "<div style='border-bottom: 1px solid #ccc; margin-bottom: 5px; padding-bottom: 3px;'><b>HISTORIAL DE VOTOS</b></div>"

            #         # Buscamos de mayor a menor
            #         for n in range(5, 0, -1):
            #             cod_campo = f"voto{n}"
            #             valor = getattr(i, cod_campo, None)

            #             # Obtenemos la descripción real desde nuestro diccionario (si no existe, usamos el código)
            #             nombre_eleccion = nombres_votos.get(
            #                 cod_campo.upper(), cod_campo.upper()
            #             )

            #             if valor == "S":
            #                 # Si es el primer 'S' que encontramos, define el color del botón
            #                 if btn_class == "btn-dark":
            #                     btn_class = colores_config.get(cod_campo)
            #                 # Añadimos al historial con color VERDE
            #                 historial.append(
            #                     f"<span style='color: #28a745;'>●</span> <b>{nombre_eleccion}:</b> SI"
            #                 )

            #             elif valor == "N":
            #                 # Añadimos al historial con color ROJO (pero no afecta al color del botón)
            #                 historial.append(
            #                     f"<span style='color: #dc3545;'>●</span> <b>{nombre_eleccion}:</b> NO"
            #                 )

            #         item["btn_class"] = btn_class
            #         item["tooltip_votos"] = (
            #             header_html + "<br>".join(historial)
            #             if historial
            #             else "Sin historial de votos"
            #         )

            #         data.append(item)

            #     data = {
            #         "data": data,
            #         "page": page,  # [opcional]
            #         "per_page": per_page,  # [opcional]
            #         "recordsTotal": total,
            #         "recordsFiltered": total,
            #     }

            if action == "search":
                data = []
                # 1. Captura de parámetros
                term = request.POST.get("term", "")
                start_date = request.POST.get("start_date", "")
                end_date = request.POST.get("end_date", "")

                # Parámetros de filtrado
                filtros = {
                    "local_votacion_id": request.POST.get("local_votacion"),
                    "mesa": request.POST.get("mesa"),
                    "seccional_id": request.POST.get("seccional"),
                    "operador_id": request.POST.get("operador"),
                    "ciudad_id": request.POST.get("ciudad"),
                    "barrio_id": request.POST.get("barrio"),
                    "manzana_id": request.POST.get("manzana"),
                    "tipo_voto_id": request.POST.get("tipo_voto"),
                    "pasoxpc": request.POST.get("pasoxpc"),
                    "pasoxmv": request.POST.get("pasoxmv"),
                }

                _start = request.POST.get("start")
                _length = request.POST.get("length")
                _search = request.POST.get("search[value]", "")

                # 2. Lógica de Ordenamiento con Mejoras para Mesa y Orden
                _order = []
                annotation_kwargs = {}

                # Iteramos sobre el orden enviado por DataTables
                for i in range(12):  # Aumentado el rango para cubrir todas tus columnas
                    col_idx_key = f"order[{i}][column]"
                    if col_idx_key in request.POST:
                        _column_number = request.POST[col_idx_key]
                        _dir = request.POST.get(f"order[{i}][dir]", "asc")
                        prefix = "-" if _dir == "desc" else ""

                        # Casos especiales de ordenamiento
                        if _column_number == "10":  # Edad (calculado)
                            _order.append(f"{prefix}fecha_nacimiento")
                        elif _column_number == "4":  # Fullname (calculado)
                            _order.append(f"{prefix}apellido")
                            _order.append(f"{prefix}nombre")
                        elif _column_number == "1":  # MESA (Forzar numérico)
                            annotation_kwargs["mesa_int"] = Cast("mesa", IntegerField())
                            _order.append(f"{prefix}mesa_int")
                        elif _column_number == "2":  # ORDEN (Forzar numérico)
                            annotation_kwargs["orden_int"] = Cast(
                                "orden", IntegerField()
                            )
                            _order.append(f"{prefix}orden_int")
                        else:
                            # Obtener el nombre del campo desde la config del datatable (columns[i][data])
                            data_field = request.POST.get(
                                f"columns[{_column_number}][data]", "id"
                            )
                            field_name = data_field.split(".")[0]
                            _order.append(f"{prefix}{field_name}")

                # 3. ORDEN POR DEFECTO (Si DataTables no envía un orden específico)
                if not _order:
                    # Forzamos las anotaciones para el orden por defecto
                    annotation_kwargs["mesa_int"] = Cast("mesa", IntegerField())
                    annotation_kwargs["orden_int"] = Cast("orden", IntegerField())

                    # Definimos la jerarquía: Local -> Mesa -> Orden
                    _order = ["local_votacion__nombre", "mesa_int", "orden_int", "id"]
                else:
                    # Si ya hay un orden, añadimos ID al final para consistencia
                    if "id" not in [o.replace("-", "") for o in _order]:
                        _order.append("id")

                # 3. Construcción del QuerySet base
                qs = Elector.objects.filter(distrito=request.user.distrito)

                # 4. Aplicar Búsqueda General (Nombre o CI)
                search_val = term if term else _search
                if search_val:
                    if search_val.isnumeric():
                        qs = qs.filter(ci__icontains=search_val)
                    else:
                        # Búsqueda por nombre completo
                        parts = search_val.split()
                        q_obj = Q()
                        for part in parts:
                            q_obj &= Q(nombre__icontains=part) | Q(
                                apellido__icontains=part
                            )
                        qs = qs.filter(q_obj)

                # 5. Aplicar Filtros Específicos (Evitando SQL dinámico manual)
                for campo, valor in filtros.items():
                    if valor and valor != "":
                        if campo in ["pasoxpc", "pasoxmv"]:
                            # Manejo de COALESCE para campos de paso
                            kwargs = {f"{campo}": valor}
                            qs = qs.filter(**kwargs)
                        else:
                            kwargs = {f"{campo}": valor}
                            qs = qs.filter(**kwargs)

                # Filtro por fecha de nacimiento (aniversarios)
                if start_date and end_date:
                    try:
                        dt = datetime.strptime(start_date, "%Y-%m-%d")
                        qs = qs.filter(
                            fecha_nacimiento__month=dt.month,
                            fecha_nacimiento__day=dt.day,
                        )
                    except ValueError:
                        pass

                # 6. Aplicar Anotaciones de ordenamiento y Orden final
                if annotation_kwargs:
                    qs = qs.annotate(**annotation_kwargs)

                qs = qs.order_by(*_order)

                # 7. Paginación
                total = qs.count()
                start = int(_start) if _start else 0
                length = int(_length) if _length else 10

                if length == -1:
                    qs = qs[start:]
                else:
                    qs = qs[start : start + length]

                # 8. Preparación de datos (JSON)
                nombres_votos = {
                    p.parametro: p.descripcion
                    for p in Parametro.objects.filter(
                        parametro__in=["VOTO1", "VOTO2", "VOTO3", "VOTO4", "VOTO5"]
                    )
                }

                final_data = []
                colores_config = {
                    "voto5": "btn-success",
                    "voto4": "btn-warning",
                    "voto3": "btn-orange",
                    "voto2": "btn-danger",
                    "voto1": "btn-danger-dark",
                }

                for i in qs:
                    item = i.toJSON()
                    btn_class = "btn-dark"
                    historial = []
                    header_html = "<div style='border-bottom: 1px solid #ccc; margin-bottom: 5px;'><b>HISTORIAL DE VOTOS</b></div>"

                    for n in range(5, 0, -1):
                        cod_campo = f"voto{n}"
                        valor = getattr(i, cod_campo, None)
                        nombre_eleccion = nombres_votos.get(
                            cod_campo.upper(), cod_campo.upper()
                        )

                        if valor == "S":
                            if btn_class == "btn-dark":
                                btn_class = colores_config.get(cod_campo)
                            historial.append(
                                f"<span style='color: #28a745;'>●</span> <b>{nombre_eleccion}:</b> SI"
                            )
                        elif valor == "N":
                            historial.append(
                                f"<span style='color: #dc3545;'>●</span> <b>{nombre_eleccion}:</b> NO"
                            )

                    item["btn_class"] = btn_class
                    item["tooltip_votos"] = (
                        header_html + "<br>".join(historial)
                        if historial
                        else "Sin historial"
                    )
                    final_data.append(item)

                # 9. Respuesta Final
                return JsonResponse(
                    {
                        "data": final_data,
                        "recordsTotal": total,
                        "recordsFiltered": total,
                    },
                    safe=False,
                )

            elif action == "search_select2":
                field = request.POST.get("field")
                term = request.POST.get("term", "")
                results = []

                if field == "ciudad":
                    # Buscamos por denominación O por ID exacto (si es numérico)
                    query = Q(denominacion__icontains=term)
                    if term.isdigit():
                        query |= Q(id=term)

                    qs = Ciudad.objects.filter(query)[:10]
                    # Usamos str(x) para que el texto mostrado sea el que define tu __str__ en el modelo
                    results = [{"id": x.id, "text": str(x)} for x in qs]

                elif field == "barrio":
                    # Buscamos por denominación O por ID exacto (si es numérico)
                    query = Q(denominacion__icontains=term)
                    if term.isdigit():
                        query |= Q(id=term)

                    qs = Barrio.objects.filter(query)[:10]
                    # Usamos str(x) para que el texto mostrado sea el que define tu __str__ en el modelo
                    results = [{"id": x.id, "text": str(x)} for x in qs]

                elif field == "manzana":
                    barrio_id = request.POST.get("barrio_id")

                    # Buscamos por denominación O por el campo 'cod' (o 'codigo')
                    query = Q(denominacion__icontains=term)
                    if term:  # Si el término no está vacío
                        # Cambia 'cod' por el nombre exacto de tu campo en el modelo Manzana
                        query |= Q(cod__icontains=term)
                        if term.isdigit():
                            query |= Q(id=term)

                    qs = Manzana.objects.filter(query)

                    if barrio_id:
                        qs = qs.filter(barrio_id=barrio_id)

                    results = [{"id": x.id, "text": str(x)} for x in qs[:10]]

                # No olvides mantener aquí tu bloque de tipo_voto
                elif field == "tipo_voto":
                    query = Q(cod__icontains=term)
                    if term.isdigit():
                        query |= Q(id=term)
                    qs = TipoVoto.objects.filter(query, activo__exact=True)[:15]
                    results = [{"id": x.id, "text": str(x)} for x in qs]

                return JsonResponse(results, safe=False)

            elif action == "quick_update":
                try:
                    elector = Elector.objects.get(pk=request.POST.get("id"))
                    field = request.POST.get("field")
                    val = request.POST.get("value")
                    print(val)

                    if field == "ciudad":
                        elector.ciudad_id = val if val else None

                    elif field == "barrio":
                        # Si cambia el barrio, el ID de la manzana DEBE ser None
                        elector.barrio_id = val if val else None
                        elector.manzana_id = None

                    elif field == "manzana":
                        elector.manzana_id = val if val else None

                    elif field == "tipo_voto":
                        elector.tipo_voto_id = val if val else None

                    elif field == "nro_casa":
                        elector.nro_casa = val if val else None

                    elector.save()
                    return JsonResponse({"status": "ok"})
                except Exception as e:
                    return JsonResponse({"error": str(e)})
            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_url"] = reverse_lazy("elector_create")
        context["form"] = ShearchForm(usuario=self.request.user)
        context["title"] = "Listado de Electores"
        context["distrito"] = self.request.user.distrito.denominacion
        return context


class ElectorCreateView(PermissionMixin, CreateView):
    model = Elector
    template_name = "padron/elector/create.html"
    form_class = ElectorForm
    success_url = reverse_lazy("elector_list")
    permission_required = "add_elector"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {"valid": True}
        try:

            type = self.request.POST["type"]
            obj = self.request.POST["obj"].strip()
            if type == "denominacion":
                if Elector.objects.filter(denominacion__iexact=obj):
                    data["valid"] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST["action"]
        try:
            if action == "add":
                data = self.get_form().save()
            elif action == "validate_data":
                return self.validate_data()

            elif action == "search_manzana_id":
                data = [{"id": "", "text": "(Todos)"}]
                barrio_list = None
                # print(request.POST)
                if "id" in request.POST:
                    barrio_list = [request.POST["id"] if "id" in request.POST else None]

                elif "id[]" in request.POST:
                    barrio_list = (
                        request.POST.getlist("id[]") if "id[]" in request.POST else None
                    )

                if barrio_list:
                    # qs = Manzana.objects.filter(barrio_id__in=barrio_list)
                    # print(qs.query)
                    for i in Manzana.objects.filter(barrio_id__in=barrio_list):
                        data.append(
                            {"id": i.id, "text": str(i), "data": i.barrio.toJSON()}
                        )
                # print(data)

            elif action == "search_mesa_id":
                data = [{"id": "", "text": "(Todos)"}]
                local_votacion_list = [
                    request.POST["id"] if "id" in request.POST else None
                ]
                if local_votacion_list is None:
                    local_votacion_list = [
                        request.POST.getlist("id[]") if "id[]" in request.POST else ""
                    ]
                for i in (
                    Elector.objects.values("mesa")
                    .filter(
                        distrito=self.request.user.distrito,
                        local_votacion_id__in=local_votacion_list,
                    )
                    .extra(select={"int_mesa": "CAST(mesa AS INTEGER)"})
                    .distinct()
                    .order_by("int_mesa")
                ):
                    data.append(
                        {"id": i["mesa"], "text": f"Mesa N° {i['mesa']}", "data": i}
                    )

            else:
                data["error"] = "No ha seleccionado ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["list_url"] = self.success_url
        context["title"] = "Nuevo registro de un elector"
        context["action"] = "add"
        return context


class ElectorUpdateView(PermissionMixin, UpdateView):
    model = Elector
    template_name = "padron/elector/create.html"
    form_class = ElectorForm
    success_url = reverse_lazy("elector_list")
    permission_required = "change_elector"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def validate_data(self):
        data = {"valid": True}
        try:
            type = self.request.POST["type"]
            obj = self.request.POST["obj"].strip()
            id = self.get_object().id
            if type == "denominacion":
                if Elector.objects.filter(name__iexact=obj).exclude(id=id):
                    data["valid"] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST["action"]
        try:
            if action == "edit":
                data = self.get_form().save()
            elif action == "validate_data":
                return self.validate_data()
            elif action == "search_manzana_id":
                data = [{"id": "", "text": "------------"}]
                for i in Manzana.objects.filter(barrio_id=request.POST["id"]):
                    data.append(
                        {"id": i.id, "text": i.denominacion, "data": i.barrio.toJSON()}
                    )
            else:
                data["error"] = "No ha seleccionado ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    # Este usamos para el modal
    def get(self, request, *args, **kwargs):
        data = {}
        try:
            if request.user.has_perm("electoral.change_elector"):
                pk = kwargs["pk"]
                elector = get_object_or_404(Elector, pk=pk)
                form = ElectorForm(usuario=self.request.user, instance=elector)
                context = self.get_context_data()
                context["form"] = form
                self.template_name = "padron/elector/create_modal.html"
                context["action_url"] = reverse_lazy(
                    "elector_update", kwargs={"pk": pk}
                )
                data["html_form"] = render_to_string(
                    self.template_name, context, request=request
                )
            else:
                data["error"] = "No tiene permisos para editar"

        except Exception as e:
            data["error"] = str(e)
        # print(data['html_form'])
        return HttpResponse(json.dumps(data), content_type="application/json")
        # return  JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["list_url"] = self.success_url
        context["title"] = "Edición de un elector"
        context["action"] = "edit"
        return context


class ElectorDeleteView(PermissionMixin, DeleteView):
    model = Elector
    template_name = "padron/elector/delete.html"
    success_url = reverse_lazy("elector_list")
    permission_required = "delete_elector"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Notificación de eliminación"
        context["list_url"] = self.success_url
        return context


def test_reporte(request):
    # debemos obtener nuestro objeto classroom haciendo la consulta a la base de datos
    report = JasperReportBase()
    report.report_name = "rpt_001"
    return report.render_to_response()


class RegistroVotoRapidoView(FormView):
    template_name = "padron/elector/registro_voto_filtro_datatables.html"
    form_class = FormFilterGenerarPDFMesa

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action == "generate_grid":
            local_id = request.POST.get("local_votacion")
            mesa_num = request.POST.get("mesa")

            # Buscamos los electores de la mesa ordenada
            electores = Elector.objects.filter(
                local_votacion_id=local_id, mesa=mesa_num
            ).order_by(Cast("orden", IntegerField()))

            columnas = 20
            lista_electores = list(electores)

            # Armamos la matriz plana estructurada en filas con nombres de columnas
            matriz_json = []
            for i in range(0, len(lista_electores), columnas):
                bloque = lista_electores[i : i + columnas]
                fila_dict = {}

                for idx in range(columnas):
                    if idx < len(bloque) and bloque[idx] is not None:
                        elector = bloque[idx]
                        fila_dict[f"col_{idx}"] = {
                            "id": elector.id,
                            "orden": elector.orden,
                            "pasoxmv": True if elector.pasoxmv == "S" else False,
                            "elector": elector.get_fullname(),
                        }
                    else:
                        fila_dict[f"col_{idx}"] = None

                matriz_json.append(fila_dict)

            # Le respondemos directo al AJAX de DataTables
            return JsonResponse({"matriz": matriz_json}, safe=False)

        # Comportamiento por defecto
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(usuario=self.request.user)
        context["title"] = "Carga Rápida de Votos por Mesa"
        context["action"] = "generate_grid"
        return context


@csrf_exempt  # O usá el middleware normal ya que pasamos el X-CSRFToken en el header
def quick_update_voto_endpoint(request):
    if request.method == "POST":
        try:
            # Al venir de un fetch con JSON, cargamos el body así:
            data = json.loads(request.body)
            elector_id = data.get("elector_id")

            elector = Elector.objects.get(id=elector_id)

            # Invertimos el estado del campo progreso (pasoxmv)
            nuevo_estado_char = "N" if elector.pasoxmv == "S" else "S"
            # Guardamos ÚNICAMENTE este campo de forma aislada
            Elector.objects.filter(id=elector_id).update(pasoxmv=nuevo_estado_char)

            return JsonResponse(
                # Retornamos al JS un booleano (True/False) para que pinte el botón fácil
                {"success": True, "nuevo_estado": (nuevo_estado_char == "S")}
            )
        except Elector.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Elector no encontrado"}, status=404
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)


class RegistroVotoMovilView(FormView):
    template_name = "padron/elector/registro_voto_movil.html"
    form_class = FormFilterGenerarPDFMesa

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action == "get_elector_info":
            local_id = request.POST.get("local_votacion")
            mesa_num = request.POST.get("mesa")
            orden_num = request.POST.get("orden")

            try:
                # Buscamos exactamente el elector por su número de orden y mesa
                elector = Elector.objects.get(
                    local_votacion_id=local_id, mesa=mesa_num, orden=orden_num
                )

                return JsonResponse(
                    {
                        "success": True,
                        "elector": {
                            "id": elector.id,
                            "nombre": f"{elector.apellido}, {elector.nombre}".upper(),
                            "ci": f"{elector.ci:,}".replace(",", "."),
                            "pasoxmv": (elector.pasoxmv == "S"),
                        },
                    }
                )
            except Elector.DoesNotExist:
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"El N° de orden {orden_num} no existe para esta mesa.",
                    }
                )
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})

        # Conservamos la acción anterior si se llega a requerir
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(usuario=self.request.user)
        context["title"] = "Control Móvil de Votos (Veedores)"
        context["action"] = "generate_grid"
        return context
