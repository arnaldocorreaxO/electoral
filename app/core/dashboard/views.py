from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum,Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView

from core.reports.choices import months,rango_edad
from core.pos.models import Product, Sale, Client, Provider, Category, Purchase, Company
from core.electoral.models import Elector, Seccional
from core.security.models import Dashboard



class DashboardView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtcpanel.html'
        return 'hztpanel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_electores_seccional':
                info = []
                # for i in Product.objects.order_by('-id')[0:10]:
                #     info.append([i.name, i.stock])
                for i in Elector.objects.values('seccional__denominacion') \
                        .annotate(tot_electores=Count(True)) \
                        .order_by('-tot_electores'):
                        info.append([i['seccional__denominacion'],i['tot_electores']])
                
                data = {
                    'name': 'Electores por Seccional',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_preferencia_votos':
                info = []
                # for i in Product.objects.order_by('-id')[0:10]:
                #     info.append([i.name, i.stock])
                for i in Elector.objects.values('tipo_voto__denominacion') \
                        .exclude(tipo_voto__cod__in=['F','E'])\
                        .annotate(tot_votos=Count(True)) \
                        .order_by('-tot_votos'):
                        info.append([i['tipo_voto__denominacion'] if i['tipo_voto__denominacion'] else 'SIN PREFERENCIA',
                                     i['tot_votos']])
               
                data = {
                    'name': 'Preferencia de Votos',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }

            elif action == 'get_graph_rango_edades_pie':
                info = []
                data = []
                # Todas las edades de los Electores
                for i in rango_edad[1:]:
                    hoy = datetime.now()
                    anho_ini = (hoy - relativedelta(years=i[1])).year
                    anho_fin = (hoy - relativedelta(years=i[0])).year

                    cant = Elector.objects.filter(fecha_nacimiento__year__range=[anho_ini,anho_fin])\
                            .aggregate(cant=Coalesce(Count(True), 0))['cant']
                    info.append([i[2],cant])
               
                data = {
                    'name': 'Pie Rango Edades',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_rango_edades':
                data = []
                rows = []
                # Todas las edades de los Electores
                for i in rango_edad[1:]:
                    hoy = datetime.now()
                    anho_ini = (hoy - relativedelta(years=i[1])).year
                    anho_fin = (hoy - relativedelta(years=i[0])).year
                    # print(anho_ini,'-',anho_fin)
                    result = Elector.objects.filter(fecha_nacimiento__year__range=[anho_ini,anho_fin])\
                                            .aggregate(cant=Coalesce(Count(True), 0))['cant']
                    rows.append(float(result))
                data.append({'name': 'Total', 'data': rows})
                rows = []
                # Solo Electores Identificados
                for i in rango_edad[1:]:
                    hoy = datetime.now()
                    anho_ini = (hoy - relativedelta(years=i[1])).year
                    anho_fin = (hoy - relativedelta(years=i[0])).year
                    # print(anho_ini,'-',anho_fin)
                    result = Elector.objects.filter(fecha_nacimiento__year__range=[anho_ini,anho_fin])\
                                            .exclude(barrio_id__exact=0)\
                                            .exclude(barrio__isnull=True)\
                                            .aggregate(cant=Coalesce(Count(True), 0))['cant']
                    
                    rows.append(float(result))
                data.append({'name': 'Identificados', 'data': rows})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['company'] = Company.objects.first()
        context['elector'] = Elector.objects.all().count()
        context['votos_positivos'] = Elector.objects.filter(tipo_voto__exact=6).count()
        context['votos_negativos'] = Elector.objects.exclude(tipo_voto__cod__in=[6,'A','E','F']).count()
        context['product'] = Product.objects.all().count()
        context['sale'] = Sale.objects.filter().order_by('-id')[0:10]
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
