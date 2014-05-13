import socket
import sys
import os
import time
#import urllib2

UNEXPECTED_RESPONSE = '100'
MISSING_PAGE        = '200'

""" handle the incoming messages from the server """
class handler:
    
    def get_between(self, t, s, e):
        return t.split(s)[-1].split(e)[0]

    def get_id(self, msg):
        lines = msg.split('\r\n')
        return int(lines[-2].split(' ')[0])

    def parse_pasv(self, msg):
        nmsg = self.get_between(msg, '(', ')')
        p = nmsg.split(',')
        return '.'.join(p[:4]), int(p[4])*256 + int(p[5])

    def parse_nlst(self, msg):
        if msg:
            return msg.split('\r\n')[:-1]
        else:
            return []

    def global_parse(self, msg):
        return self.get_between(msg, ' ', '\r\n')

    def string_to_epoch(self, t, timezone):
        localtime = (int(t[:4]),
                     int(t[4:6]),
                     int(t[6:8]),int(t[8:10]),int(t[10:12]),int(t[12:14]),
                     0,0,0)
        return time.mktime(localtime)+timezone

    def parse_time(self, msg, timezone):
        string = self.global_parse(msg)
        return self.string_to_epoch(string, timezone)

    def parse_size(self, msg):
        return self.global_parse(msg)

    def validify_case(self, msg):
        """basic exceptions to some of the relays,
        this will validify if some reponses were
        appropriate enough to continue as required"""
       
        if self.get_id(msg) in (450, 550):
            # 450: no files found in folder
            # 550: means a folder (not a file)
            return False
        return True


""" make a custom socket object """
class mk_socket:
    
    def __init__(self, sid, host, port=21):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.sid = str(sid)
        self.open = True
        self.handle = handler()

    def hold_state(self, error):
        # in the case of an error...
        #print '\n\n!!!', error
        # raw_input('    Socket ID: %s\nPress any key to terminate program ...\n'%self.sid)
        #sys.exit(1)
        pass

    def cls(self):
        # don't close the socket more than once
        if self.open:
            self.s.close()
            self.open = False

    def relay(self, mes='', expect=False, filt=''):
        str(self.send(mes, True, filt))
        return self.recv(expect)

    def recv(self, expect=False):
        print(self.sid, '<<<')
        
        try:
            rec = self.s.recv(1024)
        except socket.error:
            self.hold_state('Software caused connection abort')
            
        print(rec)

        # use expect

        if len(rec) > 3:
            # server has another message
            if rec[3] == '-':
                return rec+self.recv()
        return rec        

    def send(self, mes='', CRLF=True, filt=''):
        print(self.sid, '>>>')

        try:
            self.s.send(mes + ('', '\r\n')[CRLF==True])
            # '\r\n' is a <CRLF> (endline), this tells the 
            # server that this is the end of the command
        except socket.error:
            self.hold_state('Connection reset')

        if CRLF: # avoid outputting the file transfers
            if filt:
                print(mes.replace(filt, '*'*len(filt)))
            else:
                print(mes)


""" open a file, 1024 bytes at a time """
class open_slow:

    def __init__(self, name):

        self.f = open(name, 'rb')
        self.size = os.stat(name)[6]
        self.pos = 0
        self.opened = True

    def next(self, buff=1024):

        self.f.seek(self.pos)
        self.pos += buff

        if self.pos >= self.size:
            piece = self.f.read(-1)
            self.f.close()
            self.opened = False
        else:
            piece = self.f.read(buff)
            
        return piece

"""
FTP Client Class
----------------

This class, for communicating with an FTP,
consists of the following functions ...

.connect       connect to the host
.think         output a thought to the console (debugging)
.do_nothing    check for a connection
.upload        upload a file by its name and contents
.set_time      synchronize the time with the server
               looks for a page containing:
               <?php echo time(); ?>
.set_timezone  set the timezone by hours off of server
               
.LOGIN         login to the FTP with a username and password
.DIR           get a list of files
.SIZE          get the size of a file in bytes
.TIME          get the time of modification in seconds since epoch
.CDUP          change to parent directory
.CWD           change the current working directory
.MKD           create a new folder
.MODE          set the transfer mode
.TYPE          set the type of file to be transferred
.STRU          set the file structure for transfer
.PASV          a passive connection will have the data
               transfer port open on the server's side
.QUIT          close session and connections
"""

