from dataclasses import dataclass,field
from decimal import Decimal
from typing import Optional
import  datetime

ID_TYPE=Optional[int]

@dataclass(frozen=True)
class VeiculosEntity:
    tipo_id:int
    id:ID_TYPE=None
    Ativo:Optional[str]=None
    placa:Optional[str]=None
    RENAVAN:Optional[str]=None
    marca:Optional[str]=None
    modelo:Optional[str]=None
    ano:Optional[int]=None
    tipo_combustivel:Optional[str]=None
    situacao:Optional[str]=None
    custo_total_de_manutencao: Decimal = Decimal('0.00')


@dataclass(frozen=True)
class ManutencaoEntity:
    veiculo_id:int
    id:ID_TYPE=None
    motivo:Optional[str]=None
    local_manutencao:Optional[str]=None
    operacao:Optional[str]=None
    registro:Optional[str]=None
    custo_manutencao : Decimal=Decimal('0.00')








'''

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

'''
