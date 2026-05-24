import json
from django.template.loader import render_to_string
from core.electoral.models import Elector, LocalVotacion
from core.reports.forms import (
    FormFilterGenerarPDFMesa,
    ReportForm,
)
from django.db.models import Max, IntegerField
from django.db.models.functions import Cast
from core.reports.jasperbase import JasperReportBase
from core.security.mixins import ModuleMixin
from core.security.models import Module
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import IntegerField, Max
from django.conf import settings
from core.electoral.models import Elector

try:
    from weasyprint import HTML
except ImportError:
    HTML = None

"""Reporte de Barrios y Manzanas con Codigo"""


# class RptElectoral000ReportView(ModuleMixin, FormView):
#     template_name = "electoral/reports/rpt_electoral000.html"
#     form_class = ReportForm

#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         action = request.POST["action"]
#         data = {}
#         try:
#             if action == "search_report":
#                 data = []
#                 print(request.POST)
#                 seccional = (
#                     request.POST.getlist("seccional[]")
#                     if "seccional[]" in request.POST
#                     else None
#                 )
#                 seccional = seccional if seccional != [""] else None
#                 barrio = (
#                     request.POST.getlist("barrio[]")
#                     if "barrio[]" in request.POST
#                     else None
#                 )
#                 barrio = barrio if barrio != [""] else None
#                 manzana = (
#                     request.POST.getlist("manzana[]")
#                     if "manzana[]" in request.POST
#                     else None
#                 )
#                 manzana = manzana if manzana != [""] else None
#                 # end_date = request.POST['end_date']
#                 _where = "1=1"

#                 if seccional:
#                     _where += f" AND electoral_elector.seccional_id IN {seccional}"
#                 if barrio:
#                     _where += f" AND electoral_elector.barrio_id IN {barrio}"
#                 if manzana:
#                     _where += f" AND electoral_elector.manzana_id IN {manzana}"
#                 _where = _where.replace("[", "(").replace("]", ")")
#                 print(_where)
#                 qs = (
#                     Elector.objects.values(
#                         "barrio__id",
#                         "barrio__denominacion",
#                         "manzana__cod",
#                         "manzana__denominacion",
#                     )
#                     .filter(distrito=self.request.user.distrito)
#                     .extra(
#                         select={
#                             "barrio__cod": "CAST (electoral_elector.barrio_id AS INTEGER)"
#                         }
#                     )
#                     .annotate(cant_elector=Count(True))
#                     .extra(where=[_where])
#                     .order_by("barrio__cod", "manzana__cod")
#                 )
#                 for i in qs:
#                     item = {
#                         "barrio": f"({i['barrio__id']}) - {i['barrio__denominacion']}",
#                         "manzana": f"({i['barrio__id']} / {i['manzana__cod']}) - {i['manzana__denominacion']}",
#                         "cant_elector": i["cant_elector"],
#                     }
#                     data.append(item)
#                 # print(data)
#             else:
#                 data["error"] = "No ha ingresado una opción"
#         except Exception as e:
#             data["error"] = str(e)
#         return HttpResponse(json.dumps(data), content_type="application/json")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["form"] = ReportForm(usuario=self.request.user)
#         context["title"] = "Reporte de Barrios y Manzanas"
#         return context


