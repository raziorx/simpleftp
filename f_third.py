 #!/usr/bin/python3
import socket
import sys
import os
import time

class cliente:
	@staticmethod

	def __init__(FTP):
		FTP.handle = handler()
		FTP.buffer_size = 1024
		FTP.sock_pasv = False

	def connect(FTP):
		FTP.sock_main = mk_socket(1, '192.100.230.21')
		FTP.sock_main.recv()

	def think(FTP, thought):
		print("!!!", str(thought) + '\n')

	def do_nothing(FTP):
		FTP.sock_main.relay('NOOP')

	def error(FTP, err, msg):
		raise err

	def LOGIN(FTP, usern, passw):
		FTP.sock_main.relay('USER ' + usern)
		res = self.sock.main.relay('PASS ' + passw, filt = passw)

		if FTP.handle.get_id(res) != 230:
			FTP.error(UNEXPECTED_RESPONSE, 'Nombre de usuario o contrasena incorrectos')

	def DIR(FTP):
		FTP.PASV()
		msg = FTP.sock_main.relay('NLST')

		if FTP.handle.validify_case(msg):
			msg = ''
			add = True

			while add != '':
				add = FTP.sock_pasv.recv()
				msg += add
			FTP.think('Mensaje enviado. Listado terminado.')
			FTP.sock_pasv.cls()

			ftlist = FTP.handle.parse_nlst(msg)
			FTP.think(ftlist)
			FTP.sock.main.recv(226)

		else:
			FTP.sock_pasv.cls()
			ftlist = []
		return ftlist

	def SIZE(FTP, f):
		msg = FTP.sock_main.relay('SIZE ' + f)

		if FTP.handle.validity_case(msg):
			fsize = FTP.handle.parse_size(msg)

		else:
			fsize = False
		return fsize

	def CDUP(FTP):
		FTP.sock_main.relay('CDUP')

	def MODE(FTP, m = 'S'):
		FTP.sock_main.relay('MODE ' + m)

	def TYPE(FTP, t = 'A'):
		FTP.sock_main.relay('TYPE ' + t)

	def STRU(FTP, s = 'F'):
		FTP.sock_ain.relay('STRY ' + s)

	def CWD(FTP, dname):
		FTP.sock_main.relay('CWD ' + dname, 250)

	def MKD(FTP, dname):
		FTP.sock_main.relay('MKD ' + dname, 257)

	def PASV(FTP):
		if FTP.sock_pasv:
			FTP.think('Buscando sockets abiertos...')
			assert not FTP.sock_pasv.open

		msg = FTP.sock_main.relay('PASV')
		nIP, nPORT = FTP.handle.parse_pasv(msg)

		FTP.sock_pasv = mk_socket(2, nIP, nPORT)

	def QUIT(FTP):
		if FTP.sock_pasv:

			if FTP.sock_pasv.open:
				FTP.think('Puerto pasivo abierto. Cerrando...')
				FTP.sock_pasv.cls()

			else:
				FTP.think('Puerto cerrado previamente.')

		FTP.sock_main.relay('QUIT')
		FTP.sock_main.cls()

	def upload(FTP, fname, fsource):
		FTP.pasv()
		FTP.sock_main.relay('STOR ' + fname)

		xfile = open_slow(fsource)

		while xfile.opened:
			FTP.sock_pasv.send(xfile.next(FTP.buffer_size), False)

		FTP.sock_pasv.cls()
		FTP.sock_main.recv(226)

	def upload_init(FTP, fname, fsource):
		FTP.PASV()
		FTP.sock_main.relay('STOR ' + fname)
		xfile = open_slow(fsource)
		return xfile

	def upload_send(FTP, xfile, buff):
		FTP.sock_pasv.send(xfile.next(buff), False)
		return xfile.opened

	def upload_abort(FTP):
		FTP.sock_main.send('ABOR')
		FTP.sock_pasv.cls()
		FTP.sock_main.recv(226)

	def upload_close(FTP):
		FTP.sock_pasv.cls()
		FTP.sock_main.recv(226)

#inicio de main 
if __name__ == '__main__':
 	client1 = cliente();

	try:
		client1.LOGIN('userftp', 'r3d3sf1s1c@s')

	except UNEXPECTED_RESPONSE:
		print("Error al iniciar sesion.")
		sys.exit(1)

	client1.MODE()
	client1.TYPE('I')
	client1.STRU()
	client1.CWD('/')
	client1.MKD('prueba')
	client1.CWD('prueba')

	dest = 'archivo_prueba.py'
	client1.upload(dest, sys.argv[0])

	diir = client1.DIR()
	fsize = client1.SIZE(dest)
	client1.QUIT()

	if dest in diir:
		print("Realizado. '%s' cargado al directorio. (%s Bytes)\n", dest, fsize)

	else:
		print("El archivo no pudo ser cargado al directorio.")
