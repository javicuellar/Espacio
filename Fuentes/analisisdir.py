# -*- coding: utf-8 -*-

import os, time

# Paquetes del proyecto
import memoria 	as m		# Contiene las Clases Unidad / Directorio / Fichero


tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 
sintipo = []


dicbyte = { b'\x81' : b'u',	 b'\xa6' : b'a', b'\xad' : b'!', 	# caractéres no válidos
			b'\xa0' : b'\xe1',	# á
			b'\x82' : b'\xe9',	# é
			b'\xa1' : b'\xed',	# í
			b'\xa2' : b'\xf3',	# ó
			b'\xa3' : b'\xfa', 	# ú
			b'\xa4' : b'\xf1' 	# ñ
			}


fec_display = '%Y-%m-%d %H:%M:%S'   # establece formato de fecha-hora



def leerlinea(file):
	linea, byte = '', b' '
	byte = file.read(1)
	while byte != b'' and byte != b'\r':
		if byte in dicbyte:
			# caracter transformado que da error o es invalido
			byte = dicbyte[byte]
		linea += byte.decode(u'cp1252')
		#print ('l: ', linea)
		byte = file.read(1)
	#print (linea, ' > ', linea[2:12])
	return linea


def calculardirectorio(directorio, ruta):
	num_subdir = len(directorio.subdirectorios) - 1
	subdir = directorio.subdirectorios
	
	for dir in range(num_subdir, -1, -1):
		if ruta.find(subdir[dir].path) == 0:
			return calculardirectorio(subdir[dir], ruta)
	return directorio
		

def actdirectorio(directorio):
	for dir in directorio.subdirectorios:
		actdirectorio(dir)
		directorio.numfiles += dir.numfiles
		directorio.numdir += dir.numdir + 1
		directorio.tamano += dir.tamano


def analizar(fich):
	with open(fich, 'rb') as f:
		# Leyendo fichero con el contenido de un comando DIR en DOS
		# Las dos primeras líneas contienes el volumen y el número de serie (clave de las unidades)
		vol = leerlinea(f)[30:]			# extraemos el nombre del volumen de la línea 1
		nserie = leerlinea(f)[36:]	# extraemos el numero de serie (clave) de la linea 2
		fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		
		# Creamos la clase Unidad con la información que tenemos
		unidad = m.Unidad(nserie, vol, 0, fechaudit)
		
		# Iniciamos contadores de directorio y ficheros y leemos la tercera línea vacía
		contdir = 0
		linea = leerlinea(f)
		
		while True:
			linea = leerlinea(f)
			if linea == '':
				break	# Hemos llegado al final del fichero y salimos del bucle
			
			elif len(linea) == 1:
				# Leyendo línea vacía que ignoramos
				pass
			
			elif linea[2:12] == 'Directorio': 
				# Comienzan los archivos de un directorio, creamos el subdirectorio
				dir = linea[16:]
				# Leemos dos líneas más, la primera vacía y la siguiente contiene la fecha de mod.
				linea = leerlinea(f)
				linea = leerlinea(f)
				fechamod = linea[1:18]
				
				# Actualizamos el número de fihceros del directorio leído anteriormente
				if contdir > 0:
					dirleido.numfiles = contfiles
					dirleido.tamano = tamfiles
				
				# Grabamos directorio, falta información (numfiles, numdir, tamano)
				dirleido = m.Directorio(dir, fechamod, 0, 0, 0)
				
				if contdir == 0:
					unidad.directorio = dirleido
				elif contdir == 1:
					unidad.directorio.subdirectorios.append(dirleido)
				else:
					calculardirectorio(unidad.directorio, dir).subdirectorios.append(dirleido)
				
				contdir += 1
				contfiles, tamfiles = 0, 0

			elif len(linea) > 34 and linea[1].isdigit() and linea[35].isdigit():
				# Leyendo la información de un fichero
				fechamod = linea[1:18]
				tamano = int(linea[19:36].replace(' ', '').replace('.', ''))
				nombre, extension = os.path.splitext(linea[37:])
				tipo = ''
				if extension.lower() in tipos:
					tipo = tipos[extension.lower()]
				elif not extension.lower() in sintipo:
					sintipo.append(extension.lower())
				
				contfiles += 1
				tamfiles += tamano
				
				dirleido.ficheros.append(m.Fichero(nombre, extension, tipo, fechamod, tamano))
				
			elif linea[6:11] == 'Total': 
				# Actualizamos el número de fihceros del directorio leído anteriormente
				if contdir > 1:
					dirleido.numfiles = contfiles
					dirleido.tamano = tamfiles

				# Leyendo las últimas líneas con la información de num. ficheros y num. dir.
				# y espacio libre en la unidad
				linea = leerlinea(f)
				contfiles = int(linea[5:17].replace(' ', '').replace('.', ''))	
				tamano = int(linea[28:42].replace(' ', '').replace('.', ''))
								
				linea = leerlinea(f)
				elibre = int (linea[23:linea.find('bytes')].replace(" ","").replace(".",""))
				
				unidad.libre = elibre
	
	actdirectorio(unidad.directorio)
	
	return unidad

	
if __name__ == "__main__":
	pass
