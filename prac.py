import curses
screen = curses.initscr()
screen.addstr(0,0,('Hello'))
screen.refresh()
screen.getch()
curses.endwin()
