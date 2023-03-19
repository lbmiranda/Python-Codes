from appdoacoes.models import Donativo,Categoria
import csv


def run():
    with open('donativos.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  

        for row in reader:
            print(row)

            categoria = Categoria.objects.get_or_create(descricao=row[-1])
            categoria_obj = categoria[0]

            print(categoria)

            donativo = Donativo(descricao=row[0],unidade=row[1], categoria_id=categoria_obj.codigo_categoria)

            print(donativo)

            donativo.save()