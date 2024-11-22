# -*- coding: utf-8 -*-

import os, time

# Paquetes del proyecto
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero



tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 


fec_display = '%Y-%m-%d %H:%M:%S'   # establece formato de fecha-hora
sintipo = []



def analizar(fich):
	with open(fich, 'r') as f:
		# Leyendo fichero con el contenido de un comando DIR en DOS
		# Las dos primeras líneas contienes el volumen y el número de serie (clave de las unidades)
		vol = f.readline()[30:-1]		# extraemos el nombre del volumen de la línea 1
		nserie = f.readline()[36:-1]	# extraemos el numero de serie (clave) de la linea 2
		fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		# Creamos la clase Unidad con la información que tenemos
		unidad = m.Unidad(nserie, vol, 0, fechaudit)
		
		# Iniciamos contadores de directorio y ficheros y leemos la tercera línea vacía
		contdir, contfiles = 0, 0
		linea = f.readline()
		
		while True:
			linea = f.readline()
			if linea == '':
				break	# Hemos llegado al final del fichero y salimos del bucle
			
			elif len(linea) == 1:
				# Leyendo línea vacía que ignoramos
				pass
			
			elif linea[1:11] == 'Directorio': 
				# Comienzan los archivos de un directorio, creamos el subdirectorio
				dir = linea[15:-1]
				contdir += 1
				# Leemos dos líneas más, la primera vacía y la siguiente contiene la fecha de mod.
				linea = f.readline()
				linea = f.readline()
				fechamod = linea[0:17]
				
				# Grabamos directorio, falta información (numfiles, numdir, tamano)
				directorio = m.Directorio(dir, fechamod, 0, 0, 0)
				
				if contdir == 1:
					unidad.directorio = directorio
				else:
					unidad.directorio.subdirectorios.append(directorio)

			elif len(linea) > 34 and linea[1].isdigit() and linea[34].isdigit():
				# Leyendo la información de un fichero
				contfiles += 1
				fechamod = linea[0:17]
				tamano = int(linea[19:35].replace(' ', '').replace('.', ''))
				nombre, extension = os.path.splitext(linea[36:-1])
				tipo = ''
				if extension in tipos:
					tipo = tipos[extension]
				elif not extension in sintipo:
					sintipo.append(extension)
				
				directorio.ficheros.append(m.Fichero(nombre, extension, tipo, fechamod, tamano))
				
			elif linea[5:10] == 'Total': 
				# Leyendo las últimas líneas con la información de num. ficheros y num. dir.
				# y espacio libre en la unidad
				linea = f.readline()
				contfiles = int(linea[5:17].replace(' ', '').replace('.', ''))	
				tamano = int(linea[26:40].replace(' ', '').replace('.', ''))
								
				linea = f.readline()
				contdir = int(linea[5:17].replace(' ', '').replace('.', ''))
				elibre = int (linea[22:linea.find('bytes')].replace(" ","").replace(".",""))
				
				# Actualizamos num. ficheros, num. dir., tamano y espacio libre de la Unidad
				unidad.directorio.numfiles = contfiles
				unidad.directorio.numdir = contdir
				unidad.directorio.tamano = tamano
				unidad.libre = elibre
	return unidad
	


	
if __name__ == "__main__":
	pass
