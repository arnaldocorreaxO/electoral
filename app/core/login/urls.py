from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginAuthView.as_view(), name='login'),
    path('logout', LogoutRedirectView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_password'),
    path('different/', LoginAuthView.as_view(), name='login_different'),
    path('change/password/<str:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('authenticated/', LoginAuthenticatedView.as_view(), name='login_authenticated'),
]