# from django.db.models.signals import post_save, post_delete,pre_save
# from django.dispatch import receiver
# from processos.models import ItemAlocado
#
#
# @receiver(pre_save, sender=ItemAlocado)
# def salvar_quantidade_anterior(sender, instance, *args, **kwargs):
#     if instance.pk:
#         instance._quantidade_anterior=ItemAlocado.objects.get(pk=instance.pk)
#     else:
#         instance._quantidade_anterior=0
#
#
# @receiver(post_save, sender=ItemAlocado)
# def atualizar_estoque(sender, instance, created, **kwargs):
#     item=instance.item_alocado
#     nova=instance.quantidade or 0
#     anterior=getattr(instance, '_quantidade_anterior', 0) or 0
#     diferenca=nova-anterior
#     item.quantidade_total-=diferenca
#     item.save()
#
# @receiver(post_delete, sender=ItemAlocado)
# def devolver_estoque_apos_deletar(sender, instance, **kwargs):
#     item = instance.item_alocado
#     item.quantidade += instance.quantidade or 0
#     item.save()