# -*- coding: utf-8 -*-

import sys, time


# Módulos del proyecto
import lectura   as l		# Módulo de lectura de información de la Unidad, extrae sus directorios y ficheros
import grabarcsv as g		# Módulo que exporta la información de la Unidad a fichero .CSV





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
		
		# Analizar la información de la unidad, directorios y ficheros y
		# se almacena en memoria en clase Unidad, Directorios y Ficheros
		unidad = l.leer(ruta)
		
		tiempo_final = time.time() 
		print (tiempo_final - tiempo_inicial)
		
		# Utilizamos módulo grabarcsv para exportar la información de la unidad a fichero .CSV
		g.Exportarcsv(unidad)
