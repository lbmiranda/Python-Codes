from django.contrib import admin
from .models import Autor, Genero, Livro, InstanciaLivro, Idioma


# Register your models here.
admin.site.register(Genero)
admin.site.register(Idioma)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome','sobrenome','data_nascimento', 'data_morte')

admin.site.register(Autor,AutorAdmin)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    pass


@admin.register(InstanciaLivro)
class InstanciaAdmin(admin.ModelAdmin):
    pass

