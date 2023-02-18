from django.contrib import admin
from .models import Autor, Genero, Livro, InstanciaLivro, Idioma


# Register your models here.
admin.site.register(Genero)
admin.site.register(Idioma)

class InstanciaLivroInline(admin.TabularInline):
    model = InstanciaLivro
    extra = 1

class LivroInline(admin.StackedInline):
    model = Livro
    extra = 0

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome','sobrenome','data_nascimento', 'data_morte')
    fields = [('nome', 'sobrenome'), ('data_nascimento','data_morte')]
    inlines = [LivroInline]

admin.site.register(Autor,AutorAdmin)

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo','autor','mostra_genero')
    inlines = [InstanciaLivroInline]


@admin.register(InstanciaLivro)
class InstanciaAdmin(admin.ModelAdmin):
    
    list_display = ('id','livro','data_devolucao','status', 'emprestado_para')
    list_filter = ('status','data_devolucao')
    fieldsets = (
        ('Dados gerais', {
            'fields': ('livro','edicao','id')
        }),
        ('Disponibilidade', {
            'fields': ('status','data_devolucao','emprestado_para')
        }),
    )


