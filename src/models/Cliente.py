from src.database.Data import Data
from src.database.Types import Type
from src.database.Validators.Unique import Unique


class Cliente(Data):
    nombre = 'clientes'

    campos = {
        'id': {
            'type': Type.string,
            'rules': []
        },
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
