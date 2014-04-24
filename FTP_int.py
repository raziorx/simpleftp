import signal
signal.signal(signal.SIGINT, signal.SIG_IGN)
import socket
import os
import sys
import curses
import traceback
import atexit
import time

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

