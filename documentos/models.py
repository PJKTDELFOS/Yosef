from django.db import models
from processos.models import Pedidos
from utils import tools_utils
from django.utils import timezone

# Create your models here.


class Documentos(models.Model):
    documento=models.CharField(max_length=100,null=True,blank=True)
    numero=models.CharField(max_length=100,null=True,blank=True)
    pedido_origem=models.CharField(max_length=100,null=True,blank=True,choices=(
        ('comercial','comercial'),('financeiro','financeiro'),('RH','RH'),
        ('Produção','Produção'),("Administrador","Administrador"),
    ))
    emissor=models.CharField(max_length=100,null=True,blank=True)
    sitio_emissor=models.CharField(max_length=255,null=True,blank=True)
    tipo_documento=models.CharField(max_length=255,null=True,blank=True,choices=(
        ('certidao','Certidao'),('licença','licença'),('declração','declaração')
    ))
    data_emissao=models.DateField(null=True,blank=True,default=timezone.now)
    data_vencimento=models.DateField(null=True,blank=True)
    arquivo=models.FileField(null=True,blank=True,upload_to=tools_utils.documentos_load_path)

    def __str__(self):
        return self.documento


    class Meta:
        verbose_name_plural = 'documentos'
        verbose_name = 'documento'

    def save(self, *args, **kwargs):
        isnew=self.pk is None
        if isnew and self.arquivo:
            temp_arquivo=self.arquivo
            self.arquivo=None
            super().save(*args, **kwargs)
            self.arquivo=temp_arquivo
        super().save(*args, **kwargs)


