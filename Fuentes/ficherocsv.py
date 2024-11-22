# -*- coding: utf-8 -*-

import os, csv

# Paquetes del proyecto
import mapeo	as c		# Contien funciones para mapear una línea de un fichero, mapear palabras


filecsv = u'.\Espacio\Tmp\Informe.csv'
unidades = u'.\\Espacio\\Tmp\\Unidades.csv'
directorios = u'.\\Espacio\\Tmp\\Directorios.csv'
backup = u'.\Espacio\Tmp\Backup.csv'


class FileCSV():
	def __init__(self, modo, tipo='T'):
		file = filecsv
		if modo == 'a':
			file = backup
		if tipo == 'U':
			file = unidades
		elif tipo == 'D':
			file = directorios
		
		self.doc = open(file, modo, newline='')	  # modo w=escribir, a=añadir 
		
		if modo == 'w' or modo == 'a':
			self.doc_csv = csv.writer(self.doc, delimiter=';') 	  	# variable declarada por convencion
			
			if tipo == 'T':
				# Grabamos la cabecera de las columnas del fichero .CSV
				cabecera = ('Tipo', 'Nivel Dir', 'Disco', 'Directorio', 'Nombre', 'Fecha Mod.', 'Ficheros',
							'Directorios', 'Tamaño', 'Bytes', 'Libre', 'Fecha', 'Error')
			else:
				# Formato salida: [f. analisis, volumen, directorio, tamaño, fecha modificación,  
				# num. ficheros, num. directorios, espacio libre, error
				cabecera = ('Fecha', 'Disco', 'Directorio', 'Tamaño', 'Fecha Mod.', 
							'Ficheros', 'Directorios', 'Libre', 'Error')
			
			self.doc_csv.writerow(cabecera)
		else:
			self.doc_csv = csv.reader(self.doc, delimiter=';') 	# variable declarada por convencion

			
	def Leer_registro(self):
		try:
			return next(self.doc_csv)
		except StopIteration:
			return ''


	def escribir_registro(self, registro):
		self.doc_csv.writerow(registro)


	def Grabar_CSV(self, lista, tipo):
		# Formateamos la salida dependiendo si es información de Unidad, Directorio o Fichero
		for reg in lista:
			if reg[0] == 'U':	   # Contiene info unidad.: volumen, espacio_libre, fecha uditoria
				vol, err = c.mapeo_string(reg[1])
				libre = reg[2]
				faudit = reg[3]
			elif reg[0] == 'D':	   # contiene info dir....: path, fechamod, numfiles, numdir, tamano, error, nivel
				if tipo == 'T' or (libre != 0 and tipo == 'U') or (libre == 0 and tipo == 'D' and reg[6] != ' (Acceso Denegado)'):
					self.escribir_registro(formato_directorio(reg, vol, libre, faudit, tipo))
				
				ruta, err = c.mapeo_string(reg[1])
				libre = 0
			elif reg[0] == 'A':	   # contiene info archivo:  nombre, extension, fechamod, tamano, tipo, error, nivel
				self.escribir_registro(formato_archivo(reg, vol, faudit, ruta))
			else:
				print ('Info de unidad errónea al formatear salida a csv.')


	def __del__(self):
		self.doc.close()

				



def Info_unidad(reg):
	# Clase Unidad: volumen, espacio_libre, fechaudit
	return reg[2], int(reg[13]), reg[11]
	
def Info_directorio(reg):
	# Clase Directorio: path, fechamod, numfiles, numdir, tamano, error
	return reg[3], reg[5], int(reg[6]), int(reg[7]), int(reg[9]), reg[12]

def Info_fichero(reg):
	nombre, extension = os.path.splitext(reg[4])
	# Clase Fichero: nombre, extension, tipo, fechamod, tamano, error
	return nombre, extension, reg[10], reg[5], int(reg[9]), reg[12]

		

def formato_archivo(infoarchivo, vol, faudit, ruta):
	# Info archivo: nombre, extension, fechamod, tamano, tipo, error, nivel
	nombre, err = c.mapeo_string(infoarchivo[1]+infoarchivo[2])
	if infoarchivo[6] == '' and err != '':
		infoarchivo[6] = err

	if infoarchivo[4] < 1024*1024*1024:
		tam = str(infoarchivo[4])
	else:
		tam = '%.2f' % (infoarchivo[4]/(1024*1024*1024)) + ' GB.'
	
	# Formato salida: ['U', nivel dir., volumen, directorio, nombre completo, fecha modificación,  
	# 		num. ficheros y dir. vacío, tamaño formateado, tamaño, tipo archivo y fecha revisión
	salida = ['A', infoarchivo[7], vol, ruta, nombre, infoarchivo[3], 
			'', '', tam, infoarchivo[4], infoarchivo[5], faudit, infoarchivo[6]]
	return salida


def formato_directorio(infoarchivo, vol, libre, faudit, tipo):
	if libre != 0:		# es el primer directoiro, formateamos como unidad
		tip = 'U'
		if libre < 1024*1024:
			lib = '%.2f' % (libre/(1024)) + ' KB.'
		elif libre < 1024*1024*1024:
			lib = '%.2f' % (libre/(1024*1024)) + ' MB.'
		else:
			lib = '%.2f' % (libre/(1024*1024*1024)) + ' GB.'
	else:
		tip = 'D'
		lib = ''
	
	# Info directorio: path, fechamod, numfiles, numdir, tamano, error
	ruta, err = c.mapeo_string(infoarchivo[1])
	if infoarchivo[6] == '' and err != '':
		infoarchivo[6] = err
	
	if infoarchivo[5] < 1024:
		tam = str(infoarchivo[5]) + ' Bytes'
	elif infoarchivo[5] < 1024*1024:
		tam = '%.2f' % (infoarchivo[5]/(1024)) + ' KB.'
	elif infoarchivo[5] < 1024*1024*1024:
		tam = '%.2f' % (infoarchivo[5]/(1024*1024)) + ' MB.'
	else:
		tam = '%.2f' % (infoarchivo[5]/(1024*1024*1024)) + ' GB.'

	if tipo == 'T':
		# Formato salida: ['D', nivel dir, volumen, directorio, vacío, fecha modificación,  
		# 		num. ficheros, num. directorios, tamaño formateado, tamaño, tipo archivo y fecha revisión
		salida = [tip, infoarchivo[7], vol, ruta, '', infoarchivo[2], 
				infoarchivo[3], infoarchivo[4], tam, infoarchivo[5], lib, faudit, infoarchivo[6], libre]
	else:
		# Formato salida: [f. analisis, volumen, directorio, tamaño, fecha modificación,  
		# 		num. ficheros, num. directorios, espacio libre, error
		salida = [faudit, vol, ruta, tam, infoarchivo[2], 
				infoarchivo[3], infoarchivo[4], lib, infoarchivo[6]]
	return salida
