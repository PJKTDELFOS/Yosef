from django.contrib import admin
from . import models
from axes.models import AccessLog
from django.contrib import admin, messages
from django.contrib.auth.models import User


# Register your models here.
# Função de ação para liberar bloqueio
def liberar_bloqueio(modeladmin, request, queryset):
    total_deletados = 0
    for user in queryset:
        deletados, _ = AccessLog.objects.filter(username=user.username).delete()
        total_deletados += deletados
    messages.success(request, f'Bloqueio liberado para {queryset.count()} usuário(s). Total de registros deletados: {total_deletados}.')
liberar_bloqueio.short_description = "Liberar bloqueio de usuários selecionados"



class dependenteinline(admin.TabularInline):
    model = models.dependente
    extra = 0
    fields = ('id', 'funcionario', 'nome_dependente', 'cpf_dependente', 'grau_relacional')


class uniformes_EPIinline(admin.TabularInline):
    model = models.uniformes_EPI
    extra = 0
    fields = ('id', 'funcionario', 'tipo')

class UserAdmin(admin.ModelAdmin):
    actions = [liberar_bloqueio]


@admin.register(models.cadastrofuncionario)
class cadastrofuncionarioadmin(admin.ModelAdmin):
    list_display= ('id','nomecompleto','idade',)
    list_display_links = ('id',)
    search_fields = 'nomecompleto','cpf,',
    inlines = [dependenteinline,uniformes_EPIinline,]
    actions = [liberar_bloqueio]



@admin.register(models.dependente)
class depenenteadmin(admin.ModelAdmin):
    list_display = ('id','funcionario','nome_dependente')
    list_display_links = ('id','funcionario','nome_dependente')
    list_filter =('id','funcionario','nome_dependente',)

@admin.register(models.uniformes_EPI)
class uniformes_EPI_admin(admin.ModelAdmin):
    list_display = ('id','funcionario',)
    list_display_links = ('id',)
    list_filter = ('funcionario',)










