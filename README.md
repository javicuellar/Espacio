# Proyecto ESPACIO 3.0, analizador de discos (unidades, carpetas, usbs).


El proyecto pretende leer los archivos y subdirectorios de una ruta data, y posteriormente realizar un reporte (en .csv) para su análisis.



### Componentes actuales del proyecto (09/06/2022):

	Leeme.txt		Fichero informativo con las versiones del proyecto.
	__main__.py		Script principal
	lectura.py		Módulo encargado de leer los ficheros y directorios
	mapeo.py		Módulo para mapear carácteres inválidos del nombre de un directorio o archivo.
	discos.py		Módulo de mantenimiento de Discos/Unidades/Directorios/Ficheros
	ficherocsv.py	Módulo encargado de extracción de la info. y formatearla a fichero .csv

---------------------------------------------------------------------------------------------------

### Mejoras a realizar:    (05/09/2017)


02/10/2017  OK  1) Exportar info de directorio con nivel de subdirectorio como par�metro.

05/09/2017  OK	1) Ser capaz de importar la estructura de directorios y archivos del fichero .csv.
		2) Actualizar la información de una unidad (leida de .csv) con la info actual.
		3) Exportar a .csv (simple), es decir, unidad, y 2-3 niveles de subdirectorios.

	* Usar 7z o Zipfile(módulo) para listar y poder leer los archivos que contiene.
	* Analizar la información leída para: buscar ficheros duplicados, etc.

---------------------------------------------------------------------------------------------------


08/09/2017	- Renombramos módulo grabarcsv a ficherocsv, sacamos las funcionalidades de las clases
		de Unidades, directorios y Ficheros.

		- Ampliada la función de leer CSV para leer varias unidades.
		- Incluido un menú en __main__ para realizar las operaciones de lectura, exportar, etc.
		- Incluido submenú para Exportar, se puede exportar Unidades, Directorios ppales. o todo.


---------------------------------------------------------------------------------------------------


07/09/2017	- Desarrollada función para leer la estructura de directorios de un fichero .CSV y
		grabarla en memoria en clases Unidad, Directorios, Ficheros.
		- Renombramos módulo memoria a discos, juntamos en él todas las funcionalidades de
		las unidades, en la nueva clase Discos.


---------------------------------------------------------------------------------------------------


__main__.py		M�dulo principal
	
	Recoge parámetros de la línea de comandos, el directorio a escanear (utilizando el módulo sys).

	Llama al módulo lectura para usar su función leer(ruta).

		- leerunidad(path).- usa el comando OS.POPEN(ins. dos) para ejectuar el DIR del DOS.

		Recupera el volumen y el número de serie de la unidad. Devuelve clase Unidad.

		- leer_dir(path).- usa el comando OS.LISTDIR(ruta) para recuperar los archivos y directorios.

		Con el comando OS.PATH.ISDIR(pathname) identifica directorio y archivo
.
		Recupera los archivos y directorios de la ruta pasada en la clase Directorio.path.
		
		- leerfile(path, file).- utiliza OS.PATH.SPLITEXT(fichero) para separar nombre y extensión,

		OS.PATH.JOIN(ruta, archivo) para unir ruta y nombre de archivo y OS.STAT(para recuperar la información del archivo (fechamod, tamaño, etc.)

		Recupera toda la información del fichero pasado.

		- act_directorio(Directorio).- Actualiza la información de num. de archivos, número de directorios y tamaño de cada subdirectorio recursivamente.


	Toda la información de estructura de directorios y archivos es guardada en clases del módulo memoria.py.



	Llama al módulo grabarcsv para usar su función Exportarcsv(unidad), exporta la información a fichero .CSV:

		- Se recupera la información de la memoria en las clases Unidad, Directorio y Ficheros. Para ello usa la función exportar() de Unidad que llama a su Directorio y recursivamente a sus Ficheros y Directorios. Devolviendo una lista con la información de Unidad, Directorios y Ficheros.


		- formato_csv(lista).- dependiendo del elemento en la lista, formatea Unidades (solo recoge información), Directorios (formatea la informaci�n del directorio) y Ficheros (formatea la información de ficheros).

		- leer_csv.- lee el fichero .CSV y va guarda en memoria su estructura de Directorios y Ficheros.

