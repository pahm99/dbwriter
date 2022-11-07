from os import path, mkdir
import json
from pick import pick
from rich.console import Console
from rich.table import Table
from itertools import zip_longest
from rich.prompt import Prompt, FloatPrompt, IntPrompt


class Data:
    campos = {}
    nombre = ''
    search_key = 'nombre'

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
        if not path.exists(f'./db/{self.nombre}_table/index.json'):

            dic = {
                'id': 0,
                'tabla': self.nombre,
                'columnas': [],
                'longitud': 0
            }

            for campo_key in self.campos:
                dic['columnas'].append({
                    'tipo': self.campos[campo_key]['type'].value,
                    'campo': campo_key,
                    'posicion': counter,
                });
                counter = counter + 1
                pass
            findex = open(f'./db/{self.nombre}_table/index.json', 'w')
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

    def __pedir_columnas(self):
        title = 'Favor de seleccionar las columnas a proyectar (espacio para seleccionar, enter para continuar)'
        campos = list(self.campos.keys())
        selected = pick(campos, title, multiselect=True, min_selection_count=1)
        selected_flat = []
        for sel in selected:
            selected_flat.append(sel[0])
        return selected_flat

    def select(self):
        selected = self.__pedir_columnas()
        # preguntamos si desea filtrar por ID o por search key
        filter, i = pick(['id', self.search_key, 'no'], '¡Desea filtrar?')
        console = Console()
        table = Table('ID', *selected, title=self.nombre)
        index_file = open(f'./db/{self.nombre}_table/index.json', 'r')
        index_file.close()

        ## arreglo de los archivos de los campos a leeer
        fcampos = []
        for camp in selected:
            fcampos.append(open(f'./db/{self.nombre}_table/{camp}.fd', 'r'))

        for row in zip_longest(*fcampos):
            row_striped = []
            for val in row:
                [id,val] = val.strip().split(',')
                row_striped.append(val)
            table.add_row(id, *row_striped)

        console.print(table)

    # aumenta en una, el id del documento
    def auto_increment(self):
        json_file = open(f'./db/{self.nombre}_table/index.json', 'r')
        dic = json.loads(json_file.read())
        json_file.close()
        jsonf = open(f'./db/{self.nombre}_table/index.json', 'w')

        dic['id'] = dic['id'] + 1
        dic['longitud'] = dic['longitud'] + 1

        jsonf.write(json.dumps(dic, indent=4))
        jsonf.close()

        return dic['id']

    """
    El campo que nos pasaron les llenamoslos valores, de lo contrario son NULL
    """

    def insert(self):
        cols = self.__pedir_columnas()
        len = IntPrompt.ask('¿Cuantos nuevos registros van a hacer?', default=1)
        console = Console()
        table = Table('ID' ,*cols,title='Registros realizados')
        for i in range(0, len):
            fill = {}
            for col in cols:
                val = None
                selfcol = self.campos[col]
                reg = f'{i + 1} => {col}'
                match selfcol['type'].value:
                    case 'string':
                        val = Prompt.ask(reg)
                    case 'number':
                        val = FloatPrompt.ask(reg)

                # TODO si el valor no es correcto, saltamos este regitro

                val = str(val)
                fill[col] = val
            # caso contrario lo registramos
            id = self.auto_increment()
            params = fill.keys()
            registro = [str(id)]
            for key in self.campos:
                fcampo = open(f'./db/{self.nombre}_table/{key}.fd', 'a')
                if key not in params: # significa que es un campo nulo, porque no lo ingresaron
                    fcampo.write(f'{id},[NULL]\n')
                else: # si tneemos el valor
                    v = fill[key]
                    fcampo.write(f'{id},{v}\n')
                    registro.append(v)
                fcampo.close()
            table.add_row(*registro)

        console.print(table)