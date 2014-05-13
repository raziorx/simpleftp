import socket
import sys
import os
import time
from os import walk
s = socket.socket()
def send(message='',filt=''):
	CRLF=True
	s.send(message + ("\r\n"))
def recieve():
	rec = s.recv(1024)
        print (rec)
        if len(rec) > 3:
            if rec[3] == '-':
                return rec+recieve()
        return (rec)        
def action(message='',filt=''):
	send(message,filt)
	return recieve()
def browse_local(path=''):
	for (dirpath, dirnames, filenames) in walk(path):
		print dirpath
		print ('Files in directory')
		print dirnames
		print filenames
		print ('\n')
		break
def listar():
	message = ('PASV')
	send(message)
	message = s.recv(1024)
	print message
	nmsg = message.split('(')[-1].split(')')[0]
	p = nmsg.split(',')
	newip, newport = '.'.join(p[:4]), int(p[4])*256 + int(p[5])
	print newip
	print newport
	p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	p.connect((newip, newport))
	message = ('NLST')
	action (message)
	rec = p.recv(1024)
	print rec
	p.close
#s.connect((raw_input("Enter FTP Address: "), 21))
s.connect(("192.100.230.21", 21))
print recieve()		
		
#usern = raw_input("Enter user: ")
#action('USER '+usern)
action('USER '+'userftp')
#passw = raw_input("Enter password: ")
#action('PASS '+passw)
action('PASS '+'r3d3sf1s1c@s')
print("Remote Directory")
message = ('PWD')
action(message)
print("Local Directory")
path = ('/home/ec2-user/proyecto/simpleftp')
browse_local(path)
print('Change remote directory')
message = ('CWD pub')
action(message)
print('Change local directory')
path = (path+raw_input("Directorio: ")+'/')
browse_local(path)
message = ('TYPE I')
action(message)
message = ('TYPE A')
action(message)
message = ('MODE S')
action(message)
listar()
#f=open ("libroR.pdf", "rb") 
#l = f.read(1024)
#while (l):
 #   s.send(l)
  #  l = f.read(1024)
s.close                     # Close the socket when done
