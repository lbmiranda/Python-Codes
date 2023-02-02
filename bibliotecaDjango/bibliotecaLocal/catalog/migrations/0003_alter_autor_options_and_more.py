# Generated by Django 4.1.2 on 2023-02-02 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_autor_alter_genero_nome_alter_livro_isbn_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'ordering': ['nome', 'sobrenome']},
        ),
        migrations.RenameField(
            model_name='autor',
            old_name='date_of_birth',
            new_name='data_nascimento',
        ),
        migrations.RenameField(
            model_name='autor',
            old_name='first_name',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='autor',
            old_name='last_name',
            new_name='sobrenome',
        ),
        migrations.RemoveField(
            model_name='autor',
            name='date_of_death',
        ),
        migrations.AddField(
            model_name='autor',
            name='data_morte',
            field=models.DateField(blank=True, null=True, verbose_name='Data da morte'),
        ),
    ]