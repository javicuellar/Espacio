# Proyecto ESPACIO 2.0, analizador de discos (unidades, carpetas, usbs).


El proyecto pretende leer los archivos y subdirectorios de una ruta data, y posteriormente realizar un reporte (en .csv) para su análisis.


### Componentes actuales del proyecto (31/08/2017):

__main__.py		Script principal
leerbyte.py		Módulo encargado de leer fichero de DIR byte a byte y transformarlo a unicode
analisisdir.py	Módulo encargado de leer un DIR de DOS y extraer los ficheros y directorios
memoria.py		Módulo con las clases Unidad, Directorios y Ficheros

---------------------------------------------------------------------------------------------------

31/08/2017	Se estructura código para tener un módulo principal y módulos de servicio.

Tiempo prueba: 

* lectura unidad d:\ portátil trabajo --> 0.174 segundos.


---------------------------------------------------------------------------------------------------


__main__.py		Módulo principal

	Obtenie la ruta a analizar introducida como parámetro en la llamada al módulo principal (sys). Si no est� informada devuelve mensaje informativo y termina el script.

   	- captura_dir(path).- usa el comando OS.POPEN(inst. dos) para ejectuar el DIR del DOS.

	- mapeo(filein, fileout).- mapea el fichero filein a unicode, eliminando caracteres no válidos y transformando las tildes, ñ, etc.
			Utiliza módulo: leerbyte.py

	- analizar(fleout).- Lee el fichero que contiene la salida del DIR mapeada correctamente y extrae la información de la Unidad, Directorio principal, subdirectorios y ficheros.
			Utiliza módulo: analisisdir.py

	El resultado lo va almacenando en memoria, en la clase Unidad que contiene la clase Directorio.	La clase Directorio es la que contiene una lista con clases ficheros y una lista con clases subdirectorios.
			Utiliza módulo: memoria.py

	- imprimir.- Usa el mótodo imprimir de la clase Unidad y de la clase Directorios para imprimir en pantalla la información extraida del DIR.
