from django.urls import include, path

app_name = 'cliente_proveedor'

urlpatterns = [
    path('', include('app.cliente_proveedor.urls.cliente_proveedor_urls')),
]