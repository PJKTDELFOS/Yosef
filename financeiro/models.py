from django.db import models
from processos.models import Pedidos
from utils import tools_utils
from django.utils import timezone
# Create your models here.

class Centro_de_custo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Centro de Custo'
        verbose_name_plural = 'Centros de Custo'

class Contas_a_pagar(models.Model):
    conta=models.CharField(max_length=100)
    Centrodecusto = models.ForeignKey(
        Centro_de_custo, on_delete=models.CASCADE,related_name='centrodecusto',verbose_name='Centro de Custo')
    vencimento = models.DateField(default=timezone.now,blank=True,null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    credor = models.CharField(max_length=100)
    origem = models.CharField(max_length=100)
    data_de_criacao = models.DateField(auto_now_add=True)
    descricao = models.TextField()
    nota_fiscal_compra = models.CharField(max_length=100,verbose_name='nota fiscal')
    numero_de_parcelas = models.IntegerField(default=1)
    valor_das_parcelas = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(default=None, max_length=250, null=True,choices=(
        ('A vencer','A vencer'),('Vencida','Vencida'),
    ),verbose_name='status')
    ocorrencias = models.TextField()
    documentos = models.FileField(upload_to=tools_utils.docs_finan_load_path,null=True,blank=True)
    banco=models.CharField(max_length=100)
    agencia=models.CharField(max_length=100)
    conta_corrente=models.CharField(max_length=100)

    def __str__(self):
        return self.conta

    class Meta:
        verbose_name = 'Conta a pagar'
        verbose_name_plural = 'Contas a pagar'

    def save(self, *args, **kwargs):
        is_new=self.pk is None
        if is_new and self.documentos:
            temp_docs=self.documentos
            self.documentos=None
            super().save(*args, **kwargs)
            self.documentos=temp_docs
        super().save(*args, **kwargs)

class Contas_a_receber(models.Model):
    cobrança = models.CharField(max_length=100)
    origem = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    contrato = models.CharField(max_length=100)
    nota_fiscal = models.CharField(max_length=100)
    valor_total_do_pedido = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    data_cobranca = models.DateField()
    data_pgto = models.DateField()
    status = models.CharField(default=None, max_length=250, null=True,choices=(
        ('enviado','enviado'),('Vencida','Vencida'),('pago','pago'),
    ),verbose_name='status')
    tipo_documento = models.CharField(max_length=100)
    arquivos = models.FileField(upload_to=tools_utils.docs_finan_load_path_rcbm,null=True,blank=True)

    def __str__(self):
        return self.cobrança

    class Meta:
        verbose_name = 'Conta a receber'
        verbose_name_plural = 'Contas a receber'

    def save(self, *args, **kwargs):
        is_new=self.pk is None
        if is_new and self.arquivos:
            temp_docs=self.arquivos
            self.arquivos=None
            super().save(*args, **kwargs)
            self.arquivos=temp_docs
        super().save(*args, **kwargs)