from django.urls import path

from core.pos.views.crm.company.views import CompanyUpdateView
from core.pos.views.crm.promotions.views import *
from core.pos.views.crm.sale.admin.views import *
from core.pos.views.crm.sale.client.views import SaleClientListView
from core.pos.views.frm.ctascollect.views import *
from core.pos.views.frm.debtspay.views import *
from core.pos.views.scm.product.views import *
from core.pos.views.scm.provider.views import *
from core.pos.views.scm.category.views import *
from core.pos.views.scm.purchase.views import *
from core.pos.views.frm.typeexpense.views import *
from core.pos.views.frm.expenses.views import *
from core.pos.views.crm.client.views import *
from core.pos.views.crm.sale.print.views import *

urlpatterns = [
    # company
    path('crm/company/update/', CompanyUpdateView.as_view(), name='company_update'),
    # provider
    path('scm/provider/', ProviderListView.as_view(), name='provider_list'),
    path('scm/provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('scm/provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('scm/provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),
    # category
    path('scm/category/', CategoryListView.as_view(), name='category_list'),
    path('scm/category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('scm/category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('scm/category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # product
    path('scm/product/', ProductListView.as_view(), name='product_list'),
    path('scm/product/add/', ProductCreateView.as_view(), name='product_create'),
    path('scm/product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('scm/product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('scm/product/stock/adjustment/', ProductStockAdjustmentView.as_view(), name='product_stock_adjustment'),
    path('scm/product/export/excel/', ProductExportExcelView.as_view(), name='product_export_excel'),
    # purchase
    path('scm/purchase/', PurchaseListView.as_view(), name='purchase_list'),
    path('scm/purchase/add/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('scm/purchase/delete/<int:pk>/', PurchaseDeleteView.as_view(), name='purchase_delete'),
    # type_expense
    path('frm/type/expense/', TypeExpenseListView.as_view(), name='typeexpense_list'),
    path('frm/type/expense/add/', TypeExpenseCreateView.as_view(), name='typeexpense_create'),
    path('frm/type/expense/update/<int:pk>/', TypeExpenseUpdateView.as_view(), name='typeexpense_update'),
    path('frm/type/expense/delete/<int:pk>/', TypeExpenseDeleteView.as_view(), name='typeexpense_delete'),
    # expenses
    path('frm/expenses/', ExpensesListView.as_view(), name='expenses_list'),
    path('frm/expenses/add/', ExpensesCreateView.as_view(), name='expenses_create'),
    path('frm/expenses/update/<int:pk>/', ExpensesUpdateView.as_view(), name='expenses_update'),
    path('frm/expenses/delete/<int:pk>/', ExpensesDeleteView.as_view(), name='expenses_delete'),
    # debtspay
    path('frm/debts/pay/', DebtsPayListView.as_view(), name='debtspay_list'),
    path('frm/debts/pay/add/', DebtsPayCreateView.as_view(), name='debtspay_create'),
    path('frm/debts/pay/delete/<int:pk>/', DebtsPayDeleteView.as_view(), name='debtspay_delete'),
    # ctascollect
    path('frm/ctas/collect/', CtasCollectListView.as_view(), name='ctascollect_list'),
    path('frm/ctas/collect/add/', CtasCollectCreateView.as_view(), name='ctascollect_create'),
    path('frm/ctas/collect/delete/<int:pk>/', CtasCollectDeleteView.as_view(), name='ctascollect_delete'),
    # promotions
    path('crm/promotions/', PromotionsListView.as_view(), name='promotions_list'),
    path('crm/promotions/add/', PromotionsCreateView.as_view(), name='promotions_create'),
    path('crm/promotions/update/<int:pk>/', PromotionsUpdateView.as_view(), name='promotions_update'),
    path('crm/promotions/delete/<int:pk>/', PromotionsDeleteView.as_view(), name='promotions_delete'),
    # client
    path('crm/client/', ClientListView.as_view(), name='client_list'),
    path('crm/client/add/', ClientCreateView.as_view(), name='client_create'),
    path('crm/client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('crm/client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('crm/client/update/profile/', ClientUpdateProfileView.as_view(), name='client_update_profile'),
    # sale/admin
    path('crm/sale/admin/', SaleAdminListView.as_view(), name='sale_admin_list'),
    path('crm/sale/admin/add/', SaleAdminCreateView.as_view(), name='sale_admin_create'),
    path('crm/sale/admin/delete/<int:pk>/', SaleAdminDeleteView.as_view(), name='sale_admin_delete'),
    path('crm/sale/print/voucher/<int:pk>/', SalePrintVoucherView.as_view(), name='sale_print_ticket'),
    path('crm/sale/client/', SaleClientListView.as_view(), name='sale_client_list'),
]