class RptElectoral000ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_electoral000.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        data = {}

        try:
            # --- ACCIÓN 1: BÚSQUEDA TRADICIONAL (CORREGIDA SIN SQL INJECTION) ---
            if action == "search_report":
                data = []

                # Extraer listas limpias
                seccional = [x for x in request.POST.getlist("seccional[]") if x != ""]
                barrio = [x for x in request.POST.getlist("barrio[]") if x != ""]
                manzana = [x for x in request.POST.getlist("manzana[]") if x != ""]

                # Construcción segura del QuerySet usando el ORM nativo de Django
                filters = {"distrito": self.request.user.distrito}
                if seccional:
                    filters["seccional_id__in"] = seccional
                if barrio:
                    filters["barrio_id__in"] = barrio
                if manzana:
                    filters["manzana_id__in"] = manzana

                qs = (
                    Elector.objects.filter(**filters)
                    .values(
                        "barrio__id",
                        "barrio__denominacion",
                        "manzana__cod",
                        "manzana__denominacion",
                        "barrio_id",  # Reemplaza el CAST manual usando el ID directo de la relación
                    )
                    .annotate(
                        cant_elector=Count("id")
                    )  # Count sobre la PK para mayor precisión
                    .order_by("barrio_id", "manzana__cod")
                )

                for i in qs:
                    item = {
                        "barrio": f"({i['barrio__id']}) - {i['barrio__denominacion']}",
                        "manzana": f"({i['barrio__id']} / {i['manzana__cod']}) - {i['manzana__denominacion']}",
                        "cant_elector": i["cant_elector"],
                    }
                    data.append(item)
                return HttpResponse(json.dumps(data), content_type="application/json")

            # --- NUEVA ACCIÓN 2: GENERAR EL REPORTE PDF CON WEASYPRINT ---
            elif action == "generate_pdf":
                # Capturamos los campos del formulario
                local_id = request.POST.get("local_votacion_id")
                mesa_num = request.POST.get("mesa")

                if not local_id:
                    return HttpResponse(
                        "Error: El ID del Local de Votación es requerido.", status=400
                    )

                # Determinamos la lista de mesas (Específica o todas las del local)
                if mesa_num and mesa_num.strip():
                    mesas_lista = [int(mesa_num)]
                else:
                    mesas_lista = (
                        Elector.objects.filter(local_votacion_id=local_id)
                        .values_list("mesa", flat=True)
                        .distinct()
                        .order_by("mesa")
                    )

                mesas_data = []
                columnas = 20

                # Armamos las matrices dinámicas por cada mesa encontrada
                for m in mesas_lista:
                    datos_mesa = Elector.objects.filter(
                        local_votacion_id=local_id, mesa=m
                    ).aggregate(max_orden=Max("orden"))

                    max_orden = datos_mesa["max_orden"] or 0

                    matriz_ordenes = []
                    fila_actual = []

                    for i in range(1, max_orden + 1):
                        fila_actual.append(i)
                        if len(fila_actual) == columnas:
                            matriz_ordenes.append(fila_actual)
                            fila_actual = []

                    if fila_actual:
                        while len(fila_actual) < columnas:
                            fila_actual.append(None)
                        matriz_ordenes.append(fila_actual)

                    # Ajuste dinámico de escala para forzar una sola hoja por mesa
                    total_filas = len(matriz_ordenes)
                    if total_filas > 15:
                        escala_css = "escala-micro"
                    elif total_filas > 10:
                        escala_css = "escala-chica"
                    else:
                        escala_css = "escala-normal"

                    mesas_data.append(
                        {
                            "numero_mesa": m,
                            "matriz": matriz_ordenes,
                            "max_orden": max_orden,
                            "escala_css": escala_css,
                        }
                    )

                # Datos del Local para el Encabezado
                nombre_local = f"LOCAL DE VOTACIÓN N° {local_id}"
                context = {
                    "nombre_local": nombre_local,
                    "mesas": mesas_data,
                }

                # Renderizamos el template HTML a un String crudo
                html_string = render(
                    request, "electoral/reports/reporte_mesa.html", context
                ).content.decode("utf-8")

                if HTML is None:
                    return HttpResponse(
                        "Error: WeasyPrint no está configurado en el servidor.",
                        status=500,
                    )

                # Compilación y generación binaria del PDF
                html_pdf = HTML(
                    string=html_string, base_url=request.build_absolute_uri()
                )
                pdf_file = html_pdf.write_pdf()

                filename = (
                    f"Planilla_Local_{local_id}.pdf"
                    if not mesa_num
                    else f"Planilla_Mesa_{mesa_num}.pdf"
                )
                response = HttpResponse(pdf_file, content_type="application/pdf")
                response["Content-Disposition"] = f'inline; filename="{filename}"'
                return response

            else:
                data["error"] = "No ha ingresado una opción válida"

        except Exception as e:
            # Si el request es de tipo reporte JSON devolvemos el error estructurado,
            # si falla la acción del PDF, mostramos el mensaje directo.
            if action == "search_report":
                data["error"] = str(e)
                return HttpResponse(json.dumps(data), content_type="application/json")
            return HttpResponse(f"Error procesando reporte: {str(e)}", status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Barrios y Manzanas"
        return context


class RptPadron001ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_padron001.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        # print(request.POST)
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )
                barrio = (
                    request.POST.getlist("barrio") if "barrio" in request.POST else None
                )
                tipo_voto = (
                    request.POST.getlist("tipo_voto")
                    if "tipo_voto" in request.POST
                    else None
                )
                # Tipo de Voto I - INDECISO es igual a NO DEFINIDOS null ver query reporte
                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_padron001"
                report.report_url = reverse_lazy(report.report_name)
                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )
                report.params["P_BARRIO_ID"] = (
                    ",".join(barrio) if barrio != [""] else None
                )
                report.params["P_TIPO_VOTO_ID"] = (
                    ",".join(tipo_voto) if tipo_voto != [""] else None
                )

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Padron"
        context["action"] = "report"
        return context


