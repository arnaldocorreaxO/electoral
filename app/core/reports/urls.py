from django.urls import path
from .views.electoral.views import *
urlpatterns = [    
    # REPORTES ELECTORAL    
    path('rpt_padron001/', RptPadron001ReportView.as_view(), name='rpt_padron001'),
    path('rpt_electoral000/', RptElectoral000ReportView.as_view(), name='rpt_electoral000'),
    path('rpt_electoral001/', RptElectoral001ReportView.as_view(), name='rpt_electoral001'),
    path('rpt_electoral002/', RptElectoral002ReportView.as_view(), name='rpt_electoral002'),
    path('rpt_electoral003/', RptElectoral002ReportView.as_view(), name='rpt_electoral003'),
    path('rpt_estadistica001/', RptEstadistica001ReportView.as_view(), name='rpt_estadistica001'),
]
