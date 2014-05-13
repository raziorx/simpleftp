
import curses
import time
message = raw_input('Escribe el mensaje que quieres: ' )
q, vertical, horizontal = -1,1,1
y, x = 0, 0
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_YELLOW)
screen.nodelay(1)
g = 1
bold = 0
reverse = 0
b = [curses.A_NORMAL, curses.A_BOLD]
r = [curses.A_NORMAL, curses.A_REVERSE]
curses.noecho()
dims = screen.getmaxyx()
while q < 0 or q in range(49,52) or q in [98,114]:
        q = screen.getch()
        if q in range(49,52):
                g = int(chr(q))
	elif q==98:
		bold = (bold+1) %2
	if q == 114:
		reverse = (reverse+1) %2
        screen.clear()
        screen.addstr(y,x,message,curses.color_pair(g) | b[bold] | r[reverse])
        y += vertical
        x += horizontal
        if y == dims[0]-1:
                vertical = -1
        elif y == 0:
                vertical = 1
        if x == dims[1]-len(message)-1:
                horizontal = -1
        elif x == 0:
                horizontal = 1
        time.sleep(0.2)
curses.endwin()
