# -*- coding: utf-8 -*-

# Proyecto ESPACIO 1.3, analizador de discos (unidades, carpetas, usbs).
# ======================================================================
#
# 06/09/2017	Mejoras a realizar: 
#
#		1) Ser capaz de importar la estructura de directorios y archivos del fichero .csv.

import sys, time


# Módulos del proyecto
import lectura   as l		# Módulo de lectura de información de la Unidad, extrae sus directorios y ficheros
import grabarcsv as g		# Módulo que exporta la información de la Unidad a fichero .CSV





def obtener_ruta():
	ruta = ''
	try:
		ruta = sys.argv[1]
	except:
		print ('No ha introducido parámetro. Cargamos en memoria las unidades.', '\n')
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
		g.Exportar_csv(unidad)
	else:
		# Leer una unidad del fichero .CSV
		unidad = g.Leer_csv()
		
		# La volvemos a exportar para verificar que se ha leído correctamente
		g.Exportar_csv(unidad)

# Borramos la variable Unidad
del unidad
