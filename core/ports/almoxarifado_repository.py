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
    def buscar_tipo_ativo_por_id(self,id:int)->Optional[TipoAtivoEntity]:
        pass

    # @abstractmethod
    # def busccar_item_alocado_por_item_id(self,item_alocado_id:int)->List[Item_alocadoEntity]:
    #     pass

    # @abstractmethod
    # def calcular_saida_por_item_id(self,item_id:int)->Decimal:
    #     pass #para calcular a saida para os pedidos  de forma individual

    @abstractmethod
    def calcular_saida_total_por_item_id(self,item_id:int)->Decimal:
        pass


    @abstractmethod
    def salvar_lote(self,lote:LoteEntity)->LoteEntity:
        pass

    @abstractmethod
    def salvar_item(self,item:Item_almoxarifadoEntity)->Item_almoxarifadoEntity:
        pass

    @abstractmethod
    def salvar_alocacao(self,item_alocado:Item_alocadoEntity)->Item_alocadoEntity:
        pass

    @abstractmethod
    def salvar_tipo_ativo(self,tipo_ativo:TipoAtivoEntity)->TipoAtivoEntity:
        pass
