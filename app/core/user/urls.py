from django.urls import path

from app.core.user.views import  *

urlpatterns = [
    path('listar/', UseriaListView.as_view(), name='listar_usuarios'),
    path('registrar/', RegistrarUser.as_view(), name='registrar_usuarios'),
    path('editar/<int:pk>/', EditarUser.as_view(), name="editar_usuarios"),
    path('eliminar/<int:pk>/', UsuarioDeleteView.as_view(), name="eliminar_usuarios"),
    path('change/group/<int:pk>/', GroupView.as_view(), name="usuario_cambiar_grupos"),
    path('perfil/', UserProfileView.as_view(), name="editar_perfil"),
    path('edit/password/', UserChangePassword.as_view(), name="editar_password"),
]
