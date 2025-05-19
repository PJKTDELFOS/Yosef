from django.contrib import admin
from. import models
from processos.models import ItemAlocado


# Register your models here.


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
class ModelNameAdmin(admin.ModelAdmin):
    inlines = [LoteINLine,Item_alocado_inline]
    list_display = ['nome','quantidade_total',
                    'valor_untario_formatado','valor_atual_estoque_formatado' ]
    readonly_fields = ['quantidade_total',
                       'valor_untario_formatado','valor_atual_estoque_formatado']

@admin.register(models.Frota)
class frotaadmin(admin.ModelAdmin):
    inlines = [Manutencaoinline,]

@admin.register(models.Manutencao)
class manutencaoadmin(admin.ModelAdmin):
    ...

@admin.register(models.tipo_ativo)
class tipo_ativo_admin(admin.ModelAdmin):
    ...