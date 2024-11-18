# -*- coding: utf-8 -*-

'''
import locale

# Definimos el formato que deseamos
locale.setlocale(locale.LC_ALL, "es_ES.utf-8")


def formateo_num(num):
	return locale.format("%.*f", (2,num), True)
'''
	

class Fichero(object):
	def __init__(self, nombre, extension, tipo, fechamod, tamano):
		self.nombre = nombre
		self.extension = extension
		self.tipo = tipo
		self.fechamod = fechamod
		self.tamano = tamano

	def imprimir(self):
		print ('   - ', self.fechamod, self.nombre, self.extension, self.tipo, self.tamano)
		
	def exportarcsv(self, vol, ruta, faudit, tamanodir):
		nom = self.nombre + self.extension
		if tamanodir < 1024:
			tam = '%.3f' % (self.tamano/(1024)) + ' KB.'
		else:
			tam = '%.3f' % (self.tamano/(1024*1024)) + ' MB.'
		#return [vol, ruta, nom, self.fechamod, '', '', tam, '', faudit]
		return [vol, ruta, nom, self.fechamod, '', '', self.tamano, '', faudit]



		
class Directorio(object):
	def __init__(self, path, fechamod, numfiles, numdir, tamano):
		self.path = path
		self.fechamod = fechamod
		self.numfiles = numfiles
		self.numdir = numdir
		self.tamano = tamano
		self.ficheros = []
		self.subdirectorios = []
		
	def imprimir(self):
		print ('\n', '*' * 75)
		print ('\nDir.: ', self.fechamod, self.path, self.numfiles, self.numdir, self.tamano, '\n')
		for file in self.ficheros:
			file.imprimir()
		for dir in self.subdirectorios:
			dir.imprimir()

	def exportarcsv(self, vol, libre, faudit ):
		lib = '%.3f' % (libre/(1024*1024*1024)) + ' GB.'
		if self.tamano < 1024:
			tam = '%.3f' % (self.tamano/(1024)) + ' KB.'
		elif self.tamano < 1024*1024:
			tam = '%.3f' % (self.tamano/(1024*1024)) + ' MB.'
		else:
			tam = '%.3f' % (self.tamano/(1024*1024*1024)) + ' GB.'

		#lista = [[vol, self.path, '', self.fechamod, self.numfiles, self.numdir, tam, lib, faudit]]
		lista = [[vol, self.path, '', self.fechamod, self.numfiles, self.numdir, self.tamano, libre, faudit]]

		for file in self.ficheros:
			lista.append(file.exportarcsv(vol, self.path, faudit, self.tamano))
		
		for dir in self.subdirectorios:
			lista += dir.exportarcsv(vol, 0, faudit)

		return lista


        
class Unidad(object):
	def __init__(self, numserie, volumen, libre, fechaudit):
		self.numserie = numserie
		self.volumen = volumen
		self.libre = libre
		self.fechaudit = fechaudit
		self.directorio = []
	
	def imprimir(self):
		print ('-' * 75)
		print ('\n', self.numserie, self.volumen, self.libre, self.fechaudit, '\n')




if __name__ == "__main__":
	pass
