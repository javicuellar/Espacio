# Proyecto ESPACIO 1.0, analizador de discos (unidades, carpetas, usbs).
======================================================================


	El proyecto pretende leer los archivos y subdirectorios de una ruta data, grabarlos en base de datos SQLite y posteriormente realizar un reporte (en .csv) y su análisis.



Componentes actuales del proyecto (31/08/2017):

	__main__.py	Script principal
	lectura.py	Módulo encargado de leer los ficheros y directorios
	grabacion.py	Módulo encargado de grabar la información en SQLite y recuperarla
	analisis.py	Módulo encargado de la extracción de la info. a fichero .csv


---------------------------------------------------------------------------------------------------

31/08/2017	Se incorpora al módulo principal la toma de tiempos de ejecución (solo de la obtención
		de la información y almacenamiento en BD SQLite).

    Tiempo prueba: 

		* lectura unidad d:\ portátil trabajo --> 44.485 segundos.
		* lectura BD SQLite y exportar a .CSV -->  0.006 segundos.  (SOLO unidades y directorios, 61 reg.)


---------------------------------------------------------------------------------------------------

__main__.py		Módulo principal

	Crea clase tablas = BaseDatos() del módulo grabacion.py.
	Recoge parámetros de la línea de comandos, el directorio a escanear (utilizando el módulo sys).

	Dependiendo de si viene o no informado el parámetro de entrada:
	   Si viene informado, leemos la unidad, directorios y ficheros utilizando las funciones:
		- leerunidad(path).- usa el comando OS.POPEN(ins. dos) para ejectuar el DIR del DOS.

		Recupera el volumen y el número de serie de la unidad.
		- leerdir(path).- usa el comando OS.LISTDIR(ruta) para recuperar los archivos y directorios.

		Con el comando OS.STAT(pathname) identifica directorio y archivo.
		Recupera los archivos y directorios de la ruta pasada.


		- leerfile(path, file, numserie).- utiliza OS.PATH.SPLITEXT(fichero) para separar nombre y extensión,
		OS.PATH.JOIN(ruta, archivo) para unir ruta y nombre de archivo y OS.STAT(para recuperar la información del archivo (fechamod, tamaño, etc.)

		Recupera toda la información del fichero pasado.

		- Grabación de la información en SQLite: tablas unidades, directorios, ficheros (claves: numserie y path).
		La información recuperada de unidad, directorio y fichero se unifica para que contenga la misma info.

		y se puede grabar, y posteriormente exportar a fichero .CSV, de manera homogenea.

	   Si no viene informado, se exporta la información a fichero .CSV:
		- Se recupera la información de unidades de SQLite, tablas.Leerunidades(), devolviendo una lista.
		- Para cada unidad de la lista recuperada, se recupera la información de sus directorios, tablas.Leerdirectorios(unidad[0]), devolviendo una lista con los directorios.


		- Por último se usa el módulo analis.py para formatear los registros y exportarlos a .CSV.
		Se llama a la función FormatoUnidaddes(unidades) y FormatoDirectorios(directorios, dicnumserie) para
		formatear registro a .CSV (se formatean las unidades y directorios con el mismo formato).


Se utiliza la función Exportarcsv(lista) para generar el fichero .CSV, lista contiene tanto las unidades como los directorios, en el mismo formato.
