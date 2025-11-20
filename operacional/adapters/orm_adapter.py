
from core.entities.almoxarifado import (
TipoAtivoEntity,
Item_almoxarifadoEntity,
LoteEntity,
Item_alocadoEntity
)
from core.ports.almoxarifado_repository import AlmoxarifadoRepository
from core.ports.frota_repository import FrotaRepository

from operacional.models import (
lote as LoteModel,
Item_almoxarifado as ItemAlmoxarifadoModel,
Manutencao as ManutencaoModel,
Frota as FrotaModel,
tipo_ativo as TipoAtivoModel,
)
from processos.models import ItemAlocado as ItemAlocadoModel
from core.entities.frota_e_equipamentos import VeiculosEntity,ManutencaoEntity

from decimal import Decimal
from typing import List, Optional


def frota_model_to_entity(model:FrotaModel)->VeiculosEntity:
    return VeiculosEntity(
        tipo_id=model.tipo_id,# type: ignore
        id=model.pk if model.pk is not None else None,
        Ativo=model.Ativo,
        placa=model.placa,
        RENAVAN=model.RENAVAN,
        marca=model.marca,
        modelo=model.modelo,
        ano=model.ano,
        tipo_combustivel=model.tipo_combustivel,
        situacao=model.situacao,
    )

def manutencao_model_to_entity(model:ManutencaoModel)->ManutencaoEntity:
    custo_model=model.custo_total
    custo_manutencao_decimal=Decimal(
        str(custo_model) if custo_model is not None else Decimal('0.00')
    )
    return ManutencaoEntity(
        veiculo_id=model.veiculo_id,# type: ignore
        id=model.pk if model.pk is not None else None,
        motivo=model.motivo,
        local_manutencao=model.local_de_manutencao,
        operacao=model.operacao,
        registro=model.registro,
        custo_manutencao=custo_manutencao_decimal,
        data_entrada=model.data_entrada_manutencao
    )

def tipo_ativo_model_to_entity(model:TipoAtivoModel)->TipoAtivoEntity:
    return TipoAtivoEntity(
        id=model.pk if model.pk is not None else None,
        tipo_de_ativo=model.tipo_de_ativo,

    )

def item_model_to_entity(model:ItemAlmoxarifadoModel)->Item_almoxarifadoEntity:
    return Item_almoxarifadoEntity(
        tipo_ativo_id=model.tipo_id,# type: ignore
        item_id=model.pk if model.pk is not None else None,
        nome=model.nome,
    )

def lote_model_to_entity(model:LoteModel)->LoteEntity:
    return LoteEntity(
        item_id=model.item_id,# type: ignore
        id=model.pk if model.pk is not None else None,
        nota=model.nota,
        fornecedor=model.fornecedor,
        data_entrada=model.data_entrada
        if model.data_entrada is not None else None,
        valor_unitario=model.valor_unitario,
        quantidade_entrada=model.quantidade_entrada_nota or Decimal('0.00')
    )

def item_alocado_model_to_entity(model:ItemAlocadoModel)->Item_alocadoEntity:
    return Item_alocadoEntity(
        pedido_id=model.pedido_id,# type: ignore
        item_estoque_id=model.item_alocado_id,# type: ignore
        item_alocado_id=model.pk if model.pk is not None else None,
        data_alocacao=model.data_alocado
        if model.data_alocado is not None else None,
        quantidade=model.quantidade or Decimal('0.00')

    )

