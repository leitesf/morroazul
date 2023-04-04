from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from localflavor.br.models import BRStateField, BRCNPJField, BRCPFField
from solo.models import SingletonModel

from main.utils import badge_status


class Pessoa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    cpf = BRCPFField("CPF", blank=True, null=True)
    cnpj = BRCNPJField("CNPJ", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=100)
    endereco = models.CharField("Endereço", max_length=100)
    bairro = models.CharField("Bairro", max_length=100)
    cidade = models.CharField("Cidade", max_length=100)
    estado = BRStateField("Estado")
    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)
    email = models.EmailField("E-Mail")
    usuario = models.ForeignKey('main.Usuario', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def get_doc_oficial(self):
        return self.cpf if self.cpf else self.cnpj


class Cliente(Pessoa):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ["nome"]
        permissions = [
            (
                "nfs_cliente",
                "Pode visualizar as próprias notas fiscais como cliente"
            )
        ]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return '/cliente/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/cliente/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/cliente/{}/delete/'.format(self.id)

    def get_pontuacao_total(self):
        if self.notafiscal_set.exists():
            return self.notafiscal_set.aggregate(Sum('pontuacao_cliente'))['pontuacao_cliente__sum']
        else:
            return 0


@receiver(pre_save, sender=Cliente)
def criar_usuario(sender, instance, **kwargs):
    grupo_usuario = Group.objects.get(name='Cliente')
    if not instance.usuario:
        if not Usuario.objects.filter(username=instance.get_doc_oficial()):
            usuario = Usuario.criar_usuario(instance, grupo_usuario)
        else:
            usuario = Usuario.objects.get(username=instance.get_doc_oficial())
            usuario.atualizar_usuario(instance, grupo_usuario)
        instance.usuario = usuario
    else:
        instance.usuario.atualizar_usuario(instance)


class Transportador(Pessoa):
    class Meta:
        verbose_name = 'Transportador'
        verbose_name_plural = 'Transportadores'
        ordering = ["nome"]
        permissions = [
            (
                "nfs_transportador",
                "Pode visualizar as próprias notas fiscais como transportador"
            )
        ]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return '/transportador/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/transportador/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/transportador/{}/delete/'.format(self.id)

    def get_pontuacao_total(self):
        if self.notafiscal_set.exists():
            return self.notafiscal_set.aggregate(Sum('pontuacao_transportador'))['pontuacao_transportador__sum']
        else:
            return 0


@receiver(pre_save, sender=Transportador)
def criar_usuario(sender, instance, **kwargs):
    grupo_usuario = Group.objects.get(name='Transportador')
    if not instance.usuario:
        if not Usuario.objects.filter(username=instance.get_doc_oficial()):
            usuario = Usuario.criar_usuario(instance, grupo_usuario)
        else:
            usuario = Usuario.objects.get(username=instance.get_doc_oficial())
            usuario.atualizar_usuario(instance, grupo_usuario)
        instance.usuario = usuario
    else:
        instance.usuario.atualizar_usuario(instance)


class NotaFiscal(models.Model):
    numero = models.CharField("Número", max_length=100, unique=True)
    item = models.CharField("Item", max_length=100)
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor", decimal_places=2, max_digits=13)
    km = models.IntegerField("Distância em Km")
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.RESTRICT)
    transportador = models.ForeignKey(Transportador, null=True, blank=True, on_delete=models.RESTRICT)
    pontuacao_cliente = models.IntegerField("Pontuação do Cliente")
    pontuacao_transportador = models.IntegerField("Pontuação do Transportador")

    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ["numero"]

    def __str__(self):
        return 'NF {}'.format(self.numero)

    def get_absolute_url(self):
        return '/nota_fiscal/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/notafiscal/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/notafiscal/{}/delete/'.format(self.id)

    def get_valor_cliente(self):
        return int(self.valor/ConfiguracaoPontuacao.objects.get().reais_por_ponto)

    def get_valor_transportador(self):
        return int(self.km/ConfiguracaoPontuacao.objects.get().kms_por_ponto)


