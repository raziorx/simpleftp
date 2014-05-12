#!/usr/bin/python
# maybe you need to change the above line

# no license, no copyright, no warranties: placed into the Public Domain
# written by Marco Amrein in the year 2000

# pyFTPdrop 0.2.1
# ***************

# revision history:
#       0.2.0   initial public release
#       0.2.1   more informative FTP replies

import sys, syslog, socket,string, os

# here you can configure the stuff
class config:
	welcome_msg = "220 pyFTPdrop raps Yo man! What's up in the Ghetto?"
	max_cmd_len = 255
	storage_path = "/home/joesmith/drop"
	debug = 1 # verbose would be a better description
	filename_goodchars = string.letters + string.digits + ".-_"

# a namespace to store peer's data
class peer:
	cntrsock = socket.fromfd(sys.stderr.fileno(), socket.AF_INET, socket.SOCK_STREAM)
	ip = cntrsock.getpeername()[0]
	dataport = None

# 
def reply(x):
	sys.stderr.write(x + "\r\n")
	if config.debug:
		syslog.syslog("R:"+repr(x))

def create_datasock():
	if not peer.dataport:
		reply("425 what about a PORT command?")
		return
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(peer.ip,peer.dataport)
		reply("150 dataconnection is up!")
		return sock
	except socket.error:
		reply("425 your dataport sucks big time!")
		return

def cmd_quit(_):
	reply("221 Have a good one!")
	raise SystemExit

def cmd_user(_):
	reply("230 Sure you are!")

def cmd_pass(_):
	reply("230 You think I care about passwords?")

def cmd_dummy(_):
	reply("200 OK (in other words: ignored)")

def cmd_syst(_):
	reply("215 UNIX Type: L8")

def cmd_pasv(_):
	reply("500 You're firewalled? What a pity...")

def cmd_port(port_id):
	numstr = filter(lambda x: x in "0123456789,", port_id)
	parts = string.split(numstr,",")

	try:
		hi = int(parts[-2])
		lo = int(parts[-1])
		for v in [hi,lo]:
			if v < 0 or v > 255:
				raise ValueError
	except IndexError:	
		reply("501 are you a hacker?")
		return
	except ValueError:
		reply("501 looks like nonsense to me...")
		return

	peer.dataport = (hi << 8) + lo
	
	reply("230 Port is " + str(peer.dataport)+ " (am ignoring specified IP for security)")

def cmd_stor(raw_filename):
	filename = filter(lambda x: x in config.filename_goodchars, raw_filename)
	if filename == "":
		reply("553 Filename has not one single useful char!")
		return
	if filename[0] == ".":
		reply("553 No dot files please!")
		return

	filepath = os.path.join(config.storage_path,filename)

	try:
		open(filepath,"r").close()
		reply("553 Permission denied!")
		return
	except IOError:
		pass

	try:
		f = open(filepath,"w")
	except IOError:
		reply("553 File creation failed!")

	sock = create_datasock()

	if not sock:
		f.close()
		return

	try:
		while 1:
			a = sock.recv(1024)
			f.write(a)
			if len(a) == 0:
				break
	except socket.error:
		pass
	try:
		sock.close()
	except socket.error:
		pass
	f.close()
	reply("226 Phew, upload successfully completed")

cmdlist = (
	("quit" , cmd_quit),
	("syst", cmd_syst),
	("user", cmd_user),
	("pass", cmd_pass),
	("port", cmd_port),
	("stor", cmd_stor),
	("pasv", cmd_pasv),
	("type", cmd_dummy)
)



# parses the command and eventually calls the appropriate routine
def docmd(cmd):
	if config.debug:
		syslog.syslog("C:"+repr(cmd))

	# if the connection has broken... we have to shut down:
	if cmd == "":
		raise SystemExit

	# filter suspicious chars first
	cmd2 = filter(lambda x: ord(x) >= 32,cmd)

	lcmd2 = string.lower(cmd2)

	for c in cmdlist:
		if string.find(lcmd2, c[0]) == 0:
			return c[1](cmd2[len(c[0]):])

	reply("500 This thing is upload only! I'm gonna ignore this...")
	return

	

# the main routine
# ----------------


syslog.openlog("PyFTPdrop["+peer.ip+"]",0,syslog.LOG_DAEMON)
syslog.syslog("Incoming connection.")

(uid,gid) = os.stat(config.storage_path)[4:6]
os.setgid(gid)
os.setuid(uid)

reply(config.welcome_msg)

try:
	while 1:
		docmd(sys.stdin.readline(config.max_cmd_len))
finally:	
	syslog.syslog("Connection closed.")
	syslog.closelog()
