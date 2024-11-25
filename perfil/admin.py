from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.PerfilUsuario)
class categorytAdmin(admin.ModelAdmin):
    list_display= ('id','usuario')
    list_display_links = ('id',)

