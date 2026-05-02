import json
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.pos.forms import Promotions, PromotionsForm, Product, PromotionsDetail
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PromotionsListView(PermissionMixin, FormView):
    template_name = 'crm/promotions/list.html'
    permission_required = 'view_promotions'
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
                end_date = request.POST['start_date']
                search = Promotions.objects.filter()
                if len(start_date) and len(end_date):
                    search = search.filter(start_date__range=[start_date, end_date])
                for i in search:
                    data.append(i.toJSON())
            elif action == 'search_detproducts':
                data = []
                for det in PromotionsDetail.objects.filter(promotion_id=request.POST['id']):
                    data.append(det.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_queryset(self):
        date_now = datetime.now().date()
        proms = Promotions.objects.filter(end_date__lte=date_now, state=True)
        if proms.exists():
            proms.update(state=False)
        return Promotions.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('promotions_create')
        context['title'] = 'Listado de Promociones'
        return context


class PromotionsCreateView(PermissionMixin, CreateView):
    model = Promotions
    template_name = 'crm/promotions/create.html'
    form_class = PromotionsForm
    success_url = reverse_lazy('promotions_list')
    permission_required = 'add_promotions'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    jsondata = json.loads(request.POST['promotions'])
                    promotion = Promotions()
                    promotion.start_date = datetime.strptime(jsondata['start_date'], '%Y-%m-%d')
                    promotion.end_date = datetime.strptime(jsondata['end_date'], '%Y-%m-%d')
                    promotion.save()
                    promotion.state = promotion.end_date.date() > promotion.start_date.date()
                    promotion.save()
                    for p in jsondata['products']:
                        prod = Product.objects.get(pk=p['id'])
                        det = PromotionsDetail()
                        det.promotion_id = promotion.id
                        det.product_id = prod.id
                        det.dscto = float(p['dscto']) / 100
                        det.price_current = float(prod.pvp)
                        det.total_dscto = det.get_dscto_real()
                        det.price_final = float(det.price_current) - float(det.total_dscto)
                        det.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']

                ids = ids + list(
                    PromotionsDetail.objects.filter(promotion__state=True).values_list('product_id', flat=True))

                search = Product.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(Q(name__icontains=term) | Q(name__icontains=term))
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = p.name
                    item['choose'] = False
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Promoción'
        context['action'] = 'add'
        context['products'] = []
        return context


class PromotionsUpdateView(PermissionMixin, UpdateView):
    model = Promotions
    template_name = 'crm/promotions/create.html'
    form_class = PromotionsForm
    success_url = reverse_lazy('promotions_list')
    permission_required = 'change_promotions'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    jsondata = json.loads(request.POST['promotions'])
                    promotion = self.object
                    promotion.start_date = datetime.strptime(jsondata['start_date'], '%Y-%m-%d')
                    promotion.end_date = datetime.strptime(jsondata['end_date'], '%Y-%m-%d')
                    promotion.save()
                    promotion.state = promotion.end_date.date() > promotion.start_date.date()
                    promotion.save()
                    promotion.promotionsdetail_set.all().delete()
                    for p in jsondata['products']:
                        prod = Product.objects.get(pk=p['id'])
                        det = PromotionsDetail()
                        det.promotion_id = promotion.id
                        det.product_id = prod.id
                        det.dscto = float(p['dscto']) / 100
                        det.price_current = float(prod.pvp)
                        det.total_dscto = det.get_dscto_real()
                        det.price_final = float(det.price_current) - float(det.total_dscto)
                        det.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']

                ids = ids + list(
                    PromotionsDetail.objects.filter(promotion__state=True).values_list('product_id', flat=True))

                search = Product.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    search = search.filter(Q(name__icontains=term) | Q(name__icontains=term))
                    search = search[0:10]
                for p in search:
                    item = p.toJSON()
                    item['value'] = p.name
                    item['choose'] = False
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_detproducts(self):
        data = []
        try:
            for i in self.object.promotionsdetail_set.all():
                item = i.product.toJSON()
                item['dscto'] = format(float(i.dscto) * 100, '.2f')
                item['total_dscto'] = format(i.total_dscto, '.2f')
                item['price_current'] = format(i.price_current, '.2f')
                item['price_final'] = format(i.price_final, '.2f')
                data.append(item)
        except:
            pass
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nueva Edición de una Promoción'
        context['action'] = 'edit'
        context['products'] = self.get_detproducts()
        return context


class PromotionsDeleteView(PermissionMixin, DeleteView):
    model = Promotions
    template_name = 'crm/promotions/delete.html'
    success_url = reverse_lazy('promotions_list')
    permission_required = 'delete_promotions'

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
