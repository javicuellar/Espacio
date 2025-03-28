# -*- coding: utf-8 -*-

import os, sys, time

# Paquetes del proyecto
import analisisdir as a		# Analiza el resultado del comando DIR para extraer información de la unidad
import grabarcsv   as g



tmp = '.\Espacio\\Tmp\\tmp.txt'
informe = '.\Espacio\\Tmp\\tmp.csv'


def obtener_ruta():
	ruta = ''
	try:
		ruta = sys.argv[1]
	except:
		print ('Por favor indique unidad a leer.')
	return ruta


def capturar_dir(ruta):
	s = os.popen('dir ' + ruta + u' /s > ' + tmp)
	s.close()



	
if __name__ == "__main__":
	ruta = obtener_ruta()
	
	if ruta != '':
		tiempo_inicial = time.time() 
		
		capturar_dir(ruta)

		# Analizar el DIR mapeado para extraer información de la unidad, directorios y ficheros.
		# Devuelve la clase Unidad que contiene los subdirectorios.
		uni = a.analizar(tmp)
		
		tiempo_final = time.time() 
		print (tiempo_final - tiempo_inicial)
		
		# Utilizamos módulo grabarcsv para exportar la información de la unidad a fichero .CSV
		g.Exportarcsv(uni, informe)
		
		# borramos fichero temporal
		#os.remove(tmp)
