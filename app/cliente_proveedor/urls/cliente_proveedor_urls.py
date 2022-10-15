from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app.cliente_proveedor.views import views
# path('', views.cliente_listar, name='cliente_listar'),
urlpatterns = [
    path('cliente_list/', views.ClienteListView.as_view(), name='cliente_listar'),
    path('registrar_cliente/',views.ClienteCreateView.as_view(), name='cliente_registrar'),
    path('editar_cliente/<int:pk>/',views.ClienteUpdateView.as_view(), name='cliente_modificar'),
    path('eliminar_cliente/<int:pk>/',views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
    #Proveedor
    path('proveedor_listar/', views.ProveedorListView.as_view(), name='proveedor_listar'),
    path('registrar_proveedor/',views.ProveedorCreateView.as_view(), name='proveedor_registrar'),
    path('editar_proveedor/<int:pk>/',views.ProveedorUpdateView.as_view(), name='proveedor_modificar'),
    path('eliminar_proveedor/<int:pk>/',views.ProveedorDeleteView.as_view(), name='proveedor_eliminar'),
]