class AlmoxarifadoDjangoRepository(AlmoxarifadoRepository):

    def salvar_tipo_ativo(self, tipo_ativo: TipoAtivoEntity) -> TipoAtivoEntity:
        tipo_ativo_data = {
            'tipo_de_ativo': tipo_ativo.tipo_de_ativo,

        }
        model, created = TipoAtivoModel.objects.update_or_create(pk=tipo_ativo.id, defaults=tipo_ativo_data)# type: ignore
        return tipo_ativo_model_to_entity(model)

    def salvar_item(self, item: Item_almoxarifadoEntity) -> Item_almoxarifadoEntity:
        item_data = {
            'tipo_id': item.tipo_ativo_id,
            'nome': item.nome,
        }
        model, created = ItemAlmoxarifadoModel.objects.update_or_create(pk=item.item_id, defaults=item_data)# type: ignore

        return item_model_to_entity(model)

    def salvar_lote(self,lote:LoteEntity)->LoteEntity:
        lote_data={
            'item_id':lote.item_id,
            'nota':lote.nota,
            'fornecedor':lote.fornecedor,
            'data_entrada':lote.data_entrada,
            'valor_unitario':lote.valor_unitario,
            'quantidade_entrada_nota':lote.quantidade_entrada,

        }

        model,created=LoteModel.objects.update_or_create(pk=lote.id,defaults=lote_data)# type: ignore
        return lote_model_to_entity(model)

    def salvar_alocacao(self,item_alocado:Item_alocadoEntity) ->Item_alocadoEntity:

        item_alocado_data={
            'pedido_id':item_alocado.pedido_id,
            'item_alocado_id':item_alocado.item_estoque_id,
            'data_alocado':item_alocado.data_alocacao,
            'quantidade':item_alocado.quantidade
        }
        model,created=ItemAlocadoModel.objects.update_or_create(pk=item_alocado.item_alocado_id,# type: ignore
                                                                defaults=item_alocado_data)
        return item_alocado_model_to_entity(model)

    def calcular_saida_total_por_item_id(self,item_id:int) ->Decimal:
        from django.db.models import Sum

        resultado=ItemAlocadoModel.objects.filter(item_alocado_id=item_id).aggregate( # type: ignore
            total_saida=Sum('quantidade')
        )

        return resultado.get('total-saida') or Decimal('0.00')




class FrotaDjangoRepository(FrotaRepository):

    def buscar_veiculo_por_id(self,veiculo_id:int) ->Optional[VeiculosEntity]:
        try:
            model=FrotaModel.objects.get(pk=veiculo_id) # type: ignore
            return frota_model_to_entity(model)
        except FrotaModel.DoesNotExist: # type: ignore
            return None

    def buscar_manutencao_por_veiculo_id(self,veiculo_id:int) ->list[ManutencaoEntity]:
        manutencoes=ManutencaoModel.objects.filter(Ativo_em_manutencao_id=veiculo_id)
        return [manutencao_model_to_entity(m) for m in manutencoes]

    def salvar_veiculo(self,veiculo:VeiculosEntity) ->VeiculosEntity:
        veiculo_data={
            'tipo_id':veiculo.tipo_id,
            'Ativo':veiculo.Ativo,
            'placa':veiculo.placa,
            'RENAVAN':veiculo.RENAVAN,
            'marca':veiculo.marca,
            'modelo':veiculo.modelo,
            'ano':veiculo.ano,
            'tipo_combustivel':veiculo.tipo_combustivel,
            'custo_manutencao_agregado':veiculo.custo_total_de_manutencao
        }
        model,created=FrotaModel.objects.update_or_create(pk=veiculo.id,defaults=veiculo_data)
        return frota_model_to_entity(model)

    def salvar_manutencao(self,manutencao:ManutencaoEntity) ->ManutencaoEntity:
        manutencao_data={
            'veiculo_id':manutencao.veiculo_id,
            'motivo':manutencao.motivo,
            'local_de_manutencao':manutencao.local_manutencao,
            'operacao':manutencao,
            'registro':manutencao.registro,
            'custo_manutencao':manutencao.custo_manutencao,
            'data_entrada':manutencao.data_entrada_manutencao
        }
        model,created=ManutencaoModel.objects.update_or_create(pk=manutencao.id,defaults=manutencao_data)
        return manutencao_model_to_entity(model)









