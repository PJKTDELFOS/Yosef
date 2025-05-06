from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Pedidos, ItemAlocado,Contratos


@receiver([post_save,post_delete], sender=ItemAlocado)
def atualizar_custo_total_pedido(sender,instance, **kwargs):
    # o acesso e feito pelo related name da classe que voce quer acessar
    pedido=instance.pedido
    total = sum(item.Valor_total_alocado or 0 for item in pedido.itens_alocados.all())
    pedido.custo_total = total
    pedido.save()

    contrato=pedido.contrato
    total_contrato=sum(pedido.custo_total or 0 for pedido in contrato.pedidos.all())
    contrato.custo_total_contrato=total_contrato
    contrato.save()