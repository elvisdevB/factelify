"""factelify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from factelify import views
from django.conf import settings
from django.conf.urls.static import static
from app.core.homepage.views import IndexView
urlpatterns = [
    path('', IndexView.as_view(),name='index'),
    path('principal/', views.Principal.as_view(), name='principal'),
    path('admin/', admin.site.urls),
    path('login/', include('app.core.login.urls')),
    path('cliente/', include('app.cliente_proveedor.urls')),
    path('facturacion/', include('app.facturacion.urls')),
    path('inventario/', include('app.inventario.urls')),
    path('reports/',include('app.reports.urls')),
    path('user/', include('app.core.user.urls')),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)