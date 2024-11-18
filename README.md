# Proyecto ESPACIO 1.2, analizador de discos (unidades, carpetas, usbs).
========================================================================

El proyecto lee la estructura de archivos y subdirectorios de una ruta data, la graba en memoria (clases Unidad, Directorio y Fichero) y exporta la información	en un informe a .csv.


Componentes actuales del proyecto (05/09/2017):

	__main__.txt	Este fichero informativo
	__main__.py		Script principal
	lectura.py		Módulo encargado de leer los ficheros y directorios
	mapeo.py		Módulo para mapear carácteres inválidos del nombre de un directorio o archivo.
	memoria.py		Módulo que contiene las clases Unidad, Directorio, Fichero.
	grabarcsv.py	Módulo encargado de extracción de la info. y formatearla a fichero .csv

---------------------------------------------------------------------------------------------------

05/09/2017	

    Mejoras a realizar: 

		* Usar el módulo locale para formatear tamaños a 999.999,99.
		* Usar 7z o Zipfile(módulo) para listar y poder leer los archivos que contiene.
		* Exportar a .csv (simple), es decir, unidad, y 2-3 niveles de subdirectorios.
		* Ser capaz de importar la estructura de directorios y archivos del fichero .csv.
		* Analizar la información leída para: buscar ficheros duplicados, etc.

---------------------------------------------------------------------------------------------------

__main__.py		Módulo principal

	Recoge parámetros de la línea de comandos, el directorio a escanear (utilizando el módulo sys).

	Llama al módulo lectura para usar su función leer(ruta).

		- leerunidad(path).- usa el comando OS.POPEN(ins. dos) para ejectuar el DIR del DOS.
		Recupera el volumen y el número de serie de la unidad. Devuelve clase Unidad.

		- leer_dir(path).- usa el comando OS.LISTDIR(ruta) para recuperar los archivos y directorios.
		Con el comando OS.PATH.ISDIR(pathname) identifica directorio y archivo.
		Recupera los archivos y directorios de la ruta pasada en la clase Directorio.path.
	
		- leerfile(path, file).- utiliza OS.PATH.SPLITEXT(fichero) para separar nombre y extensión,
		OS.PATH.JOIN(ruta, archivo) para unir ruta y nombre de archivo y OS.STAT(para recuperar la información del archivo (fechamod, tamaño, etc.)
		Recupera toda la información del fichero pasado.

		- act_directorio(Directorio).- Actualiza la información de num. de archivos, número de directorios y tamaño de cada subdirectorio recursivamente.

	Toda la información de estructura de directorios y archivos es guardada en clases del módulo memoria.py.

	Llama al módulo grabarcsv para usar su función Exportarcsv(unidad), exporta la información a fichero .CSV:
		- Se recupera la información de la memoria en las clases Unidad, Directorio y Ficheros. Para ello usa la funci�n exportar() de Unidad que llama a su Directorio y recursivamente a sus Ficheros y Directorios. Devolviendo una lista con la informaci�n de Unidad, Directorios y Ficheros.

		- formato_csv(lista).- dependiendo del elemento en la lista, formatea Unidades (solo recoge información), Directorios (formatea la información del directorio) y Ficheros (formatea la información de ficheros).
