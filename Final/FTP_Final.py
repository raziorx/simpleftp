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
	    
def operacion(mes=''):
	send(mes)
	return recieve()
def local_dir(ruta=''):
	for (dirruta, dirnames, filenames) in walk(ruta):
		print ('"'+dirruta+'"')
		break
def browse_local(ruta=''):
	for (dirruta, dirnames, filenames) in walk(ruta):
		print (dirnames)
		print (filenames)
		print ('\n')
		break
def pasv():
	while True:
		restriccion = ''
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
		
def envarch(file=''):
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

def enumera():
	newip, newport = pasv()
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	mes = ('NLST')
	operacion (mes)
	rec = p.recv(1024)
	rec = rec.decode()
	rec.split('\r\n')
	print (rec)
	mes = ('ABOR')
	p.send(bytes(mes + ("\r\n"), "UTF-8"))
	p.close
	recieve()

s.connect(("192.100.230.21", 21))
s.recv(1024)		
operacion('USER '+'userftp')
operacion('PASS '+'r3d3sf1s1c@s')
ruta = ('/home/ec2-user/proyecto/')
buff=1024
#Menu
while True:
	os.system('cls' if os.name == 'nt' else 'clear')
	print ('*-------------------------------*') 
	print ('*\t\tMenu\t\t*') 
	print ('*1 - Enviar archivos\t\t*') 
	print ('*2 - Recibir archivos\t\t*') 
	print ('*3 - Cambiar directorio local\t*')
	print ('*4 - Cambiar directorio Remoto\t*')
	print ('*5 - Imprimir directorios\t*') 
	print ('*6 - Modificar permisos\t\t*')
	print ('*7 - Salir\t\t\t*')
	print ('*-------------------------------*') 
	seleccion = input('Seleccione una opcion: ')
	if seleccion == '1':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('*-------------------------------*') 
			print ('*\tModificar\t*') 
			print ('Seleccione el Tipo de archivo que deseas subir')
			print ('1 - Archivos de Texto')
			print ('2 - Imagenes')
			print ('3 - Return')
			seleccion2 = input('Seleccione una opcion: ')
			if seleccion2 == '1':
				os.ruta = ruta
				file = input('¿Cual es el nombre del archivo?')
				mes = ('TYPE A')
				operacion(mes)
				envarch(file)
				print(input('Pulse una tecla para continuar.'))
			if seleccion2 == '2':
				os.ruta = ruta
				file = input('¿Cual es el nombre del archivo?')
				mes = ('TYPE I')
				operacion(mes)
				envarch(file)
				print(input('Hit Return'))
			if seleccion2 == '3':
				break
	
	if seleccion == '2':
		while True:
			print ('Hola')
			break
			
	if seleccion == '3':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('1 - Cambiar el directorio Local.')
			print ('2 - Regresar')
			print ('3 - Directorio original')
			seleccion2 = input('Seleccione una opcion: ')
			if seleccion2 == '1':
				print('Cambiando el directorio Local')
				ruta = (ruta+input("Directorio: ")+'/')
				browse_local(ruta)
				print(input('Pulsa una tecla para continuar'))
			if seleccion2 == '2':
				break
			if seleccion2 == '3':
				ruta = ('/home/ec2-user/proyecto/')
				os.ruta = ruta
				
	if seleccion == '4':
		while True:
			os.system('cls' if os.name == 'nt' else 'clear')
			print ('1 - Cambiar el directorio remoto')
			print ('2 - Regresar')
			seleccion2 = input('Seleccione una opcion: ')
			if seleccion2 == '1':
				print('Cambiando el directorio remoto')
				rd = input("Ingresar el directorio: ")
				operacion('CWD '+rd)
				print(input('Pulsa una tecla para continuar.'))
			if seleccion2 == '2':
				break
	
	
	if seleccion == '5':
		while True:
			
			directory = ''
			os.system('cls' if os.name == 'nt' else 'clear')
			print('Directorio Remoto')
			mes = ('PWD')
			send(mes)
			directory = s.recv(1024)
			directory = directory.decode()
			restriccion = directory.split('i')
			restriccion = restriccion[0].split(' ')
			restriccion = restriccion[0]
			if restriccion == '257':
				directory = directory.split('"')
				directory = directory[1]
				print('"'+directory+'"')
			else:
				print('"'+directory+'"')
			enumera()
			print('Directorio Local')
			local_dir(ruta)
			browse_local(ruta)
			print(input('Pulse una tecla para continuar.'))
			break
	if seleccion == '6':
		file=input('Escribe el nombre del archivo.')
		permisos=input('Escribe los permisos en hexadecimal Por ejemplo (777)')
		operacion('SITE CHMOD '+permisos+ ' ' + file)
	if seleccion == '7':
		break
		
