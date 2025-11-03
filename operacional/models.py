from django.db import models
from django.utils import timezone
from utils import tools_utils
from decimal import Decimal
from openpyxl import load_workbook
import os
from django.conf import settings
from django.core.exceptions import ValidationError
import pytz

# posso dividir os suprimentos e internos e externos?
# Create your models here.

# fazer o caminho dos documentos de manutençao do veiculo
# manutenção vai ficar dentro do veiculo
# ser operacional/frota/ativo/filename

class tipo_ativo(models.Model):
    tipo_de_ativo=models.CharField(max_length=20)
    def __str__(self):
        return self.tipo_de_ativo
    class Meta:
        verbose_name_plural = "Tipos  de ativo"
        verbose_name = "Tipo de ativo"


class Frota(models.Model):
    Ativo = models.CharField(max_length=20,blank=True,null=True,verbose_name='Ativo da frota')
    tipo = models.ForeignKey(tipo_ativo,on_delete=models.CASCADE,verbose_name='Tipo de ativo',related_name='frota')
    placa = models.CharField(max_length=20,blank=True,null=True)
    RENAVAN=models.CharField(max_length=20,blank=True,null=True)
    marca = models.CharField(max_length=20,blank=True,null=True)
    modelo = models.CharField(max_length=20,blank=True,null=True)
    ano = models.IntegerField(blank=True,null=True)
    tipo_combustivel = models.CharField(max_length=20,blank=True,null=True)
    situacao = models.CharField(max_length=100,blank=True,null=True,choices=(
        ("Galpao",'Parado'),('Manutenção','Manutenção'),
        ('Avariado',"Avariado"),("Operação","Operação"),("Reservado","Reservado")
    ))
    documento=models.FileField(blank=True,null=True,upload_to=tools_utils.documentos_frota_load_path,max_length=255)

    def __str__(self):
        return f' {self.Ativo}:{self.placa}'


    class Meta:
        verbose_name_plural = 'Veiculo'
        verbose_name = 'Veiculos'


    def save(self, *args, **kwargs):
        isnew=self.pk is None
        if isnew and self.documento:
            temp_documento=self.documento
            self.documento=None
            super().save(*args, **kwargs)
            self.documento=temp_documento
        super().save(*args, **kwargs)

# ser operacional/frota/ativo/manutencao/tipo/ordem/filename
class Manutencao(models.Model):
    Ativo_em_manutencao=models.ForeignKey(Frota,on_delete=models.CASCADE,
                                         related_name='manutencao',verbose_name='Ativo em manutencao')
    data_entrada_manutencao=models.DateField(blank=True,null=True)
    motivo=models.TextField(blank=True,null=True,verbose_name='Motivo',max_length=2500)
    local_de_manutencao=models.CharField(max_length=255,blank=True,null=True)
    operacao=models.CharField(max_length=255,blank=True,null=True)
    registro=models.TextField(max_length=5000,blank=True,null=True)
    custo_total=models.FloatField(blank=True,null=True)
    documentos=models.FileField(blank=True,null=True,upload_to=tools_utils.documentos_manutencao_frota_load_path)

    def __str__(self):
        return f' ordem {self.pk}-{self.Ativo_em_manutencao.Ativo}-{self.Ativo_em_manutencao.placa}'

    class Meta:
        verbose_name='Manutencao'
        verbose_name_plural='ordens de Manutenção'

    def valor_formatado(self):
        return tools_utils.formata_preco(self.custo_total)
    valor_formatado.short_description='Valor'



    def save(self, *args, **kwargs):
        isnew=self.pk is None
        if isnew and self.documentos:
            temp_documento=self.documentos
            self.documentos=None
            super().save(*args, **kwargs)
            self.documentos=temp_documento
        super().save(*args, **kwargs)


class Item_almoxarifado(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.ForeignKey(tipo_ativo, on_delete=models.CASCADE, verbose_name='Tipo_de_ativo')
    def __str__(self):
        return f' {self.nome}'

    @property
    def quantidade_total(self):
        entrada = sum(l.quantidade_entrada_nota or 0 for l in self.lotes.all())
        saida = sum(s.quantidade for s in self.itens_alocados.all())  # Usa a quantidade de itens alocados
        total_em_estoque = entrada - saida
        return total_em_estoque

    @property
    def valor_total_estoque(self):
        valor_total=sum(v.valor_total or 0 for v in self.lotes.all())
        return valor_total

    @property
    def valor_atual_estoque(self):
        entradas=sum(v.valor_total or 0 for v in self.lotes.all())
        saidas=sum(s.Valor_total_alocado or 0 for s in self.itens_alocados.all() )
        valor_atual_estoque=entradas-saidas
        return valor_atual_estoque

    def valor_atual_estoque_formatado(self):
        return tools_utils.formata_preco(self.valor_atual_estoque)
    valor_atual_estoque_formatado.short_description = 'Valor atual em estoque'


    def valor_total_estoque_formatado(self):
        return tools_utils.formata_preco(self.valor_total_estoque)
    valor_total_estoque_formatado.short_description = 'Valor Total em estoque'

    @property
    def Preco_unitario_medio(self):
        quantidade_total = sum(l.quantidade_entrada_nota or 0 for l in self.lotes.all())

        if quantidade_total > 0:
            valor_total_estoque = self.valor_total_estoque
            precomedio = valor_total_estoque / quantidade_total
            return precomedio
        return None

    def valor_untario_formatado(self):
        return tools_utils.formata_preco(self.Preco_unitario_medio)
    valor_untario_formatado.short_description='Valor Unitario medio'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'


class lote(models.Model):
    item=models.ForeignKey(Item_almoxarifado,related_name='lotes',on_delete=models.CASCADE,verbose_name='Item almoxarifado')
    nota=models.CharField(blank=True,null=True,max_length=100)
    fornecedor=models.CharField(blank=True,null=True,max_length=100)
    data_entrada=models.DateField(blank=True,null=True,default=timezone.now)
    valor_unitario=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2)
    quantidade_entrada_nota=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2)
    valor_total=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2,editable=False)
    Nf=models.FileField(upload_to=tools_utils.documentos_amoxarifado_load_path)

    def __str__(self):
        return f' lote {self.nota}-{self.fornecedor} '

    class Meta:
        verbose_name='Lote'
        verbose_name_plural='lotes'

    def save(self, *args, **kwargs):
        isnew=self.pk is None
        if isnew and self.Nf:
            temp_documento=self.Nf
            self.Nf=None
            super().save(*args, **kwargs)
            self.Nf=temp_documento

        if self.valor_unitario >0 and self.quantidade_entrada_nota>0:
            self.valor_total=self.valor_unitario*self.quantidade_entrada_nota
        super().save(*args, **kwargs)



# class Historico_almoxarifado(models.Model):
#     item_almoxarifado=models.ForeignKey(Item_almoxarifado,on_delete=models.CASCADE,verbose_name='Itemalmoxarifado')
#     pedido=models.

# duvida o calculo dos custo deve ser feito pelo preço medio ou pelo preço atualk?
#fazer na segunda ou terça a migraçaõ














