from .models import *
from django.forms import ModelForm, ValidationError, ModelChoiceField, CharField, Textarea, PasswordInput, \
    ModelMultipleChoiceField
from django.conf import settings
from django.forms.widgets import CheckboxSelectMultiple


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'data_nascimento', 'telefone', 'endereco', 'bairro', 'cidade', 'estado']


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
