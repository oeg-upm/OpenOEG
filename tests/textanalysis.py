import os

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

paginas=open_file('./tfg/paginas.txt')

print(paginas.split("\n")[0])