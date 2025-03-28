import pandas as pd
from cryptography.fernet import Fernet
import os



#  Función de encriptado
def Clave():
    return Fernet(b'yTuch5OUKymW9A343oBlHHRSPWF-w5RHqXSVxLKOuwI=')

#  Función de encriptado
def Encriptar(texto):
    #cifrado = Clave()
    return Clave().encrypt(str.encode(texto))

#  Función de Desencriptado
def DesEncriptar(texto):
    #cifrado = Fernet(b'yTuch5OUKymW9A343oBlHHRSPWF-w5RHqXSVxLKOuwI=')
    #texto_bytes = str.encode(texto)
    #print(texto_bytes, type(texto_bytes))
    return Clave().decrypt(str.encode(texto)).decode()



#  Función para lectura de fichero CSV de configuración y devolver diccionario
def LeerConfig(app):
    config = dict()

    try:
        df = pd.read_csv('.\\' + app + '.csv', sep=';')
    except:
        try:
            df = pd.read_csv('.\\' + app + '\\' + app + 'Pruebas.csv', sep=';')
        except:
            try:
                df = pd.read_csv('.\\' + app + 'Pruebas.csv', sep=';')
            except:
                print('Se ha producido un error al no encontrar el fichero de configuración. Directorio ', os.getcwd())
                return config

    for i in range(len(df)):
        fila = df.iloc[i]
        if not fila[0] in config.keys():
            config[fila[0]] = dict()

        if fila[1] in ['servidor', 'usuario', 'password']:
            # print(fila[1], fila[2], Encriptar(fila[2]))
            fila[2] = DesEncriptar(fila[2])

        config[fila[0]] [fila[1]] = fila[2]

    del df
    
    return config




if __name__ == "__main__":
	#  Pruebas módulo
    print("Script leerConfig - Pruebas")

    LeerConfig('Espacio')