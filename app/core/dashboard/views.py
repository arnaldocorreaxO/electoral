from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum,Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView

from core.reports.choices import months
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
            if action == 'get_graph_stock_products':
                info = []
                # for i in Product.objects.order_by('-id')[0:10]:
                #     info.append([i.name, i.stock])
                for i in Elector.objects.values('seccional__denominacion') \
                        .annotate(tot_electores=Count(True)) \
                        .order_by('-tot_electores'):
                        info.append([i['seccional__denominacion'],i['tot_electores']])
                
                data = {
                    'name': 'Stock de Productos',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_purchase_vs_sale':
                data = []
                year = datetime.now().year
                rows = []
                for i in months[1:]:
                    result = Sale.objects.filter(date_joined__month=i[0], date_joined__year=year).aggregate(
                        resp=Coalesce(Sum('total'), 0.00))['resp']
                    rows.append(float(result))
                data.append({'name': 'Ventas', 'data': rows})
                rows = []
                for i in months[1:]:
                    result = Purchase.objects.filter(date_joined__month=i[0], date_joined__year=year).aggregate(
                        resp=Coalesce(Sum('subtotal'), 0.00))['resp']
                    rows.append(float(result))
                data.append({'name': 'Compras', 'data': rows})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['company'] = Company.objects.first()
        context['clients'] = Client.objects.all().count()
        context['provider'] = Provider.objects.all().count()
        context['category'] = Category.objects.filter().count()
        context['product'] = Product.objects.all().count()
        context['sale'] = Sale.objects.filter().order_by('-id')[0:10]
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
