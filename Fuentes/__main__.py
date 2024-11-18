# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, time
import lectura   as l
import grabacion as g
import analisis  as a




def leer(path, numserie, fechaudit):
	archivos, directorios, error = l.leerdir(path)
	numdir, numfile, peso, fechamod = 0,0,0, ''
	for dir in directorios:
		numdir += 1
		(p,c,d,f,e) = leer(dir, numserie, fechaudit)
		numdir += d
		f = f + e
		tablas.Grabardir((numserie, dir, f, c, d, p, fechaudit))
					#(numserie, path, fechamod, numfiles, numdir, tamano, fechaudit)
		peso += p
		numfile += c
		fechamod = f
	#print ('      Directorio: ', path)					# debug directorio leido
	for file in archivos:
		numfile += 1
		infofile = l.leerfile(path, file, numserie)
		peso += infofile[6]
		if fechamod < infofile[5]:
			fechamod = infofile[5]
		tablas.Grabarfile(infofile)
	print ('> Directorio: ', path, '  Num. files: ', numfile, '  Num. dir: ', numdir, '  Peso: ', peso)	# debub num. archivos y tamano
	return (peso, numfile, numdir, fechamod, error)



tablas = g.BaseDatos() 

try:
	path = sys.argv[1]
	print ('  > Path: ', path)
	print ('-' * 70)
	
	tiempo_inicial = time.time()
		
	infounidad = l.leerunidad(path)		#(numserie, volumen, fechamod, numfiles, numdir, tamano, libre, fechaudit)

	infounidad[5], infounidad[3], infounidad[4], infounidad[2], error = leer(path, infounidad[0], infounidad[7])

	tuplaunidad = tuple(infounidad)
	print (tuplaunidad)
	tablas.Grabarunidad(tuplaunidad)

	tiempo_final = time.time() 
	print (tiempo_final - tiempo_inicial)

except:
	# Si no se pasa par�metros con la ruta a analizar
	# Sacar un informe en fichero excel (formato .csv) de las unidades

	tiempo_inicial = time.time()
	
	unidades = tablas.Leerunidades()

	directorios = []
	for unidad in unidades:
		directorios += tablas.Leerdirectorios(unidad[0])
		
	listaunidades, dicnumserie = a.FormatoUnidaddes(unidades)
	exportar = listaunidades + a.FormatoDirectorios(directorios, dicnumserie)
		
	a.Exportarcsv(exportar)

	tiempo_final = time.time() 
	print (tiempo_final - tiempo_inicial)
