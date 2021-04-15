import json

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, CreateView, FormView

from core.pos.forms import *
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class DebtsPayListView(PermissionMixin, FormView):
    template_name = 'frm/debtspay/list.html'
    permission_required = 'view_debtspay'
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
                search = DebtsPay.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for a in search:
                    data.append(a.toJSON())
            elif action == 'search_pays':
                data = []
                pos = 1
                for det in PaymentsDebtsPay.objects.filter(debtspay_id=request.POST['id']):
                    item = det.toJSON()
                    item['pos'] = pos
                    data.append(item)
                    pos += 1
            elif action == 'delete_pay':
                id = request.POST['id']
                det = PaymentsDebtsPay.objects.get(pk=id)
                debtspay = det.debtspay
                det.delete()
                debtspay.validate_debt()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cuentas por Pagar'
        context['create_url'] = reverse_lazy('debtspay_create')
        return context


class DebtsPayCreateView(PermissionMixin, CreateView):
    model = DebtsPay
    template_name = 'frm/debtspay/create.html'
    form_class = PaymentsDebtsPayForm
    success_url = reverse_lazy('debtspay_list')
    permission_required = 'add_debtspay'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_debtspay':
                data = []
                term = request.POST['term']
                for i in DebtsPay.objects.filter(purchase__provider__name__icontains=term).exclude(state=False)[0:10]:
                    item = i.toJSON()
                    item['text'] = i.__str__()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    payment = PaymentsDebtsPay()
                    payment.debtspay_id = int(request.POST['debtspay'])
                    payment.date_joined = request.POST['date_joined']
                    payment.valor = float(request.POST['valor'])
                    payment.desc = request.POST['desc']
                    if len(payment.desc) == 0:
                        payment.desc = 'Sin detalles'
                    payment.save()
                    payment.debtspay.validate_debt()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Pago'
        context['action'] = 'add'
        return context


class DebtsPayDeleteView(PermissionMixin, DeleteView):
    model = DebtsPay
    template_name = 'frm/debtspay/delete.html'
    success_url = reverse_lazy('debtspay_list')
    permission_required = 'delete_debtspay'

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
