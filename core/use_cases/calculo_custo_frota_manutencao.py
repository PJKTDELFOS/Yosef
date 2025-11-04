from decimal import Decimal
from typing import List
from core.ports.frota_repository import FrotaRepository
from core.entities.frota_e_equipamentos import VeiculosEntity, ManutencaoEntity
from dataclasses import replace


class CalculoCustoManutencaoUsecase:

    def __init__(self, repo:FrotaRepository):
        self.repo = repo


    def calculo_custo_total_manutencoes_frota_equipamentos(self,veiculo_id:int)->Decimal:
        manutencoes:List[ManutencaoEntity]=self.repo.buscar_manutencao_por_veiculo_id(veiculo_id)
        custo_total=sum((m.custo_manutencao for m in manutencoes),Decimal('0.00'))
        return custo_total.quantize(Decimal('0.00'))

    #mais a frente implementar  custos mais detalhados, conforme necessidades dos clientes


class AtualizarCustoFrotaUsecase:
    def __init__(self, repo:FrotaRepository,calculo:CalculoCustoManutencaoUsecase):
        self.repo = repo
        self.calculo = calculo


    def execute(self,veiculo_id:int):
        veiculo:VeiculosEntity=self.repo.buscar_veiculo_por_id(veiculo_id)
        if not veiculo:
            raise ValueError(f'Veiculo {veiculo_id} nao encontrado')

        novo_custo=self.calculo.calculo_custo_total_manutencoes_frota_equipamentos(veiculo_id)
        veiculo_atualizado=replace(veiculo,custo_total_de_manutencao=novo_custo)
        veiculo_salv0=self.repo.salvar_veiculo(veiculo_atualizado)
        return veiculo_salv0


class RegistroManutencao:

    def __init__(self, repo:FrotaRepository,calculo:CalculoCustoManutencaoUsecase):
        self.repo = repo
        self.calculo = calculo

    def execute(self,nova_manutencao:ManutencaoEntity)->ManutencaoEntity:
        manutencao_salva=self.repo.salvar_manutencao(nova_manutencao)
        veiculo_id=manutencao_salva.veiculo_id
        novo_custo_total=self.calculo.calculo_custo_total_manutencoes_frota_equipamentos(veiculo_id)
        veiculo :VeiculosEntity=self.repo.buscar_veiculo_por_id(veiculo_id)
        if not veiculo:
            raise ValueError(f'Veiculo {veiculo_id} nao encontrado')
        veiculo_atualizado=replace(veiculo,custo_total_de_manutencao=novo_custo_total)

        self.repo.salvar_veiculo(veiculo_atualizado)
        return manutencao_salva




