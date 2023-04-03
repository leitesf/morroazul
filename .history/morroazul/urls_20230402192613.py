from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('',include('website.urls')),
    path('admin/', admin.site.urls),
    path('cliente/<int:cliente_id>/', views.show_cliente),
    path('nota_fiscal/<int:nota_fiscal_id>/', views.show_nota_fiscal),
    path('transportador/<int:transportador_id>/', views.show_transportador),
    path('usuario/<int:usuario_id>/alterar_senha/', views.alterar_senha),
    path('minhas_nfs_cliente/', views.show_cliente),
    path('minhas_nfs_transportador/', views.show_transportador),
]
