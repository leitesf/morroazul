from django.apps import AppConfig
from django.db.models.signals import pre_save
from main.signals import definir_pontuacao


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        notafiscal = self.get_model('NotaFiscal')
        pre_save.connect(definir_pontuacao, sender=notafiscal)
