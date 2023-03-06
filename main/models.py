from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRStateField


class Pessoa(models.Model):
    nome = models.CharField("Nome", max_length=100)
    telefone = models.CharField("Telefone", max_length=100)
    endereco = models.CharField("Endereço", max_length=100)
    bairro = models.CharField("Bairro", max_length=100)
    cidade = models.CharField("Cidade", max_length=100)
    estado = BRStateField("Estado")
    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)
    email = models.EmailField("E-Mail")

    class Meta:
        abstract = True


class Cliente(Pessoa):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return '/cliente/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/cliente/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/cliente/{}/delete/'.format(self.id)


class Transportador(Pessoa):
    class Meta:
        verbose_name = 'Transportador'
        verbose_name_plural = 'Transportadores'
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return '/transportador/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/transportador/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/transportador/{}/delete/'.format(self.id)


class NotaFiscal(models.Model):
    numero = models.CharField("Número", max_length=100, unique=True)
    item = models.CharField("Item", max_length=100)
    descricao = models.CharField("Descrição", max_length=100)
    valor = models.DecimalField("Valor", decimal_places=2, max_digits=13)
    km = models.IntegerField("Distância em Km")
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.RESTRICT)
    transportador = models.ForeignKey(Transportador, null=True, blank=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ["numero"]

    def __str__(self):
        return 'NF {}'.format(self.numero)

    def get_absolute_url(self):
        return '/notafiscal/{}'.format(self.id)

    def get_edit_url(self):
        return '/admin/main/notafiscal/{}/change/'.format(self.id)

    def get_delete_url(self):
        return '/admin/main/notafiscal/{}/delete/'.format(self.id)


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
