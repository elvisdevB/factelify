from django.urls import include, path

app_name = 'facturacion'

urlpatterns = [
    path('', include('app.facturacion.urls.facturacion_urls')),
]