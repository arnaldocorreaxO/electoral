from django.urls import path
from .views.users.views import *

urlpatterns = [
    path('admin/', UserListView.as_view(), name='user_list'),
    path('admin/add/', UserCreateView.as_view(), name='user_create'),
    path('admin/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('admin/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('admin/update/password/', UserUpdatePasswordView.as_view(), name='user_update_password'),
    path('admin/update/profile/', UserUpdateProfileView.as_view(), name='user_update_profile'),
    path('admin/choose/profile/<int:pk>/', UserChooseProfileView.as_view(), name='user_choose_profile'),
]
