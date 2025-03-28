# -*- coding: utf-8 -*-

# Módulo memoria del Proyecto ESPACIO 1.3, analizador de discos (unidades, carpetas, usbs).
# =========================================================================================
#
# 07/09/2017	- Se crea una nueva clase, Discos, que contiene una lista de unidades
#				- Se crea métodos de Discos para leer unidad a partir de una ruta y leer las unidades
#				de un fichero .CSV.

import time


# Módulos del proyecto
import lectura    as l		# Módulo de lectura de información de la Unidad, extrae sus directorios y ficheros
import ficherocsv as f		# Módulo que lee y graba la información de la Unidad a fichero .CSV

	

class Discos():
	def __init__(self):
		self.unidades = []

		
	def Leer_disco(self, ruta):
		tiempo_ini = time.time() 
		# Analizar la información de la ruta (unidad, directorios y ficheros) y
		# la incorpora como clase Unidad (Unidad, Directorios y Ficheros)
		volumen, libre, faudit = l.Leer_unidad(ruta)

		# Creamos la clase Unidad con la información que tenemos
		unidad = Unidad(volumen, libre, faudit)
		unidad.leer_directorio(ruta)
	
		self.unidades.append(unidad)

		tiempo_fin = time.time() 
		print ('\n', 'Tiempo lectura ', ruta, ': ', tiempo_fin - tiempo_ini)
		self.Existe_unidad()

	
	def Leer_csv(self):
		# Lee del fichero .CSV todas las unidades que contine.
		tiempo_ini = time.time() 
		file_csv = f.FileCSV('r')
		
		reg = file_csv.Leer_registro()		# Leemos cabecera e ignoramos
		reg = file_csv.Leer_registro()

		# Procesamos los registros leídos del fichero .CSV hasta el final del fichero
		while reg != '':
			procesado = True

			if reg[0] == 'U':		
				# Es una Unidad, la procesamos creando la Unidad y su Directorio ppal.
				dire = self.crear_unidad(reg)
	
			# Tratamos registro léido hasta final del fichero o que se procese el registro
			while reg != '' and procesado:
				ruta = dire.path
				if ruta != '':
					ruta += '\\'
			
				ruta_nueva = reg[3]
				if ruta_nueva != '':
					ruta_nueva += '\\'
			
				if ruta_nueva.find(ruta) > -1 or ruta == '':
					# La nueva ruta leída está dentro de la ruta del directorio actual -> lo procesamos
					if reg[0] == 'A':		# Es una archivo, lo incorporamos al directorio
						nom, ext, tipo, fmod, tam, error = f.Info_fichero(reg)
						fichero = Fichero(nom, ext, tipo, fmod, tam, error)
						
						dire.ficheros.append(fichero)
				
					elif reg[0] == 'D':		# Es un directorio, lo incorporamos a sus subdirectorios
						ruta, fmod, nfiles, ndir, tam, error = f.Info_directorio(reg)
						subdir = Directorio(ruta, fmod, nfiles, ndir, tam, error, dire)
						
						dire.subdirectorios.append(subdir)
						# Nos movemos al subdirectorio leído para incorporar sus ficheros o subdirectorios
						dire = subdir
				
					procesado = False
				else:
					# El directorio donde estamos (DIRE) no contiene al nuevo directorio, subimos de dir.
					dire = dire.dirpadre
			
			# Leemos el siguiente registro del fichero .CSV
			reg = file_csv.Leer_registro()
	
		tiempo_fin = time.time() 
		print ('\n', 'Tiempo leer fichero CSV: ',tiempo_fin - tiempo_ini)
		
		del file_csv
	


	def Exportar_csv(self, tipo, maxnivel=1):
		tiempo_ini = time.time() 
		file_csv = f.FileCSV('w', tipo)
		
		info_discos = []
		for unidad in self.unidades:
			info_discos += unidad.exportar(tipo, maxnivel)
		
		# Grabamos la información de discos (una lista) llamando a la función Grabar_CSV
		file_csv.Grabar_CSV(info_discos, tipo)
		
		tiempo_fin = time.time() 
		print ('\n', 'Tiempo exportar a CSV: ', tiempo_fin - tiempo_ini)
		
		del file_csv


	def crear_unidad(self, csv):
		volumen, libre, faudit = f.Info_unidad(csv)
		unidad = Unidad(volumen, libre, faudit)
			
		ruta, fmod, nfiles, ndir, tam, error = f.Info_directorio(csv)
		unidad.directorio = Directorio(ruta, fmod, nfiles, ndir, tam, error, 0)
				
		self.unidades.append(unidad)
		return unidad.directorio


	def Listar_unidades(self):
		for unidad in self.unidades:
			unidad.imprimir()


	def Existe_unidad(self):
		# Comprueba si la última unidad cargada en memoria existe ya
		unidad_leida = self.unidades[len(self.unidades) - 1]
		for num in range(len(self.unidades) - 1):
			if self.unidades[num].volumen == unidad_leida.volumen:
				self.unidades[num].backup_csv()
				self.unidades.pop(num)
				
				


