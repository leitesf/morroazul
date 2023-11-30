def definir_pontuacao(sender, instance, **kwargs):
    if instance.id is not None:
        pass
    else:
        instance.pontuacao_cliente = instance.get_valor_cliente()
