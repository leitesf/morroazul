from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from django_middleware_global_request import get_request
from solo.admin import SingletonModelAdmin

from main.forms import ClienteForm, UsuarioForm, TransportadorForm, NotaFiscalForm
from main.models import Cliente, Usuario, NotaFiscal, Transportador, ConfiguracaoPontuacao, Beneficio, Pedido
from main.utils import links_no_admin


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'nome', 'telefone', 'bairro', 'cidade', 'estado')
    search_fields = ('nome', 'telefone', 'bairro', 'cidade', 'estado')
    ordering = ('nome',)
    list_filter = ('bairro', 'cidade', 'estado')
    list_display_links = None

    form = ClienteForm

    def get_links(self, obj):
        user = get_request().user
        pode_visualizar = user.has_perm('main.view_cliente')
        pode_editar = user.has_perm('main.change_cliente')
        return links_no_admin(obj, pode_visualizar, pode_editar)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class TransportadorAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'nome', 'telefone', 'bairro', 'cidade', 'estado')
    search_fields = ('nome', 'telefone', 'bairro', 'cidade', 'estado')
    ordering = ('nome',)
    list_filter = ('bairro', 'cidade', 'estado')
    list_display_links = None

    form = TransportadorForm

    def get_links(self, obj):
        user = get_request().user
        pode_visualizar = user.has_perm('main.view_transportador')
        pode_editar = user.has_perm('main.change_transportador')
        return links_no_admin(obj, pode_visualizar, pode_editar)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'numero', 'item', 'valor', 'km', 'cliente', 'pontuacao_cliente', 'transportador', 'pontuacao_transportador')
    search_fields = ('numero', 'item')
    ordering = ('numero',)
    list_filter = ('cliente', 'transportador')
    list_display_links = None

    form = NotaFiscalForm

    def get_links(self, obj):
        user = get_request().user
        pode_visualizar = user.has_perm('main.view_notafiscal')
        pode_editar = user.has_perm('main.change_notafiscal')
        return links_no_admin(obj, pode_visualizar, pode_editar)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class BeneficioAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'nome', 'possui_estoque', 'pontos')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)
    list_display_links = None

    def get_links(self, obj):
        user = get_request().user
        pode_visualizar = user.has_perm('main.view_beneficio')
        pode_editar = user.has_perm('main.change_beneficio')
        pode_comprar = user.has_perm('main.fazer_pedido') and 0 < obj.estoque < user.saldo_atual()
        return links_no_admin(obj, pode_visualizar, pode_editar, pode_comprar)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def possui_estoque(self, obj):
        return "Sim" if obj.estoque > 0 else "Não"

    possui_estoque.short_description = 'Disponível?'
    possui_estoque.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'usuario', 'beneficio', 'pontos', 'data', 'get_status')
    search_fields = ('usuario', 'beneficio')
    ordering = ('status',)
    list_filter = ('status', 'beneficio',)
    list_display_links = None

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('main.aprovar_pedido') or request.user.has_perm('main.entregar_pedido'):
            return qs
        else:
            return qs.filter(usuario=request.user)

    def get_links(self, obj):
        user = get_request().user
        pode_visualizar = user.has_perm('main.view_pedido')
        return links_no_admin(obj, pode_visualizar, None)

    get_links.short_description = '#'
    get_links.allow_tags = True

    def get_status(self, obj):
        classe, status = obj.get_status_formatado()
        return mark_safe("<span class='badge bg-{}'>{}</span>".format(classe, status))

    get_status.short_description = 'Situação'
    get_status.allow_tags = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('get_links', 'get_nome', 'username', 'email', 'contato', 'get_grupos', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    list_display_links = None
    form = UsuarioForm

    def get_nome(self, obj):
        return obj.get_full_name()

    get_nome.short_description = 'Nome'
    get_nome.admin_order_field = ["first_name"]

    def get_grupos(self, obj):
        return ', '.join(obj.groups.values_list('name', flat=True))

    get_grupos.short_description = 'Grupos'

    def get_links(self, obj):
        links = ""
        links += "<a class='text-reset text-decoration-none' href='{}' title='Editar'>{}</a>".format(obj.get_edit_url(), bs_icon('pencil-square'))
        links += "<a class='text-reset text-decoration-none' href='{}' title='Alterar Senha'>{}</a>".format( '/usuario/{}/alterar_senha/'.format(obj.id), bs_icon('key'))
        return mark_safe(links)

    get_links.short_description = '#'
    get_links.allow_tags=True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(NotaFiscal, NotaFiscalAdmin)
admin.site.register(Transportador, TransportadorAdmin)
admin.site.register(Beneficio, BeneficioAdmin)
admin.site.register(ConfiguracaoPontuacao, SingletonModelAdmin)
admin.site.register(Pedido, PedidoAdmin)