class Beneficio(models.Model):
    nome = models.CharField("Nome", max_length=50)
    descricao = models.CharField("Descrição", max_length=100)
    estoque = models.IntegerField("Estoque")
    pontos = models.IntegerField("Valor em pontos")
    foto = models.ImageField("Foto")

    class Meta:
        verbose_name = 'Benefício'
        verbose_name_plural = 'Benefícios'
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return '/beneficio/{}'.format(self.id)

    def get_buy_url(self):
        return '/beneficio/{}/pedir'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/beneficio/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/beneficio/{}/delete/'.format(self.id)


class Usuario(AbstractUser):
    contato = models.CharField("Contato", max_length=100)
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name()

    def get_edit_url(self):
        return '/admin/main/usuario/{}/change/'.format(self.id)

    @classmethod
    def criar_usuario(cls, pessoa, grupo_usuario):
        usuario = cls.objects.create(
            username=pessoa.get_doc_oficial(),
            first_name=pessoa.nome.split(' ')[:1][0],
            last_name=' '.join(pessoa.nome.split(' ')[1:]),
            email=pessoa.email,
            contato=pessoa.telefone,
            data_nascimento=pessoa.data_nascimento,
            is_staff=True
        )
        usuario.set_password(pessoa.get_doc_oficial())
        if grupo_usuario not in usuario.groups.all():
            usuario.groups.add(grupo_usuario)
        usuario.save()
        return usuario

    def atualizar_usuario(self, pessoa, grupo_usuario):
        self.first_name = pessoa.nome.split(' ')[:1][0]
        self.last_name = ' '.join(pessoa.nome.split(' ')[1:])
        self.email = pessoa.email
        self.contato = pessoa.telefone
        self.data_nascimento = pessoa.data_nascimento
        if grupo_usuario not in self.groups.all():
            self.groups.add(grupo_usuario)
        self.save()

    def pontos_recebidos(self):
        pontos=0
        for cliente in self.cliente_set.all():
            pontos += cliente.get_pontuacao_total()
        for transportador in self.transportador_set.all():
            pontos += transportador.get_pontuacao_total()
        return pontos

    def pontos_gastos(self):
        return self.pedido_set.exclude(status=StatusPedido.CANCELADO).aggregate(Sum('pontos'))['pontos__sum'] or 0

    def saldo_atual(self):
        return self.pontos_recebidos() - self.pontos_gastos()


class ConfiguracaoPontuacao(SingletonModel):
    kms_por_ponto = models.IntegerField(
        "KMs por Ponto",
        default=100,
        help_text="Quantos KM serão necessários para gerar 1 ponto pro transportador."
    )
    reais_por_ponto = models.IntegerField(
        "Reais por Ponto",
        default=100,
        help_text="Quantos reais serão necessários para gerar 1 ponto pro cliente."
    )

    def __str__(self):
        return "Configuração de Pontos"

    class Meta:
        verbose_name = "Configuração de Pontos"


class StatusPedido:
    PENDENTE = '1'
    APROVADO = '2'
    ENTREGUE = '3'
    CANCELADO = '99'

    TIPOS = ((PENDENTE, 'Pendente'), (APROVADO, 'Aprovado'), (CANCELADO, 'Cancelado'), (ENTREGUE, 'Entregue'))

    @classmethod
    def get_status(cls, status):
        for tipo in cls.TIPOS:
            if tipo[0]==status:
                return tipo[1]


class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    beneficio = models.ForeignKey(Beneficio, on_delete=models.CASCADE)
    pontos = models.IntegerField("Pontos gastos")
    data = models.DateField("Data", auto_now_add=True)
    status = models.CharField("Situação", choices=StatusPedido.TIPOS, max_length=2, default=StatusPedido.PENDENTE)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ["-data"]
        permissions = [
            (
                "fazer_pedido",
                "Pode criar um pedido"
            ),
            (
                "aprovar_pedido",
                "Pode aprovar um pedido"
            ),
            (
                "entregar_pedido",
                "Pode entregar um pedido"
            )
        ]

    def __str__(self):
        return '{} - {}'.format(self.usuario, self.beneficio)

    def get_absolute_url(self):
        return '/pedido/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/pedido/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/pedido/{}/delete/'.format(self.id)

    def get_status_formatado(self):
        return badge_status(self.status)

    def cancelado(self):
        return True if self.status == StatusPedido.CANCELADO else False
