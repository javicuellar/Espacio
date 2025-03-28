###################################################################################################################################
#  Proyecto: ESPACIO, Módulo GeneraExcel - Genera Excel con Unidades, Directorios y Ficheros
#  ==============================================================================================
app = 'Espacio'
#    Modulo Espacio - Versión inicial 0.0
#    ---------------------------------------
version = '0.33'
#       * Generar Excel a partir de la BD SqlLite, usando dataframes. 
###################################################################################################################################
from leerConfig import LeerConfig
from bdSqlite import *
from lectura import *



print("Script GeneraExcel - Versión", version, "  ", datetime.now().strftime("%d/%m/%Y %H:%M"))

tiempo_ini = int(Obtener_hora())

#  Carga de diccionarios de Configuración
config = LeerConfig(app)

if config != {}:
    path = config['Ruta']['ruta'] + app
    os.chdir(path)

    bd = BaseDatos(config['Ruta']['Almacen'])
    unidades = bd.LeerUnidades()
    directorios = bd.LeerDirectorios()
    ficheros = bd.LeerFicheros()

    #  Modificamos los datos de la BD Unidades 
    #   - Añadimos columna Gb. de: total / usado / libre
    #   - Reordenamos las columnas
    #   - Formateamos la fecha
    unidades['Gb'] = unidades['total'].apply(lambda n: n / 1024**3)
    unidades['Gb.'] = unidades['usado'].apply(lambda n: n / 1024**3)
    unidades['Gb..'] = unidades['libre'].apply(lambda n: n / 1024**3)
    unidades = unidades.reindex(columns=['fecha', 'equipo', 'volumen', 'tipo', 'total', 'Gb', 'usado', 'Gb.', 'porcentje', 
                                         'libre', 'Gb..', 'tiempo'])
    unidades['fecha'] = pd.to_datetime(unidades['fecha'], format="%Y-%m-%d %H:%M:%S").dt.strftime('%d-%m-%Y')

    #  Modificamos los datos de la BD Directorios 
    #   - Añadimos columna Gb. de: total / usado / libre
    #   - Reordenamos las columnas
    #   - Formateamos la fecha
    #  Calcular nivel de directorio - núm de veces que tiene '\'
    directorios['Dir'] = directorios['ruta'].apply(lambda n: n.count('\\') + 1)
    #  Reordenar dataframe
    directorios = directorios.reindex(columns=['fecha', 'equipo', 'volumen', 'Dir', 'ruta', 'tamaño', 'fechamod', 'error'])
    #  Formateamos columna fecha como DD-MM-AAAA
    directorios['fecha'] = pd.to_datetime(directorios['fecha'], format="%Y-%m-%d %H:%M:%S").dt.strftime('%d-%m-%Y')

    discos = unidades['volumen'].sort_values()
    try:
        with pd.ExcelWriter(app + '.xlsx', mode='a', if_sheet_exists='replace') as writer:
            unidades.to_excel(writer, sheet_name='Unidades', index=False)
            directorios.to_excel(writer, sheet_name='Directorios', index=False)
            for disco in discos:
                ficheros[ficheros['volumen'] == disco].to_excel(writer, sheet_name='Fic. ' + disco, index=False)
    except:
        with pd.ExcelWriter(app + '.xlsx', mode='w') as writer:
            unidades.to_excel(writer, sheet_name='Unidades', index=False)
            directorios.to_excel(writer, sheet_name='Directorios', index=False)
            for disco in discos:
                ficheros[ficheros['volumen'] == disco].to_excel(writer, sheet_name='Fic. ' + disco, index=False)


seg = int(Obtener_hora() - tiempo_ini)
tiempo = 'Tiempo grabación Excel '+ str(seg // 60) + "'" + str(seg % 60) + '"'
print('\n', tiempo)