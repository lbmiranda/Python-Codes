# Generated by Django 4.1.2 on 2023-02-18 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_instancialivro_emprestado_para'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instancialivro',
            options={'ordering': ['data_devolucao'], 'permissions': (('pode_registrar_devolucao', 'Devolve livro'),)},
        ),
    ]
