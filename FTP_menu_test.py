import signal
signal.signal(signal.SIGINT, signal.SIG_IGN)
import socket
import os
import sys
import curses
import traceback
import atexit
import time

class cmenu(object):
    datum = {}
    ordered = []
    pos = 0


    def __init__(self, options, title="FTP MENU"):
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.curs_set(0)
        self.screen = curses.initscr()
        self.screen.keypad(1)

        self.h = curses.color_pair(1)
        self.n = curses.A_NORMAL

        for item in options:
            k, v = item.items()[0]
            self.datum[k] = v
            self.ordered.append(k)

        self.title = title

        atexit.register(self.cleanup)

    def cleanup(self):
        curses.doupdate()
        curses.endwin()

		  def upKey(self):
        if self.pos == (len(self.ordered) - 1):
            self.pos = 0
        else:
            self.pos += 1

    def downKey(self):
        if self.pos <= 0:
            self.pos = len(self.ordered) - 1
        else:
            self.pos -= 1

    def display(self):
        screen = self.screen

        while True:
            screen.clear()
            screen.addstr(2, 2, self.title, curses.A_STANDOUT|curses.A_BOLD)
            screen.addstr(4, 2, "Please select an interface...", curses.A_BOLD)

            ckey = None
            func = None

            while ckey != ord('\n'):
                for n in range(0, len(self.ordered)):
                    optn = self.ordered[n]

                    if n != self.pos:
                        screen.addstr(5 + n, 4, "%d. %s" % (n, optn), self.n)
                    else:
                        screen.addstr(5 + n, 4, "%d. %s" % (n, optn), self.h)
                screen.refresh()

                ckey = screen.getch()

                if ckey == 258:
                    self.upKey()

                if ckey == 259:
                    self.downKey()
  ckey = 0
            self.cleanup()
            if self.pos >= 0 and self.pos < len(self.ordered):
                self.datum[self.ordered[self.pos]]()
                self.pos = -1
            else:
                curses.flash()



def top():
    os.system("top")

def exit():
    sys.exit(1)
def ejemplo():
        screen = curses.initscr()
        screen.nodelay(1)
        dims = screen.getmaxyx()
        q=-1
        x,y=0, 0
        vertical = 1
        horizontal = 1

        while q<0:
                screen.clear()
                screen.addstr(y,x,('Hello'))
                screen.refresh()
                y += vertical
                x += horizontal
                if y == dims[0] -1:
                        vertical = -1
                elif y == 0:
                        vertical = 1
                if x == dims[1] - len(('Hello'))-1:
                        horizontal = -1
                elif x == 0:
                        horizontal = 1
                q = screen.getch()
                time.sleep(0.2)
 screen.getch()
        curses.endwin()
def conexion():
        s = socket.socket()

#Nos conectamos al servidor con el metodo connect. Tiene dos parametros
#El primero es la IP del servidor y el segundo el puerto de conexion
        s.connect(("192.168.1.x", 9999))

#Creamos un bucle para retener la conexion
        while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
                mensaje = raw_input("Mensaje a enviar >> ")

    #Con la instancia del objeto servidor (s) y el metodo send, enviamos el mensaje introducido
                s.send(mensaje)

    #Si por alguna razon el mensaje es close cerramos la conexion
                if mensaje == "close":
                        break

#Imprimimos la palabra Adios para cuando se cierre la conexion
        print "Adios."

#Cerramos la instancia del objeto servidor
        s.close()

try:
    c = cmenu([
        { "Crear conexion": conexion },
        { "Exit": exit },
        ])
    c.display()

except SystemExit:
    pass
else:
    #log(traceback.format_exc())
    c.cleanup()
