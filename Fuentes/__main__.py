# -*- coding: utf-8 -*-

import os, sys, time

# Paquetes del proyecto
import leerbyte as l		# Lee el fichero en modo byte para transformar caractéres inválidos y españoles
import analisisdir as a		# Analiza el DIR de DOS para extraer la información de unidades, directorios y files.
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero



filein = '.\Espacio\leerdir.txt'
fileout = '.\Espacio\leerdir2.txt'


def obtener_ruta():
	ruta = ''
	try:
		ruta = sys.argv[1]
	except:
		print ('Por favor indique unidad a leer.')
	return ruta


def capturar_dir(ruta):
	s = os.popen('dir ' + ruta + u' /s > ' + filein)
	s.close()




if __name__ == "__main__":
	ruta = obtener_ruta()
	
	if ruta != '':
		tiempo_inicial = time.time() 
		
		capturar_dir(ruta)
		
		# Lectura del fichero filein byte a bye para mapear a unicode (tíldes, caracteres no válidos)
		l.mapeo(filein, fileout)
		
		# Analizar el DIR mapeado para extraer información de la unidad, directorios y ficheros.
		# Devuelve la clase Unidad que contiene los subdirectorios.
		uni = a.analizar(fileout)

		# Sacamos por pantalla la información de la Unidad y directorio principal.
		uni.imprimir()
		uni.directorio.imprimir()

		tiempo_final = time.time() 
		print (tiempo_final - tiempo_inicial)
