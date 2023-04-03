from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import PasswordForm
from main.models import Cliente, Usuario, NotaFiscal, Transportador, Beneficio
from main.utils import gerar_menu


@login_required
def show_cliente(request, cliente_id=None):
    if cliente_id:
        cliente = get_object_or_404(Cliente, id=cliente_id)
    elif request.user.cliente_set.exists():
        cliente = request.user.cliente_set.first()
    else:
        messages.success(request, 'Você não possui permissão para visualizar essa página')
        return redirect('/admin/')
    side_menu_list = gerar_menu(request.user, ativo='cliente' if cliente_id else 'minhas_notas_cliente')
    return render(request, 'cliente.html', locals())


@login_required
def show_transportador(request, transportador_id=None):
    if transportador_id:
        transportador = get_object_or_404(Transportador, id=transportador_id)
    elif request.user.transportador_set.exists():
        transportador = request.user.transportador_set.first()
    else:
        messages.success(request, 'Você não possui permissão para visualizar essa página')
        return redirect('/admin/')
    side_menu_list = gerar_menu(request.user, ativo='transportador')
    return render(request, 'transportador.html', locals())


@login_required
def show_nota_fiscal(request, nota_fiscal_id):
    nota_fiscal = get_object_or_404(NotaFiscal, id=nota_fiscal_id)
    side_menu_list = gerar_menu(request.user, ativo='nota_fiscal')
    return render(request, 'nota_fiscal.html', locals())


@login_required
def show_beneficio(request, beneficio_id):
    beneficio = get_object_or_404(Beneficio, id=beneficio_id)
    side_menu_list = gerar_menu(request.user, ativo='beneficio')
    pode_ver_estoque = request.user.has_perm('main.add_beneficio')
    return render(request, 'beneficio.html', locals())


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
