from core.entities.frota_e_equipamentos import frota_e_Equipamentos_Entity,Manutencao_entity
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

class Frota_repository(ABC):
    @abstractmethod
    def buscar_veiculo_por_id(self,veiculo_id:int)->Optional[frota_e_Equipamentos_Entity]:
        pass

    @abstractmethod
    def buscar_manutencao_por_id(self,veiculo_id:int)->list[Manutencao_entity]:
        pass

    @abstractmethod
    def salvar(self,manutencao:Manutencao_entity)->Manutencao_entity:
        pass