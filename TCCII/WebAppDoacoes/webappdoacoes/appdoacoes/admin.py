from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User,PerfilUsuario

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'tipo_de_conta', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('tipo_de_conta', 'entidade', 'comunidade_pf','comunidade_pj')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_de_conta'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

admin.site.register(PerfilUsuario)

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
