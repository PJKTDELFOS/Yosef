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
    tipo_ativo_id: Optional[int] = None
    item_id: ID_TYPE=None
    nome: Optional[str]=None




'''
  obs 1: poderia add comportamento de saida no item, uma vez que ele vai ter a soma dos lotes
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
    item_estoque_id:int
    item_alocado_id: ID_TYPE=None
    data_alocacao:Optional[datetime.date]=None
    quantidade:Decimal=Decimal('0.00')


