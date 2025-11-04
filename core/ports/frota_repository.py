from core.entities.frota_e_equipamentos import VeiculosEntity,ManutencaoEntity
from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

class FrotaRepository(ABC):
    @abstractmethod
    def buscar_veiculo_por_id(self,veiculo_id:int)->Optional[VeiculosEntity]:
        pass

    @abstractmethod
    def buscar_manutencao_por_veiculo_id(self,veiculo_id:int)->list[ManutencaoEntity]:
        pass

    @abstractmethod
    def salvar_veiculo(self,veiculo:VeiculosEntity)->VeiculosEntity:
        pass

    @abstractmethod
    def salvar_manutencao (self, manutencao:ManutencaoEntity)->ManutencaoEntity:
        pass