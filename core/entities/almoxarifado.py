from dataclasses import dataclass,field
from decimal import Decimal
from typing import Optional
import  datetime


ID_TYPE=Optional[int]


@dataclass(frozen=True)
class TipoAtivoEntity:
    id: ID_TYPE=None
    tipo_de_ativo: Optional[str]=None


@dataclass(frozen=True)
class Item_almoxarifadoEntity:
    tipo_id: Optional[int] = None
    id: ID_TYPE=None
    nome: Optional[str]=None




'''
    item=models.ForeignKey(Item_almoxarifado,related_name='lotes',on_delete=models.CASCADE,verbose_name='Item almoxarifado')
    nota=models.CharField(blank=True,null=True,max_length=100)
    fornecedor=models.CharField(blank=True,null=True,max_length=100)
    data_entrada=models.DateField(blank=True,null=True,default=timezone.now)
    valor_unitario=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2)
    quantidade_entrada_nota=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2)
    valor_total=models.DecimalField(blank=True,null=True,max_digits=10,decimal_places=2,editable=False)
    Nf=models.FileField(upload_to=tools_utils.documentos_amoxarifado_load_path)
'''


@dataclass(frozen=True)
class LoteEntity:
    item_id: int
    id:ID_TYPE=None
    nota: Optional[str]=None
    fornecedor:Optional[str]=None
    data_entrada:Optional[datetime.date]=None
    valor_unitario:Decimal=Decimal('0.00')
    quantidade_entrada:Decimal=Decimal('0.00')


    @property
    def valor_total(self)->Decimal:
        return self.valor_unitario * self.quantidade_entrada




@dataclass(frozen=True)
class Item_alocadoEntity:
    pedido_id: int
    item_alocado_id:int
    id: ID_TYPE=None
    data_alocacao:Optional[datetime.date]=None
    quantidade:Decimal=Decimal('0.00')