"""Electores por Barrios y Manzanas"""


class RptElectoral001ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_electoral001.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        # print(request.POST)
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )
                barrio = (
                    request.POST.getlist("barrio") if "barrio" in request.POST else None
                )
                manzana = (
                    request.POST.getlist("manzana")
                    if "manzana" in request.POST
                    else None
                )
                salto_pagina = (
                    request.POST.getlist("salto_pagina")
                    if "salto_pagina" in request.POST
                    else None
                )
                titulo_extra = (
                    request.POST.getlist("titulo_extra")
                    if "titulo_extra" in request.POST
                    else ""
                )
                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_electoral001"

                report.report_url = reverse_lazy(report.report_name)
                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                if len(titulo_extra):
                    report.report_title = titulo_extra[0]
                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )
                report.params["P_BARRIO_ID"] = (
                    ",".join(barrio) if barrio != [""] else None
                )
                report.params["P_MANZANA_ID"] = (
                    ",".join(manzana) if manzana != [""] else None
                )

                if not salto_pagina:
                    report.report_name = "rpt_electoral001_ss"

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Elector por Barrios y Manzanas"
        context["action"] = "report"
        return context


"""Electores por Barrios y Manzanas"""


class RptElectoral002ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_electoral002.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        # print(request.POST)
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )
                barrio = (
                    request.POST.getlist("barrio") if "barrio" in request.POST else None
                )
                manzana = (
                    request.POST.getlist("manzana")
                    if "manzana" in request.POST
                    else None
                )
                salto_pagina = (
                    request.POST.getlist("salto_pagina")
                    if "salto_pagina" in request.POST
                    else None
                )
                titulo_extra = (
                    request.POST.getlist("titulo_extra")
                    if "titulo_extra" in request.POST
                    else ""
                )
                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_electoral002"
                report.report_url = reverse_lazy(report.report_name)

                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                if len(titulo_extra):
                    report.report_title = titulo_extra[0]

                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )
                report.params["P_BARRIO_ID"] = (
                    ",".join(barrio) if barrio != [""] else None
                )
                report.params["P_MANZANA_ID"] = (
                    ",".join(manzana) if manzana != [""] else None
                )

                if not salto_pagina:
                    report.report_name = "rpt_electoral002_ss"

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Elector por Barrios y Manzanas"
        context["action"] = "report"
        return context


"""Electores por Operadores"""


