#  Lectura de dispositivo: unidades, directorios y ficheros
#  ========================================================
from threading import Thread
from smb.SMBConnection import SMBConnection
import platform, psutil, os


# Módulos del proyecto
from funciones import *
from bdSqlite import *
from analisis import *



# -------------------------------------------------------------------------------------------------------------------------
#  Información del SISTEMA sobre el que se está ejecutando -> nombre, sistema, so, maquina, arquitectura, procesador, fecha
class Dispositivo():
	def __init__(self, config):
		self.config = config
		self.equipo = getattr(platform, 'node')()
		self.sistema = getattr(platform, 'system')()
		self.so = getattr(platform, 'platform')()
		self.maquina = getattr(platform, 'machine')()
		self.arquitectura = getattr(platform, 'architecture')()[0]
		self.procesador = getattr(platform, 'processor')()
		self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.bd = BaseDatos(config['Ruta']['Almacen'])
		
		if self.bd.ExisteDispositivo(self.equipo):
			self.bd.ActualizarDispositivo(self.equipo, self.fecha)
		else:
			self.bd.GrabarDispositivo(self.ExportarDispositivo())
		
		if self.sistema == 'Windows':
			self.Leer_Particiones()
		else:
			self.Grabar_Unidades()

	
	def ExportarDispositivo(self):
		return [[self.fecha, self.equipo, self.sistema, self.so, self.maquina, self.arquitectura, self.procesador]]


	def Leer_Particiones(self):
		self.unidades = []
		self.directorios = []
		self.ficheros = []

		hilos = []
		particiones = psutil.disk_partitions()
		for partición in particiones:
			ruta = partición.mountpoint
			hilo = Thread(target=self.Leer_Unidad, args=(ruta, partición.fstype, ))
			hilo.start()
			hilos.append(hilo)

		#    - Plantear lectura unitaria - Directorio raiz o lectura en hilos de cada directorio ("chocan")
		#	 - si se hace en hilos, devolver salida directorios y luego juntarlos
		if self.equipo == self.config['Ruta']['NAS']:
			smb = 'SMB'
			servidor = self.config['Servidor']['servidor']
			usuario  = self.config[smb]['usuario']
			password = self.config[smb]['password']
			equipo = 'NAS'
			tiempo_ini = Obtener_hora()
			print("> Analizando unidad: ", equipo)
			try:
				self.conn = SMBConnection(usuario, password, equipo, servidor)
				self.conn.connect(servidor)
			except:
				print('Error - No es posible conectarse al Servidor', equipo)
				return
			
			tipo = 'BTRFS'
			total = 0
			usado = 0
			porcentaje = 0
			libre = 0
			
			directorios = []
			try:	
				directorios = self.conn.listShares()
			except Exception as e:
				print('Error - No es posible obtener las carpetas compartidas del Servidor', equipo)
				print('  > Error: ', e)
				# return

			for directorio in directorios:
				if not directorio.isSpecial:
					self.Leer_DirectorioSMB(equipo, directorio.name, '/')
			
			seg = int(Obtener_hora() - tiempo_ini)
			tiempo = 'Tiempo lectura ' + equipo + '  ' + str(seg // 60) + "'" + str(seg % 60) + '"'
			print ('\n', tiempo)
			self.unidades.append([self.fecha, equipo, equipo, tipo, total, usado, porcentaje, libre, tiempo])

		for i in hilos:
			i.join()

		self.Grabar_Unidades()



	#   Información de la UNIDAD -> equipo, volumen, tipo, total, usado, porcentaje, libre, fecha
	def Leer_Unidad(self, ruta, tipo):
		tiempo_ini = Obtener_hora()
		try:
			disco = psutil.disk_usage(ruta)
		except Exception as error:
			print("> error cálculo uso disco en unidad: ", ruta, " - ", error)
			return
		
		total = disco.total
		usado = disco.used
		porcentaje = disco.percent
		libre = disco.free

		f = os.popen('dir ' + ruta)
		volumen = f.readline()[30:-1].upper()
		f.close()
		
		print("> Analizando unidad: ", volumen)
		self.Leer_Directorio(ruta, volumen)
		
		seg = int(Obtener_hora() - tiempo_ini)
		tiempo = 'Tiempo lectura ' + ruta + '  ' + str(seg // 60) + "'" + str(seg % 60) + '"'
		print ('\n', tiempo)
		self.unidades.append([self.fecha, self.equipo, volumen, tipo, total, usado, porcentaje, libre, tiempo])



	#   Información del DIRECTORIO
	def Leer_Directorio(self, ruta, volumen, error=''):
		elementos = []
		try:
			elementos = os.listdir(ruta)
		except PermissionError:
			# print('> dir: ', ruta, ' Acceso denegado1')
			error = 'Acceso Denegado1'
		except Exception as error:
			print('> dir: ', ruta, ' Error: ', error)
		
		tamaño = 0
		fechamod = datetime(1,1,1)
		numdir = 1
		numfich = 0
		for elemento in elementos:
			path = os.path.join(ruta, elemento)
			
			try:
				evalua = os.path.isdir(path)
			except PermissionError:
				print ('> elemento: ', path, ' Acceso denegado2')
				error = 'Acceso Denegado2'
				self.directorios.append([self.fecha, self.equipo, volumen, path[3:], numdir, numfich, error])
			except Exception as error:
				print ('> elemento: ', ruta, " -> ", elemento, " Error: ", error)
			else:
				if evalua:
					tamañoN, numfichN, numdirN, fechamodN = self.Leer_Directorio(path, volumen)
					tamaño += tamañoN
					numdir += numdirN
					numfich += numfichN
					if fechamodN.strftime("%Y-%m-%d %H:%M:%S") > fechamod.strftime("%Y-%m-%d %H:%M:%S"):
						fechamod = fechamodN
				else:
					numfich += 1
					tamfichero, fechamodfichero = self.Leer_Fichero(ruta, elemento, volumen)
					tamaño += tamfichero
					if fechamodfichero == '0000-00-00':
						fechamodficherostr =  datetime(1,1,1).strftime("%Y-%m-%d %H:%M:%S")
					else:
						fechamodficherostr =  fechamodfichero.strftime("%Y-%m-%d %H:%M:%S")
					if fechamodficherostr > fechamod.strftime("%Y-%m-%d %H:%M:%S"):
						fechamod = fechamodfichero
		
		self.directorios.append([self.fecha, self.equipo, volumen, ruta[3:], tamaño, fechamod, numdir, numfich, error])
		return tamaño, numfich, numdir, fechamod



#   Información del DIRECTORIO en el Servidor vía SMB
	def Leer_DirectorioSMB(self, volumen, directorio, ruta, error=''):
		try:
			elementos = self.conn.listPath(directorio, ruta)
		except:
			error = 'Recurso no accesible'
			elementos = []

		path = os.path.normpath(directorio + ruta)
		tamaño = 0
		fechamod = datetime(1,1,1)
		numdir = 1
		numfich = 0
		for elemento in elementos:
			if elemento.isDirectory:
				if elemento.filename not in ['.', '..']:
					tamañoN, numdirN, numfichN, fechamodN = self.Leer_DirectorioSMB(volumen, directorio, os.path.join(ruta, elemento.filename))
					tamaño += tamañoN
					numdir += numdirN
					numfich += numfichN
					if fechamodN.strftime("%Y-%m-%d %H:%M:%S") > fechamod.strftime("%Y-%m-%d %H:%M:%S"):
						fechamod = fechamodN
			else:
				numfich += 1
				nombre, extension = os.path.splitext(elemento.filename)
				tamañofich = elemento.file_size
				fechamodfichero = datetime.fromtimestamp(elemento.last_write_time)
				fechamodfichero = datetime(fechamodfichero.year, fechamodfichero.month, fechamodfichero.day, 
			       						   fechamodfichero.hour, fechamodfichero.minute, fechamodfichero.second)
				
				error = ''
				if extension.lower() in self.config['Tipos']:
					tipo = self.config['Tipos'][extension.lower()]
				else:
					tipo = ''
				tamaño += tamañofich
				if fechamodfichero.strftime("%Y-%m-%d %H:%M:%S") > fechamod.strftime("%Y-%m-%d %H:%M:%S"):
					fechamod = fechamodfichero
				self.ficheros.append([self.fecha, self.equipo, volumen, path, nombre, extension, tipo, fechamodfichero, tamañofich, error])

		self.directorios.append([self.fecha, self.equipo, volumen, path, tamaño, fechamod, numdir, numfich, error])
		return tamaño, numdir, numfich, fechamod



	#  Información del FICHERO -> volumen, ruta, nombre, extension, tipo, fechamod, tamaño, error, fecha
	def Leer_Fichero(self, ruta, fichero, volumen, error=''):
		nombre, extension = os.path.splitext(fichero)
		fechamod = datetime(1,1,1)
		tamaño = 0
		if extension.lower() in self.config['Tipos']:
			tipo = self.config['Tipos'][extension.lower()]
		else:
			tipo = ''
		
		if error == '':
			try:
				info_fichero = os.stat(os.path.join(ruta, fichero))
			except PermissionError:
				print ('> fichero: ', os.path.join(ruta, fichero), ' Acceso denegado3')
				error = 'Acceso Denegado3'
			except FileNotFoundError:
				# > ACCESO DIRECTO.- es un fichero que está en el directorio pero no permite acceder.
				# print ('> fichero: ', os.path.join(ruta, fichero), ' Fichero no encontrado')
				error = 'Acceso directo'
			except Exception as error_excepcion:
				#print ('> fichero: ', os.path.join(ruta, fichero), ' Error:', str(error_excepcion)[:26])
				if str(error_excepcion)[:26] == ' [Errno 40] Too many levels':
					error = '[Errno 40] Too many levels'
				else:
					error = 'error desconocido'
			else:
				tamaño = info_fichero.st_size
				fechamod = datetime.fromtimestamp(info_fichero.st_mtime)  	# , tz=timezone.utc)
				fechamod = datetime(fechamod.year, fechamod.month, fechamod.day, fechamod.hour, fechamod.minute, fechamod.second)
				error = ''
			finally:
				self.ficheros.append([self.fecha, self.equipo, volumen, ruta[3:], nombre, extension, tipo, fechamod, tamaño, error])
				return tamaño, fechamod
		else:
			print(">--> llegan errores: ", error, " nombre y extesion: ", nombre, extension)
			self.ficheros.append([self.fecha, self.equipo, volumen, ruta[3:], nombre, extension, tipo, fechamod, tamaño, error])
			return tamaño, fechamod


	
	def Grabar_Unidades(self):
		tiempo_ini = Obtener_hora()
		volumenAnt = dict()
		for unidad in self.unidades:
			volumen = unidad[2]
			#if self.bd.ExisteUnidad(volumen):
				#dfAnt = list()
				#dfAnt.append(self.bd.LeerUnidad(volumen))
				#dfAnt.append(self.bd.LeerDirectoriosUnidad(volumen))
				#dfAnt.append(self.bd.LeerFicherosUnidad(volumen))
				#volumenAnt[volumen] = dfAnt
			self.bd.EliminarUnidad(volumen)
			self.bd.EliminarDirectorios(volumen)
			self.bd.EliminarFicheros(volumen)
		
		self.bd.GrabarUnidades(self.unidades)
		self.bd.GrabarDirectorios(self.directorios)
		self.bd.GrabarFicheros(self.ficheros)

		#for volumen in volumenAnt.keys():
		#	dfUnidadNuevo = self.bd.LeerUnidad(volumen)
		#	dfDirectoriosNuevo = self.bd.LeerDirectoriosUnidad(volumen)
		#	dfFicherosNuevo = self.bd.LeerFicherosUnidad(volumen)
		#	self.bd.Grabar_cambios(AnalizarCambiosUnidad(volumenAnt[volumen][0], dfUnidadNuevo), 'CambiosUnidades')
		#	self.bd.Grabar_cambios(AnalizarCambiosDirectorios(volumenAnt[volumen][1], dfDirectoriosNuevo), 'CambiosDirectorios')
		#	self.bd.Grabar_cambios(AnalizarCambiosFicheros(volumenAnt[volumen][2], dfFicherosNuevo), 'CambiosFicheros')

		seg = int(Obtener_hora() - tiempo_ini)
		tiempo = 'Tiempo Grabar BBDD SqLite ' + str(seg // 60) + "'" + str(seg % 60) + '"'
		print ('\n', tiempo)



	#  Función para la actualización del excel con los datos de dispositivos
	def Actualizar_Excel(self):
		tiempo_ini = int(Obtener_hora())
		GrabarExcel(self.config['App']['App'], self.bd.LeerUnidades(), self.bd.LeerDirectorios(), self.bd.LeerFicheros())
		seg = int(Obtener_hora() - tiempo_ini)
		tiempo = 'Tiempo grabación Excel '+ str(seg // 60) + "'" + str(seg % 60) + '"'
		print('\n', tiempo)



	def __del__(self):
		try:
			del self.unidades
			del self.directorios
			del self.ficheros
		except:
			pass
		del self.bd





if __name__ == "__main__":
	#  Pruebas módulo
	print("\n")
	disp = Dispositivo()
	
	# Borramos la variables
	del disp
