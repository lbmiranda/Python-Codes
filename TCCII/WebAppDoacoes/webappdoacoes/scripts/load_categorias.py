from appdoacoes.models import Categoria
import csv


def run():
    with open('categorias.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  

        for row in reader:
            print(row)

            categoria = Categoria(descricao=row[0],tipo=row[1])
            categoria.save()