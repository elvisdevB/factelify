from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app.facturacion.views import views

urlpatterns = [
    path('list/', views.FacturaListView.as_view(), name='listar_venta'),
    path('add/', views.FacturaCreateView.as_view(), name='registrar_venta'),
    path('delete/<int:pk>/', views.FacturaDeleteView.as_view(), name='eliminar_venta'),
    path('volante/pdf/<int:pk>/', views.GenerarFacturaVolante.as_view(), name='generar_factura')
]