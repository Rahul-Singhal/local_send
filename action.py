import termios, fcntl, sys, os, time
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

startTime = time.time()
nowTime = time.time()
try:
    while nowTime - startTime < 5.0:
        nowTime = time.time()
        try:
            c = sys.stdin.read(1)
            print str(repr(c))
            print "\\x0b"
            if str(repr(c)) == "'\\x0b'":
                print 'aesome'
            else:
                print 'not so aesome'
        except IOError: pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
print "passed"