class RptElectoral003ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_electoral003.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        # print(request.POST)
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )
                barrio = (
                    request.POST.getlist("barrio") if "barrio" in request.POST else None
                )
                manzana = (
                    request.POST.getlist("manzana")
                    if "manzana" in request.POST
                    else None
                )
                operador = (
                    request.POST.getlist("operador")
                    if "operador" in request.POST
                    else None
                )
                salto_pagina = (
                    request.POST.getlist("salto_pagina")
                    if "salto_pagina" in request.POST
                    else None
                )
                titulo_extra = (
                    request.POST.getlist("titulo_extra")
                    if "titulo_extra" in request.POST
                    else ""
                )
                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_electoral003"
                report.report_url = reverse_lazy(report.report_name)

                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                if len(titulo_extra):
                    report.report_title = titulo_extra[0]

                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )
                report.params["P_BARRIO_ID"] = (
                    ",".join(barrio) if barrio != [""] else None
                )
                report.params["P_MANZANA_ID"] = (
                    ",".join(manzana) if manzana != [""] else None
                )
                report.params["P_OPERADOR_ID"] = (
                    ",".join(operador) if operador != [""] else None
                )

                if not salto_pagina:
                    report.report_name = "rpt_electoral003"

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Elector por Barrios y Manzanas"
        context["action"] = "report"
        return context


"""Estadistica de Votos Positivos vs Negativos"""


class RptEstadistica001ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_estadistica001.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )

                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_estadistica001"
                report.report_url = reverse_lazy(report.report_name)
                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Reporte de Estadisticas Votos Positivos vs Negativos"
        context["action"] = "report"
        return context

    """Electores por Barrios y Manzanas Planilla Visita Casa por Casa"""


class RptElectoral004ReportView(ModuleMixin, FormView):
    template_name = "electoral/reports/rpt_electoral004.html"
    form_class = ReportForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        data = {}
        # print(request.POST)
        try:
            if action == "report":
                data = []
                tipo = request.POST["tipo"]
                local_votacion = (
                    request.POST.getlist("local_votacion")
                    if "local_votacion" in request.POST
                    else None
                )
                barrio = (
                    request.POST.getlist("barrio") if "barrio" in request.POST else None
                )
                manzana = (
                    request.POST.getlist("manzana")
                    if "manzana" in request.POST
                    else None
                )
                salto_pagina = (
                    request.POST.getlist("salto_pagina")
                    if "salto_pagina" in request.POST
                    else None
                )
                titulo_extra = (
                    request.POST.getlist("titulo_extra")
                    if "titulo_extra" in request.POST
                    else ""
                )
                filas = (
                    request.POST.getlist("filas") if "filas" in request.POST else None
                )
                # CONFIG
                report = JasperReportBase()
                report.report_name = "rpt_electoral004"

                report.report_url = reverse_lazy(report.report_name)
                report.report_title = (
                    Module.objects.filter(url=report.report_url).first().name
                )
                if len(titulo_extra):
                    report.report_title = titulo_extra[0]
                # PARAMETROS
                report.params["P_LOCAL_VOTACION_ID"] = (
                    ",".join(local_votacion) if local_votacion != [""] else None
                )
                report.params["P_BARRIO_ID"] = (
                    ",".join(barrio) if barrio != [""] else None
                )
                report.params["P_MANZANA_ID"] = (
                    ",".join(manzana) if manzana != [""] else None
                )
                report.params["P_FILAS"] = ",".join(filas) if filas != [""] else None

                if not salto_pagina:
                    report.report_name = "rpt_electoral001_ss"

                return report.render_to_response(tipo)

            else:
                data["error"] = "No ha ingresado una opción"
        except Exception as e:
            data["error"] = str(e)
        return HttpResponse(json.dumps(data), content_type="application/json")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReportForm(usuario=self.request.user)
        context["title"] = "Planilla de Electores para Visita Casa x Casa"
        context["action"] = "report"
        return context


