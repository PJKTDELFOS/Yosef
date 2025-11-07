from decimal import Decimal,InvalidOperation
from typing import List,Optional
from core.entities.almoxarifado import TipoAtivoEntity,LoteEntity,Item_alocadoEntity,Item_almoxarifadoEntity
from core.ports.almoxarifado_repository import AlmoxarifadoRepository
import datetime

from dataclasses import replace


class CalculoItemEstoqueUsecase:

    '''
    definir
    1-quantidade_total do item no estoque somando todos os lotes daquele item

    2-definir o preço medio unitario dos itens no estoque pela  divisao da soma dos valores totais dos lotes pela divisao da quantidade total

    3-o valor unitario-medio so pode ser alterado com entradas de novos lotes

    a saide de um item especifico para um pedido sera  o preco medio unitario x a quantidade a ser alocada
    a saida total vai ser a soma dos itens alocados x  preço medio unitario

    '''
    def __init__(self, repositorio: AlmoxarifadoRepository):
        self.repositorio = repositorio


    def quantidade_total_entrada_em_estoque_por_item_id(self,item_id:int)->Decimal:
        lotes:List[LoteEntity]=self.repositorio.buscar_lotes_por_item_id(item_id)
        quantidade_total_entrada=sum(
            (i.quantidade_entrada for i in lotes),Decimal('0.00'))
        return  quantidade_total_entrada


    def valor_total_entrada_em_estoque_por_item_id(self,item_id:int)->Decimal:
        lotes: List[LoteEntity] = self.repositorio.buscar_lotes_por_item_id(item_id)
        valor_total_entrada = sum(
            (l.valor_total for l in lotes), Decimal('0.00')
        )
        return valor_total_entrada




    def quantidade_disponivel_estoque(self,item_id:int)->Decimal:
        entradas=self.quantidade_total_entrada_em_estoque_por_item_id(item_id)
        saidas=self.repositorio.calcular_saida_total_por_item_id(item_id)
        quantidade_disponivel=entradas-saidas
        if  quantidade_disponivel <Decimal('0.00'):
            return Decimal('0.00').quantize(Decimal('0.00'))
        return quantidade_disponivel



    def preco_unitario_medio_por_item_id(self,item_id:int)->Decimal:
        quantidade_estoque=self.quantidade_total_entrada_em_estoque_por_item_id(item_id)
        valor_total=self.valor_total_entrada_em_estoque_por_item_id(item_id)
        preco_medio_unitario=valor_total/quantidade_estoque
        return preco_medio_unitario.quantize(Decimal('0.00'))

    def valor_total_estoque_por_item_id(self,item_id:int)->Decimal:
        quantidade_estoque=self.quantidade_disponivel_estoque(item_id)
        preco_unitario_medio=self.preco_unitario_medio_por_item_id(item_id)
        valor_total_estoque=quantidade_estoque*preco_unitario_medio
        return valor_total_estoque.quantize(Decimal('0.00'))




class RegistroDeAlocacaoUseCase:

    def __init__(self,repositorio:AlmoxarifadoRepository):
        self.repo=repositorio

    def registrar(self,item_id:int,pedido_id:int,quantidade_alocada:Decimal):
        estoque_disponivel=CalculoItemEstoqueUsecase(repositorio=self.repo).quantidade_disponivel_estoque(item_id)
        if quantidade_alocada>estoque_disponivel:
            raise ValueError(
                f'Estoque disponível de {estoque_disponivel} é inferior à quantidade solicitada: {quantidade_alocada}.'
            )
        nova_alocacao=Item_alocadoEntity(
            item_alocado_id=item_id,
            quantidade=quantidade_alocada,
            pedido_id=pedido_id,
            data_alocacao=datetime.date.today()
        )
        alocacao_confirmada=self.repo.salvar_alocacao(nova_alocacao)
        return alocacao_confirmada


