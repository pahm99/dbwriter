from os import path, mkdir
import json


class Data:
    campos = {}
    nombre = ''
    primary_key = 'id'

    def __init__(self):
        pass

    # comprueba que el directorio de archivos este creado
    def initDB(self):
        # corroboramos si existe nuestra directorio

        if not path.exists(f'./db/{self.nombre}_table'):
            mkdir(f'./db/{self.nombre}_table')
            pass
        # checamos si existe un index, si no lo cremaos
        counter = 1
        if not path.exists(f'./db/{self.nombre}_table/index.db'):

            dic = {
                'id': 0,
                'tabla': self.nombre,
                'columnas': []
            }

            for campo_key in self.campos:
                dic['columnas'].append({
                    'tipo': self.campos[campo_key]['type'].value,
                    'campo': campo_key,
                    'posicion': counter
                });
                counter = counter + 1
                pass
            findex = open(f'./db/{self.nombre}_table/index.json', 'a')
            findex.write(json.dumps(dic, indent=4))
            findex.close()
        # corroboramos los campos
        for campo_key in self.campos:
            if not path.exists(f'./db/{self.nombre}_table/{campo_key}.fd'):
                fcampo = open(f'./db/{self.nombre}_table/{campo_key}.fd', 'a')
                fcampo.close()
                pass
            pass
        pass

    # aumenta en una, el id del documento
    def auto_increment(self):
        json_file = open(f'./db/{self.nombre}_table/index.json', 'r')
        dic = json.loads(json_file.read())
        json_file.close()
        json_file = open(f'./db/{self.nombre}_table/index.json', 'w')

        dic['id'] = dic['id'] + 1

        json_file.write(json.dumps(dic, indent=4))
        json_file.close()

        return dic['id']

    """
    El campo que nos pasaron les llenamoslos valores, de lo contrario son NULL
    """

    def insert(self, parametros: dict):
        # recorremos los campos y validamos que exista en el indice
        for param_key in parametros:
            if param_key not in self.campos:
                err = f'El campo {param_key} no definido en {self.nombre}';
                raise Exception(err)
        pass
        # verfiicamos los campos que nos pasaron contra los que nos nos paramos
        id = self.auto_increment()  # nos regresa un id autoincrementado
        # recorremos nuestro campos contra los parametros
        # si no los nustro campo no esta en los parametros, entonce es nulo, porque
        # no se envie a ingresar

        params = parametros.keys()
        for campo in self.campos:
            fcampo = open(f'./db/{self.nombre}_table/{campo}.fd', 'a')
            if campo not in params:  # es nulo
                fcampo.write(f'{id},[NULL]\n')
            else:  # significa que lo pasaron
                val = parametros[campo]
                fcampo.write(f'{id},{val}\n')
            fcampo.close()
        pass

    pass
