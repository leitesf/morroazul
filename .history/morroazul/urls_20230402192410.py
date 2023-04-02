"""morroazul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

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
