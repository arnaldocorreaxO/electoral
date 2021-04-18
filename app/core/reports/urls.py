from django.urls import path
from .views.sale_report.views import SaleReportView
from .views.purchase_report.views import PurchaseReportView
from .views.expenses_report.views import ExpensesReportView
from .views.debtspay_report.views import DebtsPayReportView
from .views.ctascollect_report.views import CtasCollectReportView
from .views.results_report.views import ResultsReportView
from .views.electoral.views import ElectorReportView, Rpt001ReportView

urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('elector/barrio_manzana/', ElectorReportView.as_view(), name='elector_report'),
    path('rpt001/', Rpt001ReportView.as_view(), name='rpt001_report'),
    path('expenses/', ExpensesReportView.as_view(), name='expenses_report'),
    path('debts/pay/', DebtsPayReportView.as_view(), name='debtspay_report'),
    path('ctas/collect/', CtasCollectReportView.as_view(), name='ctascollect_report'),
    path('results/', ResultsReportView.as_view(), name='results_report'),
]
