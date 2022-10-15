from django.urls import path

from. import views

urlpatterns = [
    path('producto_listar/', views.ProductoListView.as_view(), name='producto_listar'),
    path('productos/registrar/', views.ProductoCreateView.as_view(), name="producto_registrar"),
    path('productos/editar/<int:pk>/', views.ProductoUpdateView.as_view(), name="producto_editar"),
    path('productos/eliminar/<int:pk>/', views.ProductoDeleteView.as_view(), name="producto_eliminar"),

    #categoria
    path('categoria/registrar/', views.CategoriaCreateView.as_view(), name="categoria_registrar"),
    path('categoria/listar/', views.CategoriaListView.as_view(), name="categoria_listar"),
    path('categoria/editar/<int:pk>/', views.CategoriaUpdateView.as_view(), name="categoria_editar"),
    path('categoria/eliminar/<int:pk>/', views.CategoriaDeleteView.as_view(), name="categoria_eliminar"),

    #test
    path('test/', views.TestView.as_view(), name="test"),
]