class ftp_client:

    # initiate the ftp client class
    def __init__(self):
        # initiate the reply handler
        self.handle = handler()

        # timesonze is defaulted to zero
        self.timezone = 0

        # buffer size
        self.buffer_size = 1024

        # so we know it doesn't exist yet in self.PASV()
        self.sock_pasv = False

    # external helpers
    def connect(self, host):
        """connect to the host"""
        self.sock_main = mk_socket(1, host)
        self.sock_main.recv()

    def set_time(self, page):
        """synchronize the time with the server"""
        ip, port = self.PASV()
        try:
            self.think('Synchronizing time...')
            opener = urllib2.build_opener()
            t1 = int(opener.open('http://'+ip+'/'+page).read())
            t2 = time.time()
            self.timezone = t2 - (t1 + 3600*5)
            self.think('Time zone set to %s seconds'%self.timezone)
            time.sleep(0.5)
            
        except(Exception,msg):
            self.error(MISSING_PAGE, 'was unable to synchronize time')

        self.sock_pasv.cls() # close the passive port

    def set_timezone(self, h):
        """set the timezone by hours off of server"""
        self.timezone = h*3600
                                 
    # start temporary functions
    def think(self, thought):
        print( "!!!", str(thought), '\n')

    def do_nothing(self):
        """check for a connection"""
        self.sock_main.relay('NOOP')

    def error(self, err, msg):
        raise err

    # start command related functions
    def LOGIN(self, usern, passw):
        """login to the FTP with a username and password"""
        self.sock_main.relay('USER '+usern)
        res = self.sock_main.relay('PASS '+passw, filt=passw)

        # expect a 230 (user logged in)
        if self.handle.get_id(res) != 230:
            self.error(UNEXPECTED_RESPONSE, 'incorrect username or password')
            
    def DIR(self):
        """get a list of files"""

        self.PASV()
        msg = self.sock_main.relay('NLST')
        
        if self.handle.validify_case(msg):

            msg = ''
            add = True
            while add != '':
                add = self.sock_pasv.recv()
                msg += add
            self.think('Empty message sent. File list is done.')
            # there is a CRLF, we know we can close
            self.sock_pasv.cls()
        
            flist = self.handle.parse_nlst(msg)
            self.think(flist)
        
            # trigger the expected 226
            self.sock_main.recv(226)

        else:
            self.sock_pasv.cls()
            flist = [] # no files = an empty list
        
        return flist
        
    def SIZE(self, f):
        """get the size of a file in bytes"""
        msg = self.sock_main.relay('SIZE '+f)
        if self.handle.validify_case(msg):
            fsize = self.handle.parse_size(msg)
        else:
            fsize = False
        return fsize

    def TIME(self, f):
        """get the time of modification in seconds since epoch"""
        msg = self.sock_main.relay('MDTM '+f)
        if self.handle.validify_case(msg):
            ftime = self.handle.parse_time(msg, self.timezone)
        else:
            ftime = False
        return ftime

    def CDUP(self):
        """change to parent directory"""
        # note: untested
        self.sock_main.relay('CDUP')

    def MODE(self, m='S'):
        """set the transfer mode"""
        self.sock_main.relay('MODE '+m)

    def TYPE(self, t='A'):
        """set the type of file to be transferred"""
        self.sock_main.relay('TYPE '+t)

    def STRU(self, s='F'):
        """set the file structure for transfer"""
        self.sock_main.relay('STRU '+s)
        
    def CWD(self, dname):
        """change the current working directory"""
        self.sock_main.relay('CWD '+dname, 250)

    def MKD(self, dname):
        """create a new folder"""
        self.sock_main.relay('MKD '+dname, 257)

    def PASV(self):
        """a passive connection will have the data
        transfer port open on the server's side"""

        if self.sock_pasv:
            self.think('Checking for open socket')
            assert not self.sock_pasv.open # make sure there is no port open
        
        # propose passive connection
        msg = self.sock_main.relf.sock_main.relay(alay('PASV'))
        newip=self.handle.parse_pasv(msg)
        newport = self.handle.parse_pasv(msg)

        # make passive connection
        self.sock_pasv = mk_socket(2, newip, newport)

        return newip, newport # return the passive IP/PORT

    def QUIT(self):
        """close session and connections"""
        if self.sock_pasv:
            if self.sock_pasv.open:
                self.think('Passive port open... closing')
                self.sock_pasv.cls()
            else:
                self.think('Passive port already closed')
        self.sock_main.relay('QUIT')
        self.sock_main.cls()
        
    # start quick-access functions
    def upload(self, fname, fsource):
        """upload a file by its name and contents"""

        # open passive connection
        self.PASV()
        self.sock_main.relay('STOR '+fname)

        my_file = open_slow(fsource)
        while my_file.opened:
            self.sock_pasv.send(my_file.next(self.buffer_size),
                                False) # don't include the CRLF in the file transfer

        # close passive connection to end transfer
        self.sock_pasv.cls()
        # warning: the passive port is now closed!

        # trigger the expected 226
        self.sock_main.recv(226)

    # break upload up in to managable pieces
    # for more customizable access
    def upload_init(self, fname, fsource):
        self.PASV()
        self.sock_main.relay('STOR '+fname)
        my_file = open_slow(fsource)
        return my_file
    
    def upload_send(self, my_file, buff):
        self.sock_pasv.send(my_file.next(buff), False)
        return my_file.opened

    def upload_abort(self):
        self.sock_main.send('ABOR')
        self.sock_pasv.cls()
        self.sock_main.recv(226)

    def upload_close(self):
        self.sock_pasv.cls()
        self.sock_main.recv(226)


if __name__ == '__main__':
    """example usage of the FTP Client class"""

    MYclient = ftp_client()
    
    try:
        MYclient.connect(input("Enter FTP Address: "))
        
    except(socket.error):
        print("Could not connect")
        sys.exit(1)
        
    try:
        MYclient.LOGIN(input("Enter Full Username: "),
                       input("Enter Password: "))
        
    except:
        print("Incorrect login")
        sys.exit(1)
    
    MYclient.MODE()    # stream transfer mode
    MYclient.TYPE('I') # image/binary type
    MYclient.STRU()    # file structure

    #MYclient.set_time('~omega/time.php')

    MYclient.CWD('/')
    MYclient.MKD('test')
    MYclient.CWD('test')

    dest = 'my_test_file.py'
    MYclient.upload(dest, sys.argv[0])
    
    folder = MYclient.DIR()
    fsize = MYclient.SIZE(dest)
    ftime = MYclient.TIME(dest)

    MYclient.QUIT()

    if dest in folder:
        print( "Success! '%s' uploaded to the folder.\n\n Size: %s BYTES\n Time: %s"%(dest,fsize,time.ctime(ftime)))
    else:
        print( "File did not succesfully upload.")

    #print folder

