# -*- coding: utf-8 -*-

import os, csv

# Paquetes del proyecto
import mapeo	as c		# Contien funciones para mapear una línea de un fichero, mapear palabras
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero


filecsv = u'.\Tmp\Informe.csv'



def Exportar_csv(unidad):
	doc = open(filecsv, 'w', newline='')
	#doc = open(filecsv, 'a', newline='')
	
	doc_csv_w = csv.writer(doc, delimiter=';') 	  # variable declarada por convencion entre programadores

	# Grabamos la cabecera de las columnas del fichero .CSV
	cabecera = ('Tipo', 'Nivel Dir', 'Volumen', 'Directorio', 'Nombre', 'Fecha Mod.', 'Ficheros', 'Directorios', 'Tamaño',
				'Bytes', 'Libre', 'Fecha', 'Error')
	doc_csv_w.writerow(cabecera)

	# Obtenemos el Directorio principal de la unidad
	info_unidad = unidad.exportar()
	
	# Usamos método formatear salida para generar los registros del informe csv
	for registro in formato_csv(info_unidad):
		doc_csv_w.writerow(registro)
	
	doc.close()



def formato_csv(lista_unidad):
	salida = []
	for info in lista_unidad:
		if info[0] == 'U':		# contiene info unidad.: volumen, espacio_libre, fecha uditoria
			vol, err = c.mapeo_string(info[1])
			libre = info[2]
			faudit = info[3]
		elif info[0] == 'D':	# contiene info dir....: path, fechamod, numfiles, numdir, tamano, error, nivel
			salida.append(formato_directorio(info, vol, libre, faudit))
			ruta, err = c.mapeo_string(info[1])
			libre = 0
		elif info[0] == 'A':	# contiene info archivo:  nombre, extension, fechamod, tamano, tipo, error, nivel
			salida.append(formato_archivo(info, vol, faudit, ruta))
		else:
			print ('Info de unidad errónea al formatear salida a csv.')
	return salida



def formato_archivo(infoarchivo, vol, faudit, ruta):
	# Info archivo: nombre, extension, fechamod, tamano, tipo, error, nivel
	nombre, err = c.mapeo_string(infoarchivo[1]+infoarchivo[2])
	if infoarchivo[6] == '' and err != '':
		infoarchivo[6] = err

	if infoarchivo[4] < 1024*1024*1024:
		tam = str(infoarchivo[4])
	else:
		tam = '%.2f' % (infoarchivo[4]/(1024*1024*1024)) + ' GB.'
	
	salida = ['A', infoarchivo[7], vol, ruta, nombre, infoarchivo[3], 
			'', '', tam, infoarchivo[4], infoarchivo[5], faudit, infoarchivo[6]]
	# Formato salida: ['U', nivel dir., volumen, directorio, nombre completo, fecha modificación,  
	# 		num. ficheros y dir. vacío, tamaño formateado, tamaño, tipo archivo y fecha revisión
	return salida


def formato_directorio(infoarchivo, vol, libre, faudit):
	if libre != 0:		# es el primer directoiro, formateamos como unidad
		tipo = 'U'
		if libre < 1024*1024:
			lib = '%.2f' % (libre/(1024)) + ' KB.'
		elif libre < 1024*1024*1024:
			lib = '%.2f' % (libre/(1024*1024)) + ' MB.'
		else:
			lib = '%.2f' % (libre/(1024*1024*1024)) + ' GB.'
	else:
		tipo = 'D'
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

	salida = [tipo, infoarchivo[7], vol, ruta, '', infoarchivo[2], 
			infoarchivo[3], infoarchivo[4], tam, infoarchivo[5], lib, faudit, infoarchivo[6], libre]
	# Formato salida: ['D', nivel dir, volumen, directorio, vacío, fecha modificación,  
	# 		num. ficheros, num. directorios, tamaño formateado, tamaño, tipo archivo y fecha revisión
	return salida




def Leer_csv():
	doc = open(filecsv, 'r', newline='')
	
	doc_csv_r = csv.reader(doc, delimiter=';') 	  # variable declarada por convencion entre programadores
	
	# Leemos la cabecera del fichero CSV
	reg = leer_registro_csv(doc_csv_r)
	
	# Leemos el siguiente registro, debe ser una Unidad
	reg = leer_registro_csv(doc_csv_r)
	
	if reg[0] == 'U':		# Es una Unidad, la procesamos creando la Unidad y su Directorio ppal.
		unidad = crear_unidad(reg)
		directorio = unidad.directorio
	
	dire = directorio
	
	# Procesamos los registros leídos del fichero .CSV hasta el final del fichero
	while reg != '':
		# Leemos el siguiente registro del fichero .CSV
		reg = leer_registro_csv(doc_csv_r)
		procesado = True
		
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
					dire.ficheros.append(crear_fichero(reg))
				
				elif reg[0] == 'D':		# Es un directorio, lo incorporamos a sus subdirectorios
					subdir = crear_subdirectorio(reg, dire)
					dire.subdirectorios.append(subdir)
					# Nos movemos al subdirectorio leído para incorporar sus ficheros o subdirectorios
					dire = subdir
				
				procesado = False
			else:
				# El directorio donde estamos (DIRE) no contiene al nuevo directorio, subimos de dir.
				dire = dire.dirpadre
	
	doc.close()
	return unidad



def crear_unidad(reg):
	# Clase Unidad: volumen, espacio_libre, fechaudit
	unidad = m.Unidad(reg[2], int(reg[13]), reg[11])
	
	# Clase Directorio: path, fechamod, numfiles, numdir, tamano, error, dirpadre
	unidad.directorio = m.Directorio(reg[3], reg[5], int(reg[6]), int(reg[7]), int(reg[9]), reg[12], 0)
	return unidad


def crear_fichero(reg):
	nombre, extension = os.path.splitext(reg[4])
	# Clase Fichero: nombre, extension, tipo, fechamod, tamano, error
	return m.Fichero(nombre, extension, reg[10], reg[5], int(reg[9]), reg[12])


def crear_subdirectorio(reg, dir):
	# Clase Directorio: path, fechamod, numfiles, numdir, tamano, error, dirpadre
	return m.Directorio(reg[3], reg[5], int(reg[6]), int(reg[7]), int(reg[9]), reg[12], dir)



def leer_registro_csv(file_csv):
	try:
		return next(file_csv)
	except StopIteration:
		return ''
