# Generated by Django 4.1.2 on 2023-02-18 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0004_idioma_livro_idioma'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancialivro',
            name='emprestado_para',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
