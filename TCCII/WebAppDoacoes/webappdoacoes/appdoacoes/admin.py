from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, DonativoMaterialOuServico, Categoria,Endereco, InstanciaMaterial

@admin.register(EmpresaEntidade)
class EmpresaEntidadeAdmin(admin.ModelAdmin):
    pass

@admin.register(EmpresaComunidade)
class EmpresaComunidadeAdmin(admin.ModelAdmin):
    pass

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('tipo','descricao')
    list_filter = ('tipo','descricao')


admin.site.register(PessoaComunidade)
admin.site.register(DonativoMaterialOuServico)
admin.site.register(Endereco)
admin.site.register(InstanciaMaterial)
