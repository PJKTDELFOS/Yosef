from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .import models
from .models import cadastrofuncionario,Usuario_sistema


@receiver(post_save,sender=cadastrofuncionario)
def criar_usuario(sender,instance,created,**kwargs):
    if created:
        usuario=User.objects.create_user(username=instance.nomecompleto,password=instance.cpf)
        Usuario_sistema.objects.create(funcionario=instance,usuario=usuario)



#a,manha definir aqui a rota do grupo para onde  vai