from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import PasswordForm
from main.models import Cliente, Usuario
from main.utils import gerar_menu


@login_required
def show_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    side_menu_list = gerar_menu(request.user)
    return render(request, 'cliente.html', locals())


@permission_required('main.add_usuario')
def alterar_senha(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    side_menu_list = gerar_menu(request.user)
    titulo = "Alterar senha de Usuário"

    if request.method == "POST":
        form = PasswordForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario.set_password(form.cleaned_data['senha'])
            usuario.save()
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/admin/main/usuario/')
    else:
        form = PasswordForm(instance=usuario)
    return render(request, 'form.html', locals())

# Create your views here.
