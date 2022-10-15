from django.urls import  path
from app.reports import views

urlpatterns = [
    path('venta/', views.ReportVenta.as_view(), name="reporte_venta"),

]