def definir_pontuacao(sender, instance, **kwargs):
    if instance.id is not None:
        pass
    else:
        instance.pontuacao_cliente = 5
        instance.pontuacao_transportador = 5
