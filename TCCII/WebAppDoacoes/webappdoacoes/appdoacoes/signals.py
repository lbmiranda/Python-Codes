from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import PerfilUsuario, User

@receiver(post_save,sender=User)
def cria_perfil(sender,instance,created,**kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)


@receiver(post_save,sender=User)
def salva_perfil(sender,instance,**kwargs):
    instance.perfilusuario.save()


@receiver(post_save, sender = User)
def adiciona_usuario_em_grupo(sender, instance, created, **kwargs):
    if created:
        if instance.tipo_de_conta == User.ENTIDADE:
            group = Group.objects.get(name='Entidades')
        else:
            group = Group.objects.get(name='ComunidadeGeral')
        group.user_set.add(instance)


        


