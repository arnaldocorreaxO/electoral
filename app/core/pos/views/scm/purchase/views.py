import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, FormView

from core.pos.forms import PurchaseForm, Purchase, PurchaseDetail, Product, Provider, DebtsPay, ProviderForm
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PurchaseListView(PermissionMixin, FormView):
    template_name = 'scm/purchase/list.html'
    permission_required = 'view_purchase'
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
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                search = Purchase.objects.filter()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            elif action == 'search_detproducts':
                data = []
                for det in PurchaseDetail.objects.filter(purchase_id=request.POST['id']):
                    data.append(det.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('purchase_create')
        context['title'] = 'Listado de Compras'
        return context


class PurchaseCreateView(PermissionMixin, CreateView):
    model = Purchase
    template_name = 'scm/purchase/create.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase_list')
    permission_required = 'add_purchase'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def validate_provider(self):
        data = {'valid': True}
        try:
            type = self.request.POST['type']
            obj = self.request.POST['obj'].strip()
            if type == 'name':
                if Provider.objects.filter(name__iexact=obj):
                    data['valid'] = False
            elif type == 'ruc':
                if Provider.objects.filter(ruc__iexact=obj):
                    data['valid'] = False
            elif type == 'mobile':
                if Provider.objects.filter(mobile=obj):
                    data['valid'] = False
            elif type == 'email':
                if Provider.objects.filter(email=obj):
                    data['valid'] = False
        except:
            pass
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    purchasejson = json.loads(request.POST['purchase'])
                    purchase = Purchase()
                    purchase.provider_id = int(purchasejson['provider'])
                    purchase.payment_condition = purchasejson['payment_condition']
                    purchase.date_joined = purchasejson['date_joined']
                    purchase.save()

                    for p in purchasejson['products']:
                        prod = Product.objects.get(pk=p['id'])
                        det = PurchaseDetail()
                        det.purchase_id = purchase.id
                        det.product_id = prod.id
                        det.cant = int(p['cant'])
                        det.price = float(p['price'])
                        det.subtotal = det.cant * float(det.price)
                        det.save()

                        det.product.stock += det.cant
                        det.product.save()

                    purchase.calculate_invoice()

                    if purchase.payment_condition == 'credito':
                        purchase.end_credit = purchasejson['end_credit']
                        purchase.save()
                        debtspay = DebtsPay()
                        debtspay.purchase_id = purchase.id
                        debtspay.date_joined = purchase.date_joined
                        debtspay.end_date = purchase.end_credit
                        debtspay.debt = purchase.subtotal
                        debtspay.saldo = purchase.subtotal
                        debtspay.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                search = Product.objects.filter(category__inventoried=True).exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(name__icontains=term)
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = '{} / {}'.format(p.name, p.category.name)
                    data.append(item)
            elif action == 'search_provider':
                data = []
                for p in Provider.objects.filter(name__icontains=request.POST['term']).order_by('name')[0:10]:
                    item = p.toJSON()
                    item['text'] = '{} / {}'.format(p.name, p.ruc)
                    data.append(item)
            elif action == 'validate_provider':
                return self.validate_provider()
            elif action == 'create_provider':
                form = ProviderForm(request.POST)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmProvider'] = ProviderForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Compra'
        context['action'] = 'add'
        return context


class PurchaseDeleteView(PermissionMixin, DeleteView):
    model = Purchase
    template_name = 'scm/purchase/delete.html'
    success_url = reverse_lazy('purchase_list')
    permission_required = 'delete_purchase'

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
