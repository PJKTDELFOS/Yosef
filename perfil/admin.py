from django.contrib import admin
from . import models
from django.contrib.auth.models import User


# Register your models here.


class dependenteinline(admin.TabularInline):
    model = models.dependente
    extra = 0
    fields = ('id', 'funcionario', 'nome_dependente', 'cpf_dependente', 'grau_relacional')


class uniformes_EPIinline(admin.TabularInline):
    model = models.uniformes_EPI
    extra = 0
    fields = ('id', 'funcionario', 'tipo')




@admin.register(models.cadastrofuncionario)
class cadastrofuncionarioadmin(admin.ModelAdmin):
    list_display= ('id','nomecompleto','idade','usuario')
    list_display_links = ('id',)
    search_fields = 'nomecompleto','cpf,',
    inlines = [dependenteinline,uniformes_EPIinline,]
    @admin.action(description='vincular usuario a funcionario')
    def vincular_funcionario(self,request,queryset):
        for funcionario in queryset:
            if not funcionario.usuario:
                user=User.objects.create_user(
                    username=funcionario.email,
                    email=funcionario.email,
                    password=f'{funcionario.cpf[0:4]}'
                )
                funcionario.usuario=user
                funcionario.save()
            else:
                self.message_user(request, f"O funcionário {funcionario.nome} "
                                           f"já possui um usuário vinculado.")



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










