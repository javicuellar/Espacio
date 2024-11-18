# -*- coding: utf-8 -*-

import csv, os



def FormatoUnidaddes(lista):
	# Formato inicial
	# ('Num. Serie', 'Volumen', 'Fecha Mod.', 'Num. ficheros', 'Num. directorios', 'Tamaño', 'Libre', 'Fecha Análisis')
	# Eliminamos num. serie e incorporarmos Directorio entre el volumen y fecha de modificación
	salida, dicnumserie = [],{}
	for l in lista:
		lis = list(l)
		if not lis[0] in dicnumserie:
			dicnumserie[lis[0]] = lis[1]
		del lis[0]
		lis.insert(1, '')
		salida.append(lis)
	# Formato final
	# ('Volumen', 'Directorio', 'Fecha Mod.', 'Num. ficheros', 'Num. directorios', 'Tamaño', 'Libre', 'Fecha Análisis')
	return salida, dicnumserie



def FormatoDirectorios(lista, dicnumserie):
	# Formato inicial
	# ('Num. Serie', 'Path', 'Fecha Mod.', 'Num. ficheros', 'Num. directorios', 'Tamaño', 'Fecha Análisis')
	# Eliminamos num. serie e incorporarmos Volumen al principio y Libre entre tamaño y fecha análisis
	salida = []
	for l in lista:
		lis = list(l)
		if lis[0] in dicnumserie:
			lis[0] = dicnumserie[lis[0]]
		else:
			lis[0] = ''
		lis[1] = lis[1][3:]
		lis.insert(6, '')
		salida.append(lis)
	# Formato final
	# ('Volumen', 'Directorio', 'Fecha Mod.', 'Num. ficheros', 'Num. directorios', 'Tamaño', 'Libre', 'Fecha Análisis')
	return salida



def Exportarcsv(lista):
	informe = u'Informe.csv'
	
	if os.path.exists(informe):
		os.remove(informe)
	
	doc = open(informe, 'w', newline='')

	doc_csv_w = csv.writer(doc, delimiter=';') 	# variable declarada por convencion entre programadores

	cabecera = ('Volumen', 'Directorio', 'Fecha Mod.', 'Num. ficheros', 'Num. directorios', 'Tamaño', 'Libre', 'Fecha Análisis')
	doc_csv_w.writerow(cabecera)
	
	for unidad in lista:
		doc_csv_w.writerow(unidad)

	doc.close()   



if __name__ == "__main__":
	pass
