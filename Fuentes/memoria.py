# -*- coding: utf-8 -*-

	

class Fichero():
	def __init__(self, nombre, extension, tipo, fechamod, tamano, error):
		self.nombre = nombre
		self.extension = extension
		self.tipo = tipo
		self.fechamod = fechamod
		self.tamano = tamano
		self.error = error

	def imprimir(self):
		print ('   - ', self.fechamod, self.nombre, self.extension, self.tipo, self.tamano)
		
	def exportar(self):
		return ['a', self.nombre, self.extension, self.fechamod, self.tamano, self.tipo, self.error]



		
class Directorio():
	def __init__(self, path, fechamod, numfiles, numdir, tamano, error):
		self.path = path
		self.fechamod = fechamod
		self.numfiles = numfiles
		self.numdir = numdir
		self.tamano = tamano
		self.error = error
		self.ficheros = []
		self.subdirectorios = []
		
	def imprimir(self):
		print ('\n', '*' * 75)
		print ('\nDir.: ', self.fechamod, self.path, self.numfiles, self.numdir, self.tamano, '\n')
		for file in self.ficheros:
			file.imprimir()
		for dir in self.subdirectorios:
			dir.imprimir()

	def exportar(self):
		salida = [['d', self.path, self.fechamod, self.numfiles, self.numdir, self.tamano, self.error]]

		for file in self.ficheros:
			salida.append(file.exportar())
		
		for dir in self.subdirectorios:
			salida += dir.exportar()

		return salida


        
class Unidad():
	def __init__(self, numserie, volumen, libre, fechaudit):
		self.numserie = numserie
		self.volumen = volumen
		self.libre = libre
		self.fechaudit = fechaudit
		self.directorio = []
	
	def imprimir(self):
		print ('-' * 75)
		print ('\n', self.numserie, self.volumen, self.libre, self.fechaudit, '\n')
	
	def exportar(self):
		salida = [['u', self.numserie, self.volumen, self.libre, self.fechaudit]]
		salida += self.directorio.exportar()
		return salida




if __name__ == "__main__":
	pass
