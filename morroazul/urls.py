from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main import views

urlpatterns = [
    path('',include('website.urls')),
    path('admin/', admin.site.urls),
    path('cliente/<int:cliente_id>/', views.show_cliente),
    path('nota_fiscal/<int:nota_fiscal_id>/', views.show_nota_fiscal),
    path('pedido/<int:pedido_id>/', views.show_pedido),
    path('pedido/<int:pedido_id>/aprovar/', views.aprovar_pedido),
    path('pedido/<int:pedido_id>/reprovar/', views.reprovar_pedido),
    path('pedido/<int:pedido_id>/entregar/', views.entregar_pedido),
    path('beneficio/<int:beneficio_id>/', views.show_beneficio),
    path('beneficio/<int:beneficio_id>/pedir', views.fazer_pedido),
    path('transportador/<int:transportador_id>/', views.show_transportador),
    path('usuario/<int:usuario_id>/alterar_senha/', views.alterar_senha),
    path('minhas_nfs_cliente/', views.show_cliente),
    path('minhas_nfs_transportador/', views.show_transportador),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
