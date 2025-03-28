#  Importamos librerías para manejar las hojas de google y el drive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#   Definir el límite de acceso, el scope = alcance, acceso a hojas de cálculo y drive
alcance =  ['https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive']

Credenciales = ServiceAccountCredentials.from_json_keyfile_name('Credenciales.json', alcance)
cliente = gspread.authorize(Credenciales)



class FileSheet():
	def __init__(self, hoja, pestaña):
		try:
			#  Intentamos abrir la hoja
			self.hoja = cliente.open(hoja)
		except:
			#  No se ha podido abrir, vamos a crear la hoja
			self.hoja = cliente.create(hoja)
			print(" -> Se crea la hoja de cálculo google Espacio")
			#  Lo comparto con mi usuario
			self.hoja.share('javicu25@gmail.com', perm_type='user', role='writer')

		self.lista_inf = []
		
		try:
			self.pestaña = self.hoja.worksheet(pestaña)
		except:
			#  Si no hemos podido abrirla, no existe, la creamos
			self.pestaña = self.hoja.add_worksheet(pestaña, rows=100, cols=20)
		

	def Leer_Pestaña(self):
		self.lista_inf = self.pestaña.get_all_values()


	def escribir_registro(self, registro):
		self.lista_inf.append(registro)


	def __del__(self):
		del self.lista_inf
