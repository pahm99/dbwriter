from src.models.Cliente import Cliente


def insertPerson(cliente: Cliente):
    cliente.insert({
        'nombre': 'Pedro Alonso',
        'ap_paterno': 'Herrera',
        'ap_materno': 'Mauricio',
        'fecha_alta': '03-05-2020',
        'credito': 5_000,
        'deuda': 2_500
    })


def main():
    cliente = Cliente()
    cliente.initDB()
    insertPerson(cliente)

    pass


if __name__ == '__main__':
    main()