# """Planilla de Mesa para Local de Votación - Generación PDF con WeasyPrint"""
class PlanillaMesaPDFView(ModuleMixin, FormView):
    template_name = "electoral/reports/planilla_mesa_filter.html"
    form_class = FormFilterGenerarPDFMesa

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        data = {}

        try:
            if action == "generate_pdf":
                local_id = request.POST.get("local_votacion")
                mesa_num = request.POST.get("mesa")
                tipo_planilla = request.POST.get("tipo_planilla")

                if not local_id:
                    return HttpResponse(
                        "Error: El ID del Local de Votación es requerido.", status=400
                    )

                local_obj = LocalVotacion.objects.filter(id=local_id).first()
                nombre_local = (
                    local_obj.denominacion if local_obj else f"LOCAL N° {local_id}"
                )

                elector_filter = Elector.objects.filter(local_votacion_id=local_id)

                # --- OPTIMIZACIÓN CRÍTICA CON CAST PARA EL REPORTE COMPLETO ---
                if mesa_num and mesa_num.strip():
                    m_num = int(mesa_num)
                    datos_mesas = (
                        elector_filter.filter(mesa=m_num)
                        .order_by()
                        .values("mesa")
                        .annotate(max_orden=Max(Cast("orden", IntegerField())))
                    )
                    if not datos_mesas:
                        datos_mesas = [{"mesa": m_num, "max_orden": 0}]
                else:
                    # Convertimos el CharField 'mesa' a IntegerField en la query para ordenar rápido
                    datos_mesas = (
                        elector_filter.annotate(mesa_int=Cast("mesa", IntegerField()))
                        .order_by()
                        .values("mesa", "mesa_int")
                        .annotate(max_orden=Max(Cast("orden", IntegerField())))
                        .order_by("mesa_int")
                    )

                mesas_data = []
                columnas = 20

                for d in datos_mesas:
                    m = d["mesa"]

                    try:
                        max_orden = int(d["max_orden"]) if d["max_orden"] else 0
                    except (ValueError, TypeError):
                        max_orden = 0

                    lista_completa = list(range(1, max_orden + 1))
                    matriz_ordenes = [
                        lista_completa[i : i + columnas]
                        for i in range(0, len(lista_completa), columnas)
                    ]

                    if matriz_ordenes:
                        while len(matriz_ordenes[-1]) < columnas:
                            matriz_ordenes[-1].append(None)

                    total_filas = len(matriz_ordenes)
                    if total_filas > 15:
                        escala_css = "escala-micro"
                    elif total_filas > 10:
                        escala_css = "escala-chica"
                    else:
                        escala_css = "escala-normal"

                    mesas_data.append(
                        {
                            "numero_mesa": m,
                            "matriz": matriz_ordenes,
                            "max_orden": max_orden,
                            "escala_css": escala_css,
                        }
                    )

                context = {
                    "nombre_local": nombre_local.upper(),
                    "mesas": mesas_data,
                }

                # 2. SELECCIÓN DINÁMICA DEL TEMPLATE SEGIN EL FILTRO
                if tipo_planilla == "doble":
                    template_reporte = "electoral/reports/planilla_mesa_pdf_doble.html"
                    sufijo_archivo = "_DOBLE"
                else:
                    template_reporte = "electoral/reports/planilla_mesa_pdf.html"
                    sufijo_archivo = ""

                html_string = render_to_string(template_reporte, context)

                if HTML is None:
                    return HttpResponse(
                        "Error: WeasyPrint no está configurado en el servidor.",
                        status=500,
                    )

                html = HTML(
                    string=html_string, base_url=request.build_absolute_uri("/")
                )
                pdf_file = html.write_pdf()

                clean_filename = nombre_local.replace(" ", "_")
                filename = (
                    f"Planilla_{clean_filename}{sufijo_archivo}.pdf"
                    if not mesa_num
                    else f"Planilla_{clean_filename}_Mesa_{mesa_num}.pdf"
                )

                response = HttpResponse(pdf_file, content_type="application/pdf")
                response["Content-Disposition"] = f'inline; filename="{filename}"'
                return response

            else:
                data["error"] = "No ha ingresado una opción válida"
                return HttpResponse(
                    json.dumps(data), content_type="application/json", status=400
                )

        except Exception as e:
            return HttpResponse(f"Error procesando reporte: {str(e)}", status=500)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FormFilterGenerarPDFMesa(usuario=self.request.user)
        context["title"] = "Planilla de Electores para Visita Casa x Casa"
        context["action"] = "generate_pdf"
        return context
