# Generated by Django 4.1.2 on 2023-02-02 00:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_death', models.DateField(blank=True, null=True, verbose_name='Died')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AlterField(
            model_name='genero',
            name='nome',
            field=models.CharField(help_text='Informe um genero literário. Ex: Ficção científica', max_length=200),
        ),
        migrations.AlterField(
            model_name='livro',
            name='isbn',
            field=models.CharField(help_text='código de 13 caracteres ISBN - <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, unique=True, verbose_name='ISBN'),
        ),
        migrations.CreateModel(
            name='InstanciaLivro',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único para este livro em particular', primary_key=True, serialize=False)),
                ('edicao', models.CharField(max_length=200)),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Manutenção'), ('e', 'Emprestado'), ('d', 'Disponível'), ('r', 'Reservado')], default='m', help_text='Disponibilidade', max_length=1)),
                ('livro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.livro')),
            ],
            options={
                'ordering': ['data_devolucao'],
            },
        ),
        migrations.AddField(
            model_name='livro',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.autor'),
        ),
    ]
