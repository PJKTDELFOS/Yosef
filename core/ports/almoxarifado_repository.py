from abc import ABC, abstractmethod
from typing import List,Optional
from decimal import Decimal

from core.entities.almoxarifado import (
TipoAtivoEntity,
Item_almoxarifadoEntity,
LoteEntity,
Item_alocadoEntity
)

class AlmoxarifadoRepository(ABC):

    @abstractmethod
    def buscar_item_por_id(self,item_id:int)->Optional[Item_almoxarifadoEntity]:
        pass

    @abstractmethod
    def buscar_lotes_por_item_id(self,item_id:int)->List[LoteEntity]:
        pass

    @abstractmethod
    def calcular_saida_total_por_item_id(self,item_id:int)->Decimal:
        pass

    @abstractmethod
    def salvar_lote(self,lote:LoteEntity)->LoteEntity:
        pass
