import curses
import time
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



