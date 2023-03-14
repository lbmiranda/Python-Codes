from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

from .models import EmpresaEntidade, EmpresaComunidade, PessoaComunidade, Donativo, Categoria, InstanciaDonativo

@admin.register(EmpresaEntidade)
class EmpresaEntidadeAdmin(admin.ModelAdmin):
    list_display=('cnpj','nome_fantasia','get_endereco','usuario_responsavel')

@admin.register(EmpresaComunidade)
class EmpresaComunidadeAdmin(admin.ModelAdmin):
    pass

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('tipo','descricao')
    list_filter = ('tipo','descricao')

@admin.register(Donativo)
class DonativoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao','categoria','unidade')


admin.site.register(PessoaComunidade)
admin.site.register(InstanciaDonativo)
