from django.urls import path
from .views.dashboard.views import *
from .views.moduletype.views import *
from .views.module.views import *
from .views.group.views import *
from .views.accessusers.views import *
from .views.databasebackups.views import *

urlpatterns = [
    # module_type
    path('module/type/', TypeListView.as_view(), name='moduletype_list'),
    path('module/type/add/', TypeCreateView.as_view(), name='moduletype_create'),
    path('module/type/update/<int:pk>/', TypeUpdateView.as_view(), name='moduletype_update'),
    path('module/type/delete/<int:pk>/', TypeDeleteView.as_view(), name='moduletype_delete'),
    # module
    path('module/', ModuleListView.as_view(), name='module_list'),
    path('module/add/', ModuleCreateView.as_view(), name='module_create'),
    path('module/update/<int:pk>/', ModuleUpdateView.as_view(), name='module_update'),
    path('module/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),
    # group
    path('group/', GroupListView.as_view(), name='group_list'),
    path('group/add/', GroupCreateView.as_view(), name='group_create'),
    path('group/update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('group/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    # access
    path('access/users/', UsersListView.as_view(), name='accessusers_list'),
    path('access/users/delete/<int:pk>/', UsersDeleteView.as_view(), name='accessusers_delete'),
    # database
    path('database/backups/', DatabaseBackupsListView.as_view(), name='databasebackups_list'),
    path('database/backups/add/', DatabaseBackupsCreateView.as_view(), name='databasebackups_create'),
    path('database/backups/delete/<int:pk>/', DatabaseBackupsDeleteView.as_view(), name='databasebackups_delete'),
    # dashboard
    path('dashboard/update/', DashboardView.as_view(), name='dashboard_update'),
]
