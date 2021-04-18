import json

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from core.pos.models import Purchase, Sale, Expenses
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ResultsReportView(ModuleMixin, FormView):
    template_name = 'results_report/report.html'
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
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']

                purchase = Purchase.objects.all()
                if len(start_date) and len(end_date):
                    purchase = purchase.filter(date_joined__range=[start_date, end_date])
                purchase = float(purchase.aggregate(resp=Coalesce(Sum('subtotal'), 0.00)).get('resp'))

                sale = Sale.objects.all()
                if len(start_date) and len(end_date):
                    sale = sale.filter(date_joined__range=[start_date, end_date])
                sale = float(sale.aggregate(resp=Coalesce(Sum('total'), 0.00)).get('resp'))

                expenses = Expenses.objects.all()
                if len(start_date) and len(end_date):
                    expenses = expenses.filter(date_joined__range=[start_date, end_date])
                expenses = float(expenses.aggregate(resp=Coalesce(Sum('valor'), 0.00)).get('resp'))

                data.append({'name': 'Compras', 'y': purchase})
                data.append({'name': 'Ventas', 'y': sale})
                data.append({'name': 'Gastos', 'y': expenses})
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Resultados'
        return context
