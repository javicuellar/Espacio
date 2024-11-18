# -*- coding: utf-8 -*-

import sqlite3, os

# La clase BaseDatos implementa el software de mantenimiento de la base de datos 
# de Unidades, Directorios y Archivos.

class BaseDatos:

    def __init__(self):
        # Comprobamos si la base de datos existe ya, en caso contrario hay que crearla. 
        # Esto, por supuesto, ocurrirá la primera vez que se ejecute el programa.
        BDfile = u'.\Espacio\espacio.sqlite'
        if not os.path.exists(BDfile):
            self.bd = sqlite3.connect(BDfile)
            
            # Una vez creado y conectado el archivo, hemos de crear las tablas
            self.bd.execute('''create table archivos
            (numserie int, path text, nombre text, extension text, tipo text, fechamod text,tamano int, hash int, fechaudit text)''')
            self.bd.execute('''create table directorios
            (numserie int, path text, fechamod text, numfiles int, numdir int, tamano int, fechaudit text)''')
            self.bd.execute('''create table unidades
            (numserie text, volumen text, fechamod text, numfiles int, numdir int, tamano int, libre int, fechaudit text)''')
        else:
            self.bd = sqlite3.connect(BDfile)
        # Con la base de datos en memoria, vamos a definir la propiedad cursor para utilizarlo.
        self.cursor = self.bd.cursor()


    def __del__(self):
        # Al eliminar el objeto se ejecuta este código que cierra la base de datos
        self.bd.close()


    def Leerunidades(self):
        # Esta función se encargará de devolver la lista de unidades
        salida = []
        salida += self.cursor.execute("select * from unidades")
        return salida


    def Leerdirectorios(self, numserie):
        # Esta función se encargará de devolver los directorios de la unidad = numserie.
        salida = []
        salida += self.cursor.execute("select * from directorios where numserie = '%s'" % numserie)
        return salida


    def Grabarunidad(self, infounidad):
        # inserta los datos en la tabla
        self.cursor.execute('''insert into unidades values
			(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')''' 
			% infounidad)
        self.bd.commit()


    def Grabardir(self, infodir):
        # inserta los datos en la tabla
        self.cursor.execute('''insert into directorios values
			(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')''' 
			% infodir)
        self.bd.commit()


    def Grabarfile(self, infofile):
        # inserta los datos en la tabla
        self.cursor.execute('''insert into archivos values
			(\'%s\', \'%s\', \"%s\", \"%s\", \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')''' 
			% infofile)
        self.bd.commit()