# para buscar una lista en otra, quizas me sirma para buscar ficheros en ficheros.
'''
import time

valores = range(40000)
datos = range(0, 10000, 3)

i = time.time()
True in [v in datos for v in valores]
time_option1 = time.time() - i

i = time.time()
any(v in datos for v in valores)
time_option2 = time.time() - i

print time_option1
print time_option2
}}}

>>> 2.96800017357
0.0			
'''

class Unidad():
	def __init__(self, volumen, libre, fechaudit):
		self.volumen = volumen
		self.libre = libre
		self.fechaudit = fechaudit
	
	def leer_directorio(self, ruta):
		self.directorio = Directorio(ruta, '', 0, 0, 0, '', 0)
		self.directorio.leer_directorio()
		self.directorio.act_directorio()
	
	def imprimir(self):
		print ('-' * 75)
		print ('\n', self.volumen, self.libre, self.fechaudit, '\n')
	
	def exportar(self, tipo, max_nivel):
		salida = [['U', self.volumen, self.libre, self.fechaudit]]
		salida += self.directorio.exportar(tipo, 0, max_nivel)
		return salida

	def backup_csv(self):
		tiempo_ini = time.time() 
		file_csv = f.FileCSV('a')
		
		# Grabamos en backup la información de la unidad
		file_csv.Grabar_CSV(self.exportar())
		
		tiempo_fin = time.time() 
		print ('\n', 'Tiempo exportar a CSV: ', tiempo_fin - tiempo_ini)
		
		del file_csv




class Directorio():
	def __init__(self, path, fechamod, numfiles, numdir, tamano, error, dirpadre):
		self.path = path
		self.fechamod = fechamod
		self.numfiles = numfiles
		self.numdir = numdir
		self.tamano = tamano
		self.error = error
		self.dirpadre = dirpadre
		self.ficheros = []
		self.subdirectorios = []
		
	
	def leer_directorio(self):
		archivos, directorios, error = l.Leer_ruta(self.path)
		
		tamano, fechamod = 0, ''
		for file in archivos:
			nom, ext, t, fmod, tam, erfile = l.Leer_file(self.path, file)
			fichero = Fichero(nom, ext, t, fmod, tam, erfile)
			self.ficheros.append(fichero)
		
			self.tamano += fichero.tamano
			if self.fechamod < fichero.fechamod:
				self.fechamod = fichero.fechamod
		
		self.numfiles = len(self.ficheros)
		self.error = error
		
		for dir in directorios:
			subdirectorio = Directorio(dir, '', 0, 0, 0, '', self)
			self.subdirectorios.append(subdirectorio)
			subdirectorio.leer_directorio()
	
	
	def act_directorio(self):
		self.path = self.path[3:]
		
		for dir in self.subdirectorios:
			dir.act_directorio()
			self.numfiles += dir.numfiles
			self.numdir += dir.numdir + 1
			self.tamano += dir.tamano
			if self.fechamod < dir.fechamod:
				self.fechamod = dir.fechamod

	
	def imprimir(self):
		print ('\n', '*' * 75)
		print ('\nDir.: ', self.fechamod, self.path, self.numfiles, self.numdir, self.tamano, '\n')
		for file in self.ficheros:
			file.imprimir()
		for dir in self.subdirectorios:
			dir.imprimir()

	def exportar(self, tipo, nivel, max_nivel):
		salida = [['D', self.path, self.fechamod, self.numfiles, self.numdir, self.tamano, self.error, nivel]]

		if tipo == 'T':
			for file in self.ficheros:
				salida.append(file.exportar(nivel))
		
		if tipo == 'T' or (tipo == 'D' and nivel < max_nivel):
			for dir in self.subdirectorios:
				salida += dir.exportar(tipo, nivel + 1, max_nivel)

		return salida


        
class Fichero():
	def __init__(self, nombre, extension, tipo, fechamod, tamano, error):
		self.nombre = nombre
		self.extension = extension
		self.tipo = tipo
		self.fechamod = fechamod
		self.tamano = tamano
		self.error = error

	def imprimir(self):
		print ('   - ', self.fechamod, self.nombre, self.extension, self.tipo, self.tamano)
		
	def exportar(self, nivel):
		return ['A', self.nombre, self.extension, self.fechamod, self.tamano, self.tipo, self.error, nivel]



if __name__ == "__main__":
	pass
