from django.contrib import admin
from django.utils.safestring import mark_safe
from django_bootstrap_icons.templatetags.bootstrap_icons import bs_icon
from django_middleware_global_request import get_request

from main.forms import ClienteForm, UsuarioForm
from main.models import Cliente, Usuario
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
        pode_visualizar = user.has_perm('main.view_imovel')
        pode_editar = user.has_perm('main.change_imovel')
        return links_no_admin(obj, pode_visualizar, pode_editar)

    get_links.short_description = '#'
    get_links.allow_tags = True

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
