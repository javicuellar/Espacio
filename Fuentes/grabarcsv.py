# -*- coding: utf-8 -*-

import os, csv

# Paquetes del proyecto
import mapeo	as c		# Contien funciones para mapear una línea de un fichero, mapear palabras

'''
import locale

# Definimos el formato que deseamos
locale.setlocale(locale.LC_ALL, "es_ES.utf-8")


def formateo_num(num):
	return locale.format("%.*f", (2,num), True)
'''


filecsv = u'.\Espacio\Tmp\Informe.csv'



def Exportarcsv(unidad):
	doc = open(filecsv, 'w', newline='')
	#doc = open(filecsv, 'a', newline='')
	
	doc_csv_w = csv.writer(doc, delimiter=';') 	  # variable declarada por convencion entre programadores

	# Grabamos la cabecera de las columnas del fichero .CSV
	cabecera = ('Tipo', 'Volumen', 'Directorio', 'Nombre', 'Fecha Mod.', 'Ficheros', 'Directorios', 'Tamaño', 'Libre', 'Fecha')
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
		if info[0] == 'u':		# contiene info unidad.:   	numserie, volumen, espacio_libre, fechaudit
			vol = c.mapeo_string(info[2])
			libre = info[3]
			faudit = info[4]
		elif info[0] == 'd':	# contiene info dir....: 	path, fechamod, numfiles, numdir, tamano, error
			salida.append(formato_directorio(info, vol, libre, faudit))
			ruta = c.mapeo_string(info[1][3:])
			tamanodir = info[5]
			libre = 0
		elif info[0] == 'a':	# contiene info archivo: 	nombre, extension, fechamod, tamano, tipo
			salida.append(formato_archivo(info, vol, faudit, ruta))
		else:
			print ('Info de unidad errónea al formatear salida a csv.')
	return salida



def formato_archivo(infoarchivo, vol, faudit, ruta):
	# Info archivo: nombre, extension, fechamod, tamano, tipo, error
	if infoarchivo[4] < 1024*1024*1024:
		tam = str(infoarchivo[4])
	else:
		tam = '%.2f' % (infoarchivo[4]/(1024*1024*1024)) + ' GB.'

	salida = ['A', vol, ruta, c.mapeo_string(infoarchivo[1]+infoarchivo[2]+infoarchivo[6]), infoarchivo[3], '', '', 
			tam, infoarchivo[5], faudit]
	# Formato salida: ['U', volumen, directorio, nombre completo, fecha modificación,  num. ficheros y dir. vacío
	# 		tamaño, tipo archivo y fecha revisión
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
	if infoarchivo[5] < 1024:
		tam = str(infoarchivo[5]) + ' Bytes'
	elif infoarchivo[5] < 1024*1024:
		tam = '%.2f' % (infoarchivo[5]/(1024)) + ' KB.'
	elif infoarchivo[5] < 1024*1024*1024:
		tam = '%.2f' % (infoarchivo[5]/(1024*1024)) + ' MB.'
	else:
		tam = '%.2f' % (infoarchivo[5]/(1024*1024*1024)) + ' GB.'

	salida = [tipo, vol, c.mapeo_string(infoarchivo[1][3:])+infoarchivo[6], '', infoarchivo[2], 
			infoarchivo[3], infoarchivo[4], tam, lib, faudit]
	# Formato salida: ['D', volumen, directorio, vacío, fecha modificación,  
	# 		num. ficheros, num. directorios, tamaño, tipo archivo y fecha revisión
	return salida
