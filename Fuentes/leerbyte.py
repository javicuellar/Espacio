# -*- coding: utf-8 -*-

dicbyte = { b'\x81' : b'u',	 b'\xa6' : b'a', b'\xad' : b'!', 	# caractéres no válidos
			b'\xa0' : b'\xe1',	# á
			b'\x82' : b'\xe9',	# é
			b'\xa1' : b'\xed',	# í
			b'\xa2' : b'\xf3',	# ó
			b'\xa3' : b'\xfa', 	# ú
			b'\xa4' : b'\xf1' 	# ñ
			}


def mapeo(f_in, f_out):
	byte = b''
	
	with open(f_in, 'rb') as f:
		byte = f.read(1)
		
		with open(f_out, 'wb') as fs:
		
			while byte != b'':
				if byte in dicbyte:
					# caracter no transformado que da error
					byte = dicbyte[byte]
				
				'''
				# Para depurar errores en lectura
				if byte == b'\xa0':
					s = byte.decode(u'cp1252')
					print (s, ' á ', byte, ':', s.encode("cp1252") )
					s = u'á'
					print (s, ' á ', byte, ':', s.encode("cp1252") )
				'''
				
				fs.write(byte)
				byte = f.read(1)
				
	print ('fin mapeo.')
				
	

dic = {u"£": u'ú', u'¤': u'ñ', u'¢': u'ó', u'¡': u'í', u'‚': u'é' }

def mapeo2(f_in, f_out):
	with open(f_in, 'rb') as f:
		byte = f.read(1)
		while byte != b'':
			linea = u''
			while byte != b'\r':
				if byte == b'\x81':
					# caracter no transformado que da error
					byte = b'u'
				if byte == b'\xa6':
					# caracter no transformado que da error
					byte = b'a'

				s = byte.decode(u'cp1252')
				if s in dic:
					s = dic[s]			
				linea += s
				byte = f.read(1)
			print (linea)
			byte = f.read(1)