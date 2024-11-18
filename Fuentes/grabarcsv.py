# -*- coding: utf-8 -*-

import os, csv




def Exportarcsv(unidad, filecsv):
	#doc = open(filecsv, 'w', newline='')
	doc = open(filecsv, 'a', newline='')
	
	doc_csv_w = csv.writer(doc, delimiter=';') 	  # variable declarada por convencion entre programadores

	# Grabamos la cabecera de las columnas del fichero .CSV
	cabecera = ('Volumen', 'Directorio', 'Nombre', 'Fecha Mod.', 'Ficheros', 'Directorios', 'Tamaño', 'Libre', 'Fecha')
	doc_csv_w.writerow(cabecera)
	
	# Obtenemos el Directorio principal de la unidad
	dir = unidad.directorio
	
	# Usamos método exportarcsv del Directorio Principal para extraer la información de sus ficheros y subdirectorios
	for reg in dir.exportarcsv(unidad.volumen, unidad.libre, unidad.fechaudit):
		doc_csv_w.writerow(reg)
	
	doc.close()
