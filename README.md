# Proyecto ESPACIO 6.03, analizador de discos (unidades, carpetas, usbs).


Ver gestión del proyecto en Trello - https://trello.com/b/qnpWcxMA/espacio

  
El proyecto pretende leer los archivos y subdirectorios de una ruta data, y posteriormente realizar un reporte (en .csv) para su análisis.


   Historial
   ---------

    **27 de marzo 2023**

    - Al realizar la lectura de las unidades, comparar mediante dataframe con la información en BD, la información anterior.


    **22 de marzo 2023**

     - Se añade hoja google Espacio para parametrizar funciones, tipos de ficheros (extensión). Se carga en funciones.py
     - Se modifica el proceso de análisis de dispositivo para que en linux no analice (lea) las unidades. Debido a que la capacidad de proceso del NAS está muy limitada, y que además de las unidades que pone a disposición, tiene un número de ficheros y directorios excesivo.
     - En windows, se realizan dos tipos de análisis: si se tiene permiso de administrador se leen las particiones del dispositivo, y si no, se leen las unidades del NAS conectadas a windows.


    **18 de marzo 2023**

     - Usando función Información Discos vista en funciones.py, cambiar:
      * recorrer unidades usando función
      * recopilar información de unidades: ruta, tipo unidad e inf. capacidad disco: total, usado, libre, porcentaje
      * hacemos clave de directorio y ficheros el volumen, debido a que linux no tiene número de serie.
      * en linux cogemos equipo como volumen.
    
     - Creación de la versión base. Versión 0. Con versiones previas en Backup.
     - Limpiar versión base, eliminamos componentes obsoletos.
