from os import path, mkdir


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
            findex = open(f'./db/{self.nombre}_table/index.db', 'a')
            for campo_key in self.campos:
                type = self.campos[campo_key]['type'].value;
                findex.write(f'{counter},{campo_key},{type},0\n')
                counter = counter + 1
                pass
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
        index = open(f'./db/{self.nombre}_table/index.db', 'r')
        lines = index.readlines()
        index.close()
        for i, line in enumerate(lines):
            [
                pos,
                campo_index,
                tipo,
                last_key
            ] = line.split(',')

            if campo_index == self.primary_key:
                index_out = open(f'./db/{self.nombre}_table/index.db','w')
                lines[i] = ','.join([pos, campo_index, tipo, str(int(last_key) + 1)]) + '\n'
                index_out.writelines(lines)
                index_out.close()
                print(lines)
                pass
        pass


        index.close()

    def insert(self, parametros: dict):
        # recorremos los campos y validamos que exista en el indice
        for param_key in parametros:
            if param_key not in self.campos:
                err = f'El campo {param_key} no definido en {self.nombre}';
                raise Exception(err)
        pass
        # si pasamos la validacion,entonces, empezamos hacer los registro
        for param_key in parametros:
            # recuperamos el indice del campo
            campo = self.getCampo(param_key)
            if campo is None:
                raise Exception(f'campo {param_key} no existente en el indice {self.nombre}_table')
            # buscamos su archivo del campo
            field = open(f'./db/{self.nombre}_table/{param_key}.fd', 'a')
            field.write('{0},{1}\n'.format(campo['id'], parametros[param_key]))
            field.close()
        # aumentamos el identificador
        self.auto_increment()

    def getCampo(self, campo):
        index = open(f'./db/{self.nombre}_table/index.db', 'r')
        for line in index:
            [
                pos,
                campo_index,
                tipo,
                last_key
            ] = line.split(',')

            if campo_index == campo:
                return {
                    'id': int(last_key),
                    'campo': campo_index,
                    'tipo': tipo,
                    'pos': pos
                }
        index.close()
        return None
