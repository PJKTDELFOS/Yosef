from django.contrib import admin

from core.use_cases.almoxarifado_use_cases import CalculoItemEstoqueUsecase
from. import models
from processos.models import ItemAlocado
from decimal import Decimal
from core.ports.frota_repository import FrotaRepository
from core.ports.almoxarifado_repository import AlmoxarifadoRepository
from operacional.adapters.orm_adapter import FrotaDjangoRepository,AlmoxarifadoDjangoRepository
from core.use_cases.calculo_custo_frota_manutencao import CalculoCustoManutencaoUsecase
from .models import Item_almoxarifado

almoxarifado_repo: AlmoxarifadoRepository = AlmoxarifadoDjangoRepository()
estoque_calc_use_case=CalculoItemEstoqueUsecase(repositorio=almoxarifado_repo)

# Register your models here.

#terminar amanha as implementações
class Manutencaoinline(admin.TabularInline):
    model = models.Manutencao
    extra = 0
    fields = ('id','Ativo_em_manutencao','data_entrada_manutencao','operacao','custo_total')

class LoteINLine(admin.TabularInline):
    model = models.lote
    extra = 0
    fields = ('id','nota','data_entrada','valor_unitario','quantidade_entrada_nota','valor_total','Nf')
    readonly_fields = ('valor_total',)

class Item_alocado_inline(admin.TabularInline):
    model =ItemAlocado
    extra=0
    readonly_fields = ('pedido','data_aloccado','quantidade','valor_total_alocado_formatado','preco_unitario_medio_pedido_formatado')
    can_delete = False


@admin.register(models.Item_almoxarifado)
class ItemAlmoxarifadoAdmin(admin.ModelAdmin):
    inlines = [LoteINLine,Item_alocado_inline]
    list_display = ['nome','quantidade_total_a_exibir',
                    'valor_unitario_a_exibir','valor_atual_estoque_a_exibir' ]

    readonly_fields = ['quantidade_total_a_exibir',
                    'valor_unitario_a_exibir','valor_atual_estoque_a_exibir']

    def quantidade_total_a_exibir(self,obj:Item_almoxarifado)->Decimal:
        return estoque_calc_use_case.quantidade_disponivel_estoque(item_id=obj.pk)
    quantidade_total_a_exibir.short_description='Quantidade em estoque'

    def valor_unitario_a_exibir(self,obj:Item_almoxarifado)->str:
        preco_medio=estoque_calc_use_case.preco_unitario_medio_por_item_id(item_id=obj.pk)
        return f' R$ {preco_medio:,.2f}'
    valor_unitario_a_exibir.short_description='Preço unitário médio'

    def valor_atual_estoque_a_exibir(self,obj:Item_almoxarifado)->str:
        valor=estoque_calc_use_case.valor_total_estoque_por_item_id(item_id=obj.pk)
        return f' R$ {valor:,.2f}'
    valor_atual_estoque_a_exibir.short_description='Valor total do estoque'









@admin.register(models.Frota)
class frotaadmin(admin.ModelAdmin):
    inlines = [Manutencaoinline,]

@admin.register(models.Manutencao)
class manutencaoadmin(admin.ModelAdmin):
    ...

@admin.register(models.tipo_ativo)
class tipo_ativo_admin(admin.ModelAdmin):
    ...