# -*- coding: utf-8 -*-



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



#cabecera = ('Volumen', 'Directorio', 'Fecha Mod.', 'Ficheros', 'Directorios', 'MB.', 'Libre', 'Fecha')
'''
# código original
class Fichero(object):
    def __init__(self,r,a):
        self.ruta = r
        (self.nombre,self.extension) = os.path.splitext(a)
        self.nombre_completo = os.path.join(r, a)
        e = os.stat(self.nombre_completo)
        self.tamanio = int(round(e.st_size/1024))
        fec = datetime.fromtimestamp(e.st_ctime)
        self.fecha = fec.strftime(formato)
        self.tipo = ''
        if self.extension in tipos:
            self.tipo = tipos[self.extension]
        elif not self.extension in sintipo:
            sintipo.append(self.extension)

class Carpeta(Fichero):
	def __init__(self,r):
		self.ruta = r
		self.nombre = ''
		self.extension = ''
		self.nombre_completo = r
		l =[]
		for (ru,_,a) in os.walk(r):
			for ar in a:
				f = Fichero(ru,ar)
				l.append(f)
			break
		self.ficheros = l
		self.tamanio = self.tamanio_carpeta()
		self.fecha = self.fecha_carpeta()
		self.tipo = self.max_tipo()

	def listar_carpeta(self):
		if len(self.ficheros) != 0:
			print (' Carpeta> ', self.nombre_completo, '    ', self.fecha, '     ', self.tamanio, 'Kb.', '      ', self.tipo)
			for f in self.ficheros:
				print ('   --> ', f.nombre_completo, '    ', f.fecha, '     ', f.tamanio, 'Kb.')

	def contar_tipos_carpeta(self):
		d = {}
		for f in self.ficheros:
			if f.tipo in d:
				d[f.tipo] += 1
			else:
				d[f.tipo] = 1
		return d

	def tamanio_carpeta(self):
		t = 0
		for f in self.ficheros:
			t += f.tamanio
		return t

	def fecha_carpeta(self):
		fec = ''
		for f in self.ficheros:
			if fec < f.fecha:
				fec = f.fecha
		return fec

	def max_tipo(self):
		l = self.contar_tipos_carpeta()
		m = 0
		t = ''
		for k in l:
			if l[k] > m:
				m = l[k]
				t = k
		return t

	def buscar_fichero(self,fich):
		for f in self.ficheros:
			if  f.nombre == fich.nombre and f.extension == fich.extension:
				print ('encontrado: ', fich.nombre + fich.extension, ' en ', f.nombre_completo)
				if f.tamanio == fich.tamanio:
					print ('  tiene el mismo tamanio')
				return True
			else:
				return False


class Directorio(Carpeta):
	def __init__(self,r):
		self.ruta = r
		self.nombre = ''
		self.extension = ''
		self.nombre_completo = r
		self.carpeta = Carpeta(r)
		l =[]
		for (ru,d,_) in os.walk(r):
			for dr in d:
				ds = Directorio(os.path.join(ru, dr))
				l.append(ds)
			break
		self.subdirectorios = l
		self.tamanio = self.tamanio_directorio()
		self.fecha = self.fecha_directorio()
		self.tipo = self.max_tipo()

	def listar_carpeta(self):
		fi = self.carpeta.ficheros
		if len(fi) != 0:
			for f in fi:
				print ('   --> ', f.nombre_completo, '    ', f.fecha, '     ', f.tamanio, 'Kb.')

	def listar_directorio(self):
		print (' Dir> ', self.nombre_completo, '    ', self.fecha, '     ', self.tamanio, 'Kb.', '      ', self.tipo)
		self.listar_carpeta()
		if len(self.subdirectorios) != 0:
			for d in self.subdirectorios:
				d.listar_directorio()

	def tamanio_directorio(self):
		t = self.carpeta.tamanio_carpeta()
		for d in self.subdirectorios:
			t += d.tamanio_directorio()
		return t

	def fecha_directorio(self):
		fec = self.carpeta.fecha_carpeta()
		for d in self.subdirectorios:
			if fec < d.fecha_directorio():
				fec = d.fecha_directorio()
		return fec

	def max_tipo(self):
		return self.carpeta.max_tipo()

	def contar_tipos_carpeta(self):
		return self.carpeta.contar_tipos_carpeta()

	def contar_tipos(self):
		t = self.contar_tipos_carpeta()
		for d in self.subdirectorios:
			t.update(d.contar_tipos_carpeta())
		return t

	def max_tipo(self):
		l = self.contar_tipos()
		m = 0
		t = ''
		if len(l) != 0:
			for k in l:
				if l[k] > m:
					m = l[k]
					t = k
		return t

	def buscar_fichero_subdirectorios(self,fich):
		b = []  # devolverá la lista de ficheros encontrados.
		for sd in self.subdirectorios:
			if sd.carpeta.buscar_fichero(fich):
				b.append(self.carpeta.ruta)
			sd.buscar_fichero_subdirectorios(fich)
		return b

	def buscar_duplicados(self):
		for f in self.carpeta.ficheros:
			print ('buscamos: ', f.nombre_completo)
			print (self.buscar_fichero_subdirectorios(f))
		for sd in self.subdirectorios:
			sd.buscar_duplicados()
'''


if __name__ == "__main__":
	pass
