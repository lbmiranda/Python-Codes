from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario, User

@receiver(post_save,sender=User)
def cria_perfil(sender,instance,created,**kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)
        print('Perfil criado')


@receiver(post_save,sender=User)
def atualiza_perfil(sender,instance,created,**kwargs):
    if not created:
        PerfilUsuario.objects.update(usuario=instance)
        print('Perfil atualizado')

@receiver(post_save,sender=User)
def salva_perfil(sender,instance,**kwargs):
    instance.perfilusuario.save()
    print('Perfil salvo')