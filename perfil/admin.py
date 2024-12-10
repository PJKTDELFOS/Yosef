from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.cadastrofuncionario)
class categorytAdmin(admin.ModelAdmin):
    list_display= ('id','nomecompleto')
    list_display_links = ('id',)

