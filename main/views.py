from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import PasswordForm
from main.models import Cliente, Usuario, NotaFiscal, Transportador, Beneficio, Pedido, StatusPedido
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
    pode_comprar = request.user.has_perm('main.fazer_pedido') and beneficio.estoque > 0
    return render(request, 'beneficio.html', locals())


@login_required
def show_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    side_menu_list = gerar_menu(request.user, ativo='pedido')
    pode_ver_estoque = request.user.has_perm('main.add_pedido')
    pode_aprovar = request.user.has_perm('main.aprovar_pedido') and pedido.status == StatusPedido.PENDENTE
    pode_entregar = request.user.has_perm('main.entregar_pedido') and pedido.status == StatusPedido.APROVADO
    return render(request, 'pedido.html', locals())


@permission_required('main.aprovar_pedido')
def aprovar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = StatusPedido.APROVADO
    pedido.save()
    messages.success(request, 'Pedido aprovado com sucesso')
    return redirect('/admin/main/pedido/')


@permission_required('main.aprovar_pedido')
def reprovar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = StatusPedido.CANCELADO
    pedido.save()
    messages.success(request, 'Pedido reprovado com sucesso')
    return redirect('/admin/main/pedido/')


@permission_required('main.entregar_pedido')
def entregar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.status = StatusPedido.ENTREGUE
    pedido.save()
    messages.success(request, 'Pedido entregue com sucesso')
    return redirect('/admin/main/pedido/')


@permission_required('main.fazer_pedido')
def fazer_pedido(request, beneficio_id):
    beneficio = get_object_or_404(Beneficio, id=beneficio_id)
    usuario = request.user
    valor = beneficio.pontos
    if not beneficio.estoque > 0:
        messages.error(request, 'Não existe estoque do produto')
        return redirect(beneficio.get_absolute_url())
    if valor > usuario.saldo_atual():
        messages.error(request, 'Você não possui saldo para realizar essa transação')
        return redirect(beneficio.get_absolute_url())
    pedido = Pedido(beneficio=beneficio, usuario=usuario, pontos=valor)
    try:
        pedido.save()
        beneficio.estoque -= 1
        beneficio.save()
        messages.success(request, 'Pedido realizado com sucesso')
        return redirect(pedido.get_absolute_url())
    except:
        messages.error(request, 'Não foi possível realizar o pedido')
        return redirect(pedido.get_absolute_url())


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
