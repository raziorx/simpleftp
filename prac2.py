import curses
screen = curses.initscr()
dims = screen.getmaxyx()
screen.addstr(dims[0]/2,dims[1]/2,('Hello'))
screen.refresh()
screen.getch()
curses.endwin()


