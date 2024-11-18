# -*- coding: utf-8 -*-


dicbyte = { b'\x81' : b'u',  b'\xa6' : b'a', b'\xad' : b'!', b'\xcc\x81' : b' ',   # caractéres no válidos
			b'\xc4\x97' : b'e',  # caractéres no válidos
			b'\xa0' : b'\xe1',	# á
			b'\x82' : b'\xe9',	# é
			b'\xa1' : b'\xed',	# í
			b'\xa2' : b'\xf3',	# ó
			b'\xa3' : b'\xfa', 	# ú
			b'\xa4' : b'\xf1' 	# ñ
			}




def leerlinea(file):
	linea, byte = '', b' '
	byte = file.read(1)
	while byte != b'' and byte != b'\r':
		if byte in dicbyte:
			# caracter transformado que da error o es invalido
			byte = dicbyte[byte]
		linea += byte.decode(u'cp1252')
		byte = file.read(1)
	#print (' > ', linea)
	return linea



def mapeo_string(palabra):
	cambio = False
	salida = ''
	for caracter in palabra:
		byte = caracter.encode('utf-8')
		if byte in dicbyte:
			# caracter transformado que da error o es invalido
			# print (byte, '>', dicbyte[byte])
			byte = dicbyte[byte]
			cambio = True
		#print (byte, '>')
		salida += byte.decode('utf-8')
	
	if cambio:
		salida += ' (cambiado)'

	return salida




if __name__ == "__main__":
	acento = u"\u0301"  # tilde
	e = u'\u0117' 		# ė
	
	texto = 'España á,é,í,ó,ú Yagüe ' + acento + 'a' + e

	mapeo_string(texto)
