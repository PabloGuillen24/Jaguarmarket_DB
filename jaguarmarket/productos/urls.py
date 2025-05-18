from django.urls import path
from . import views

urlpatterns = [
    # La vista "home" detecta si el usuario está logueado o no
    path('', views.home, name='home'),

    # Autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario,   name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # Perfil
    path('perfil/',       views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/',views.editar_perfil,   name='editar_perfil'),

    # Productos
    path('publicar/',         views.publicar_producto,    name='publicar_producto'),
    path('mis-productos/',    views.mis_productos,        name='mis_productos'),
    path('explorar/',         views.explorar_productos,   name='explorar_productos'),
    path('producto/<int:producto_id>/',                    views.detalle_producto,      name='detalle_producto'),
    path('editar-mi-producto/<int:producto_id>/',          views.editar_mi_producto,    name='editar_producto'),
    path('eliminar-producto/<int:producto_id>/',           views.eliminar_producto,     name='eliminar_producto'),

    # Chats por producto
    path('producto/<int:producto_id>/mensajes/',           views.mensajes_producto,     name='mensajes_producto'),

    # Listado global de chats
    path('chats/',            views.mis_chats,            name='mis_chats'),

    # Chat genérico entre dos usuarios (si aún lo usas)
    path('chat/<int:user_id>/', views.chat,               name='chat'),

    path('acerca/', views.acerca, name='acerca'),
    path('estudio-factibilidad/', views.estudio_factibilidad, name='estudio_factibilidad'),
    path('estudio-mercado/', views.estudio_mercado, name='estudio_mercado'),
    path('estudios-sociologicos/', views.estudios_sociologicos, name='estudios_sociologicos'),
    path('estudios-etnograficos/', views.estudios_etnograficos, name='estudios_etnograficos'),
    path('estudios-axiologicos/', views.estudios_axiologicos, name='estudios_axiologicos'),
]
