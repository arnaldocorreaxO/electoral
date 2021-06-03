from django.urls import path
from .views.electoral.views import (RptElectoral001ReportView, 
                                    RptElectoral002ReportView,
                                    RptEstadistica001ReportView, 
                                    RptPadron001ReportView)

urlpatterns = [
    # path('sale/', SaleReportView.as_view(), name='sale_report'),
    # path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    # path('expenses/', ExpensesReportView.as_view(), name='expenses_report'),
    # path('debts/pay/', DebtsPayReportView.as_view(), name='debtspay_report'),
    # path('ctas/collect/', CtasCollectReportView.as_view(), name='ctascollect_report'),
    # path('results/', ResultsReportView.as_view(), name='results_report'),
    
    # REPORTES ELECTORAL    
    path('rpt_padron001/', RptPadron001ReportView.as_view(), name='rpt_padron001'),
    path('rpt_electoral001/', RptElectoral001ReportView.as_view(), name='rpt_electoral001'),
    path('rpt_electoral002/', RptElectoral002ReportView.as_view(), name='rpt_electoral002'),
    path('rpt_estadistica001/', RptEstadistica001ReportView.as_view(), name='rpt_estadistica001'),
]
