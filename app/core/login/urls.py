from django.urls import path
from app.core.login.views import ChangePasswordView, LoguinFormView, LogoutFormView, ResetPasswordView

urlpatterns = [
    path('', LoguinFormView.as_view(), name='login'),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='reset_pass'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change_pass'),
]