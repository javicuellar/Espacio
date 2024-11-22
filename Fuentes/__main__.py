# -*- coding: utf-8 -*-

# Proyecto ESPACIO 1.3, analizador de discos (unidades, carpetas, usbs).
# ======================================================================
#
# 06/09/2017	Mejoras a realizar: 
#
#		1) Ser capaz de importar la estructura de directorios y archivos del fichero .csv.

import os

# Módulos del proyecto
import discos   as d		# Módulo de mantenimiento de Discos/Unidades/Directorios/Ficheros




def menu():
	print ('''
	1. Leer disco
	2. Listar unidades en memoria
	
	8. Leer fichero CSV
	9. Exportar a CSV Unidades
	0. Salir
		''')
	try:
		opcion = int(input('Introduzca opción: '))
	except:
		opcion = 9999
		print ('\n', 'Por favor introduzca un valor numérico.')
	return opcion



def valorar_opcion(opcion):
	os.system('CLS')	# Limpiamos la pantalla
	
	if opcion == 1: 
		ruta = input ('Introduzca ruta: ')
		# Analizar la información de la ruta introducida por parámetro (unidad, directorios y ficheros)
		discos.Leer_disco(ruta)

	elif opcion == 2:
		# Listar las unidades almacenadas en memoria
		discos.Listar_unidades()

	elif opcion == 8:
		# Leer unidades del fichero .CSV
		discos.Leer_csv()

	elif opcion == 9:
		# Exportamos la información de discos a fichero CSV
		opcion = 9999
		while opcion != 0:
			opcion = submenu_exportar()
			valorar_exportar(opcion)
		
		opcion = 9999
	elif opcion == 0:
		print("\n Adios....") 



def submenu_exportar():
	print ('''
	1. Unidades
	2. Directorios
	3. Todo
	0. Salir
		''')
	try:
		opcion = int(input('Introduzca opción: '))
	except:
		opcion = 9999
		print ('\n', 'Por favor introduzca un valor numérico.')
	return opcion



def valorar_exportar(opcion):
	if opcion == 1: 
		# Exportamos a fichero CSV solo las unidades
		discos.Exportar_csv('U')

	elif opcion == 2:
		max_nivel = int(input ('Introduzca nivel máximo de subdirectorios: '))
		# Exportamos a fichero CSV las unidades y directorios (niveles 0 y 1 por defecto)
		discos.Exportar_csv('D', max_nivel)

	elif opcion == 3:
		# Exportamos TODA la información de discos a fichero CSV
		discos.Exportar_csv('T')
	
	elif opcion == 0:
		print("\n Adios....") 



if __name__ == "__main__":
	opcion = 9999
	discos = d.Discos()
	
	while opcion != 0:
		opcion = menu()
		valorar_opcion(opcion)
	
	# Borramos la variable Unidad
	del discos
