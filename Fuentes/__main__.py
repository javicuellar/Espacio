# -*- coding: utf-8 -*-

import sys, time


# M�dulos del proyecto
import lectura   as l		# M�dulo de lectura de informaci�n de la Unidad, extrae sus directorios y ficheros
import grabarcsv as g		# M�dulo que exporta la informaci�n de la Unidad a fichero .CSV





def obtener_ruta():
	ruta = ''
	try:
		ruta = sys.argv[1]
	except:
		print ('Por favor indique unidad a leer.')
	return ruta




if __name__ == "__main__":
	ruta = obtener_ruta()
	
	if ruta != '':
		tiempo_inicial = time.time() 
		
		# Analizar la informaci�n de la unidad, directorios y ficheros y
		# se almacena en memoria en clase Unidad, Directorios y Ficheros
		unidad = l.leer(ruta)
		
		tiempo_final = time.time() 
		print (tiempo_final - tiempo_inicial)
		
		# Utilizamos m�dulo grabarcsv para exportar la informaci�n de la unidad a fichero .CSV
		g.Exportarcsv(unidad)
