from src.models.Cliente import Cliente
from rich.console import Console
from rich.text import Text
from rich.padding import Padding

cliente = Cliente()
cliente.initDB()



def main():
    command = None

    console = Console()
    info = Text('Gestor de datos local\n')
    info.append('comandos:\n')
    info.append('- select: para traer datos de la tabla\n')
    info.append('- insert: pide los datos a ingresar\n')
    info.append('- find: ecnontrar un registro y poder editar o eliminarlo\n')
    pad = Padding(info, 1)
    console.print(pad)
    while True:
        command = input('>> ').strip()
        match command:
            case 'select':
                cliente.select()
            case 'insert':
                cliente.insert()
            case 'find':
                cliente.find()
            case 'exit':
                print('Adios :D')
                break
            case other:
                print('Comando no valido')

    pass


if __name__ == '__main__':
    main()
