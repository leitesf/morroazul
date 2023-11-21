from collections.abc import Mapping
from typing import Any
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from django.forms import ModelForm, ValidationError, ModelChoiceField, CharField, Textarea, PasswordInput, \
    ModelMultipleChoiceField
from django.conf import settings
from django.forms.widgets import CheckboxSelectMultiple


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'nome_fantasia', 'cpf', 'cnpj', 'email', 'data_nascimento', 'telefone', 'endereco', 'cidade', 'estado']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if self.data.get('cnpj') and cpf:
            raise ValidationError(u'Informe somente um documento de identificação')
        if not self.data.get('cnpj') and not cpf:
            raise ValidationError(u'Informe pelo menos um documento de identificação')
        return self.cleaned_data['cpf']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if self.data.get('cpf') and cnpj:
            raise ValidationError(u'Informe somente um documento de identificação')
        if not self.data.get('cpf') and not cnpj:
            raise ValidationError(u'Informe pelo menos um documento de identificação')
        return self.cleaned_data['cnpj']


class TransportadorForm(ModelForm):
    class Meta:
        model = Transportador
        fields = ['nome', 'cpf', 'cnpj', 'email', 'data_nascimento', 'telefone', 'endereco', 'cidade', 'estado']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if self.data.get('cnpj') and cpf:
            raise ValidationError(u'Informe somente um documento de identificação')
        return self.cleaned_data['cpf']

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if self.data.get('cpf') and cnpj:
            raise ValidationError(u'Informe somente um documento de identificação')
        return self.cleaned_data['cnpj']


class NotaFiscalForm(ModelForm):
    class Meta:
        model = NotaFiscal
        fields = ['numero', 'data', 'produto', 'toneladas', 'valor_produtos', 'valor_frete', 'km', 'cliente', 'transportador', 'vendedor']

    def __init__(self, *args, **kwargs):
        super(NotaFiscalForm, self).__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = Usuario.objects.filter(groups=Group.objects.get(name='Vendedor'))
        self.fields['vendedor'].widget.can_add_related = False
        self.fields['vendedor'].widget.can_change_related = False
        self.fields['vendedor'].widget.can_delete_related = False


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'contato', 'data_nascimento', 'groups', 'is_active', 'is_superuser' ]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UsuarioForm, self).save(commit=False)

        if not user.pk:
            user.set_password(settings.DEFAULT_PASSWORD) #Set de default password
            user.is_staff = True
        if commit:
            user.save()
        return user


class PasswordForm(ModelForm):
    senha = CharField(widget=PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super(PasswordForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
