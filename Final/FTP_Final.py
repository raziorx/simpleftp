import socket
import sys
import os
import time
from os import walk
s = socket.socket()
def send(mes=''):
	s.send(bytes(mes + ("\r\n"), "UTF-8"))
def recieve():
	rec = s.recv(1024)
	    
def action(mes=''):
	send(mes)
	return recieve()
def local_dir(path=''):
	for (dirpath, dirnames, filenames) in walk(path):
		print ('"'+dirpath+'"')
		break
def browse_local(path=''):
	for (dirpath, dirnames, filenames) in walk(path):
		print (dirnames)
		print (filenames)
		print ('\n')
		break
def pasv():
	while True:
		vali = ''
		mes = ('PASV')
		send(mes)
		mes = (s.recv(1024))
		mes = mes.decode()
		nmsg = mes.split('(')
		nmsg = nmsg[-1].split(')')
		p = nmsg[0].split(',')
		newip = '.'.join(p[:4])
		newport = int(p[4])*256 + int(p[5])
		return (newip,newport)
		break
		
def sendfile(file=''):
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	send('STOR '+file)
	f = open(file, 'rb')
	size = os.stat(file)[6]
	opened = True
	pos = 0
	buff = 1024
	packs = size/1024
	timeb = 100/packs
	i=0
	print (packs)
	while opened:
		i=i+timeb
		time.sleep(.5)
		sys.stdout.write("\r%d%%" %i)
		sys.stdout.flush()
		f.seek(pos)
		pos += buff
		if pos >= size:
			piece = f.read(-1)
			opened = False
		else:
			piece = f.read(buff) 
		p.send(piece)
		sys.stdout.write("\r%d%%" %i)
		sys.stdout.flush()
		f.seek(pos)
	f.close()
	recieve()
	mes = ('ABOR')
	send(mes)
	p.close
	
	
		
	
def listar():
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	mes = ('NLST')
	action (mes)
	rec = p.recv(1024)
	rec = rec.decode()
	rec.split('\r\n')
	print (rec)
	mes = ('ABOR')
	p.send(bytes(mes + ("\r\n"), "UTF-8"))
	p.close
	recieve()
#s.connect((input("Enter FTP Address: "), 21))
s.connect(("192.100.230.21", 21))
s.recv(1024)		
		
#usern = input("Enter user: ")
#action('USER '+usern)
action('USER '+'userftp')
#passw = input("Enter password: ")
#action('PASS '+passw)
action('PASS '+'r3d3sf1s1c@s')
path = ('/home/ec2-user/proyecto/')
buff=1024
while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print ('*-------------------------------*') 
	print ('*\t\tMenu\t\t*') 
	print ('*1 - Enviar archivos\t\t*') 
	print ('*2 - Recibir archivos\t\t*') 
	print ('*3 - Cambiar directorio local\t*')
	print ('*4 - Cambiar directorio Remoto\t*')
	print ('*5 - Imprimir directorio\t*') 
	print ('*6 - Modificar permisos\t\t*')
	print ('*7 - Salir\t\t\t*')
	print ('*-------------------------------*') 
	opc = input('Seleccione una opcion: ')
	if opc == '1':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('Seleccione el Tipo de archivo que deseas subir')
			print ('1 - Archivos de Texto')
			print ('2 - Imagenes')
			print ('3 - Return')
			opc2 = input('Seleccione una opcion: ')
			if opc2 == '1':
				os.path = path
				print(path)
				file = input('File Name: ')
				mes = ('TYPE A')
				action(mes)
				sendfile(file)
				print(input('Hit Return'))
			if opc2 == '2':
				os.path = path
				file = input('File Name: ')
				mes = ('TYPE I')
				action(mes)
				sendfile(file)
				print(input('Hit Return'))
			if opc2 == '3':
				break
	
	if opc == '2':
		while True:
			print ('Hola')
			break
			
	if opc == '3':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('1 - Change Local Directory')
			print ('2 - Regresar')
			opc2 = input('Seleccione una opcion: ')
			if opc2 == '1':
				print('Cambiando el directorio Local')
				path = (path+input("Directorio: ")+'/')
				browse_local(path)
				print(input('Pulsa una tecla para continuar'))
			if opc2 == '2':
				break
				
	if opc == '4':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('1 - Cambiar el directorio remoto')
			print ('2 - Regresar')
			opc2 = input('Seleccione una opcion: ')
			if opc2 == '1':
				print('Cambiando el directorio remoto')
				rd = input("Ingresar el directorio: ")
				action('CWD '+rd)
				print(input('Pulsa una tecla para continuar.'))
			if opc2 == '2':
				break
	
	
	if opc == '5':
		while True:
			directory = ''
			os.system('cls' if os.name == 'nt' else 'clear')
			print('Remote Directory')
			mes = ('PWD')
			send(mes)
			directory = s.recv(1024)
			directory = directory.decode()
			vali = directory.split('i')
			vali = vali[0].split(' ')
			vali = vali[0]
			if vali == '257':
				directory = directory.split('"')
				directory = directory[1]
				print('"'+directory+'"')
			else:
				print('"'+directory+'"')
			listar()
			print('Local Directory')
			local_dir(path)
			browse_local(path)
			print(input('Hit Return'))
			break
	if opc == '6':
		action('SITE CHMOD '+input_var + ' ' + pof)
	if opc == '7':
		break
		
