from django.contrib import admin
from django import forms
from processos.models import Processo,Contratos,Pedidos
from django.db import models



# Register your models here.
'''
notas de atenção admin
1-sempre que por um editable, ele deve constar no list display, voce so pode mudaralgo que pode ver
'''

class Contratoinline(admin.TabularInline):
    model = Contratos
    extra=1
    fields = ('id','processo','contratante','numero',)

class Pedidoinline(admin.TabularInline):
    model = Pedidos
    extra=1
    fields = ('id',  'contratante', 'numero',)

@admin.register(Processo)
class processoAdmin(admin.ModelAdmin):
    list_display = ('id','numero_processo','numero_licitacao','contratante','modalidade',
                    'data_disputa','objeto','tipo','valor_formatado','status','show',)
    ordering = ('-id',)
    search_fields = ('contratante','numero_processo','numero_licitacao')
    inlines = [Contratoinline]
    list_display_links = ('id','numero_licitacao',)
    list_editable = ('show',)




@admin.register(Contratos)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id','processo','contratante','numero',
                    'seguro','seguradora','valor_total','inicio',
                    'vigencia','fim_contrato','executado','executavel')
    ordering = ('-id',)
    inlines = [Pedidoinline]
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'disabled': False})},  # Corrigido o uso de CharField
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None and not obj.seguro:
            form.base_fields['apolice'].widget.attrs['disabled'] = True
            form.base_fields['seguradora'].widget.attrs['disabled'] = True
        return form


@admin.register(Pedidos)
class Pedidoadmin(admin.ModelAdmin):
    list_display = ('id','contrato','numero','valor','data_entrega','show')
    ordering = ('id',)
    list_editable = ('show',)










