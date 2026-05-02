import os

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from weasyprint import HTML, CSS

from config import settings
from core.pos.models import Sale, Company


class SalePrintVoucherView(View):
    success_url = reverse_lazy('sale_admin_list')

    def get_success_url(self):
        if self.request.user.is_client():
            return reverse_lazy('sale_client_list')
        return self.success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_height_ticket(self):
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        height = 120
        increment = sale.saledetail_set.all().count() * 5.45
        height += increment
        return round(height)

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(pk=self.kwargs['pk'])
            context = {'sale': sale, 'company': Company.objects.first()}
            if sale.type_voucher == 'ticket':
                template = get_template('crm/sale/print/ticket.html')
                context['height'] = self.get_height_ticket()
            else:
                template = get_template('crm/sale/print/invoice.html')
            html_template = template.render(context).encode(encoding="UTF-8")
            url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.3.1/css/bootstrap.min.css')
            pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
                stylesheets=[CSS(url_css)], presentational_hints=True)
            response = HttpResponse(pdf_file, content_type='application/pdf')
            # response['Content-Disposition'] = 'filename="generate_html.pdf"'
            return response
        except:
            pass
        return HttpResponseRedirect(self.get_success_url())
