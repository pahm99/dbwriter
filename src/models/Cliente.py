from src.database.Data import Data
from src.database.Types import Type


class Cliente(Data):
    nombre = 'clientes'

    campos = {
        'nombre': {
            'type': Type.string,
            'rules': []
        },
        'ap_paterno': {
            'type': Type.string,
            'rules': []
        },
        'ap_materno': {
            'type': Type.string,
            'rules': []
        },
        'fecha_alta': {
            'type': Type.date,
            'rules': []
        },
        'credito': {
            'type': Type.number,
            'rules': []
        },
        'deuda': {
            'type': Type.number,
            'rules': []
        }
    }
