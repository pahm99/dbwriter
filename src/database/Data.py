import os
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
        what_select = pick(['todo', 'seleccionar campos'], '¿Que deseas seleccionar?')
        selected = None
        print(what_select)
        if what_select[0] == 'todo':
            selected = list(self.campos.keys())
        else:
            selected = self.__pedir_columnas()

        # preguntamos si desea filtrar por ID o por search key
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

        # cerramos los archivos
        for fcampo in fcampos:
            fcampo.close()
        console.print(table)

    def find(self):
        filter, i = pick(['id', self.search_key], '¿Desea filtrar por?')
        key = None
        field = None

        what_fields, i = pick(['todo', 'seleccionar'], '¿Que desea seleccionar?')

        selected = None

        if what_fields == 'todo':
            selected = list(self.campos.keys())
        else:
            selected = self.__pedir_columnas()

        if filter == 'id':
            key = IntPrompt.ask('Ingrese el ID')
            field = 'id'
        else:
            field = self.search_key
            key = Prompt.ask(f'Ingrese el valor a buscar en {self.nombre}')
        fcampos = []
        for camp in selected:
            fcampos.append(open(f'./db/{self.nombre}_table/{camp}.fd', 'r'))

        found_it = False
        fields = None
        if field == 'id':
            fields = self.__findbyid(key,selected)
        else:
            # buscamos por search key
            fsearch = open(f'./db/{self.nombre}_table/{self.search_key}.fd', 'r')
            for line in fsearch:
                [id,val] = line.strip().split(',')
                if val == key:
                    fsearch.close()
                    fields = self.__findbyid(int(id), selected)
                    break

            if not fsearch.closed:
                fsearch.close()
        if fields is not None:
            found_it = True

        console = Console()
        if found_it:

            table = Table('ID', *selected, title='Registro econtrado')
            table.add_row(*fields)
            console.print(table)
        else:
            console.print('Registro no econtrado :disappointed:')
            return

        do_something = Prompt.ask('¿Deseas hacer algo con el registro?', choices=['si', 'no'])
        if do_something == 'no':
            return None
        what_do, _ = pick(['borrar', 'editar'], '¿Que deseas hacer con el registro?')

        match what_do:
            case 'borrar':
                self.borrar_registro(fields[0])
            case 'editar':
                self.remplazar_registro(fields[0])






    def remplazar_registro(self,id):
        # preguntamos que campos quiere editar
        fields_edit = self.__pedir_columnas()
        for campo in fields_edit:
            # pedimos el nuevo valor
            new_value = Prompt.ask(f'Nuevo valor para {campo}')
            # archivo original
            fcampo = open(f'./db/{self.nombre}_table/{campo}.fd', 'r')
            # nuevo archivo
            ftmp = open(f'./db/{self.nombre}_table/{campo}.tmp', 'a')
            for line in fcampo:
                reg_id = line.strip().split(',')[0]
                if reg_id == id:
                    ftmp.write(f'{id},{new_value}\n')
                    continue
                ftmp.write(line)
            pass
            # borramos el original
            os.remove(f'./db/{self.nombre}_table/{campo}.fd')
            # renombramos el tmp al orginal
            os.rename(f'./db/{self.nombre}_table/{campo}.tmp', f'./db/{self.nombre}_table/{campo}.fd')
            fcampo.close()
            ftmp.close()
        print('Registro actualizado :D')


    def borrar_registro(self,id: str):
        # tenemos que abrir cada archivo, crear una copia del original
        # borrar el orginal, dejando el nuevo sin el valor eliminado
        # vamos por cada archivo creamos un nuevo, registrando linea a linea
        # exceptuando donde este el ID
        for campo in self.campos.keys():
            # archivo original
            fcampo = open(f'./db/{self.nombre}_table/{campo}.fd', 'r')
            # nuevo archivo
            ftmp = open(f'./db/{self.nombre}_table/{campo}.tmp', 'a')
            for line in fcampo:
                reg_id = line.strip().split(',')[0]
                if reg_id == id:
                    continue
                ftmp.write(line)
            # borramos el original
            os.remove(f'./db/{self.nombre}_table/{campo}.fd')
            # renombramos el tmp al orginal
            os.rename(f'./db/{self.nombre}_table/{campo}.tmp', f'./db/{self.nombre}_table/{campo}.fd')
            fcampo.close()
            ftmp.close()

        print("Registro eliminado :D")
        # cargamos el JSON y quitamos uno de los registros
        fjson = open(f'./db/{self.nombre}_table/index.json', 'r')
        index_json = json.loads(fjson.read())
        fjson.close()
        index_json['longitud'] = index_json['longitud'] - 1
        fjson = open(f'./db/{self.nombre}_table/index.json', 'w')
        fjson.write(json.dumps(index_json, indent=4))
        fjson.close()


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

    def __findbyid(self,id: int,selected: list):
        id = str(id)
        fcampos = []
        fields = []
        for camp in selected:
            fcampos.append(open(f'./db/{self.nombre}_table/{camp}.fd', 'r'))
        for row in zip_longest(*fcampos):
            id_reg = row[0].strip().split(',')[0]
            if id_reg == id:
                fields.append(id)
                for fill in row:
                    val = fill.strip().split(',')[1]
                    fields.append(val)
                return fields
        # cerramos los archivos
        for fcampo in fcampos:
            fcampo.close()
        return None

    """
    El campo que nos pasaron les llenamoslos valores, de lo contrario son NULL
    """

    def insert(self):
        cols = self.__pedir_columnas()
        len = IntPrompt.ask('¿Cuantos nuevos registros van a hacer?', default=1)
        console = Console()
        table = Table('ID', *cols, title='Registros realizados')
        for i in range(0, len):
            fill = {}
            for col in cols:
                val = None
                selfcol = self.campos[col]
                reg = f'{i + 1} => {col}'
                match selfcol['type'].value:
                    case 'string' | 'date':
                        val = Prompt.ask(reg)
                    case 'number':
                        val = FloatPrompt.ask(reg)
                    case other:
                        val = '[NULL]'

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