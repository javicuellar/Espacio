import os, sys, time
from stat import *

tipos = {'.py':'Python', '.pyc':'Python', '.txt':'texto', '.jpg':'foto', '.mp4':'video', '.doc':'documento','.docx':'documento',
		'.xls':'Excel', '.xlsx':'Excel', '.csv':'Excel', '.ppt':'presentacion', '.pptx':'presentacion', '.pdf':'pdf', '':'vacio',
		'.exe':'ejecutable', '.sqlite':'BDSqlite'} 

fec_display = '%Y-%m-%d %H:%M:%S'   # establece formato de fecha-hora

sintipo = []


def leerunidad(ruta):
	s = os.popen('dir ' + ruta)
	volumen = s.readline()[30:-1]
	numserie = s.readline()[36:-1]
	libre = 0
	for l in s.readlines():
		if l.count('dirs') != 0:
			libre = int (l[21:l.find('bytes')].replace(" ","").replace(".",""))
	fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	tamano, numfiles, numdir, fechamod = 0, 0, 0, ''
	return [numserie, volumen, fechamod, numfiles, numdir, tamano, libre, fechaudit]


def leerfile(ruta, archivo, numserie):
	nombre, extension = os.path.splitext(archivo)
	nombre_completo = os.path.join(ruta, archivo)
	e = os.stat(nombre_completo)
	tamanio = e.st_size
	fechamod = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e.st_mtime))
	fechaudit = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	tipo = ''
	if extension in tipos:
		tipo = tipos[extension]
	elif not extension in sintipo:
		sintipo.append(extension)
	peso = int(round(tamanio/1024))
	if peso == 0:
		peso = 1
	#print ('   --> ', nombre_completo, '    ', fechamod, ' ', peso, 'Kb.', ' ', tipo)	# debug archivos
	return (numserie, ruta, nombre, extension, tipo, fechamod, tamanio, 0, fechaudit)
	     # (codunidad, ruta, nombre, extension, tipo, fecha, tamaño, hash, fechaaudit)

def leerdir(ruta):
	files, subdir, error = [], [], ''
	try:
		for file in os.listdir(ruta):
			pathname = os.path.join(ruta, file)
			info = os.stat(pathname)
			if S_ISDIR(info.st_mode):    	# Tratamiento de subdirectorios
				subdir.append(pathname)
			elif S_ISREG(info.st_mode):  	# Tratamiento de archivos
				files.append(file)
			else:				 			# desconocido tipo de fichero
				print (' > Fichero desconocido %s' % pathname)
	except PermissionError:
			error = ' (Acceso Denegado)'
	return files, subdir, error

	
if __name__ == "__main__":
	print ('-' * 70)
	leerdir(sys.argv[1])
