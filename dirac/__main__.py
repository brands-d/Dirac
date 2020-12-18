import sys
import signal

from dirac.dirac import Dirac

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
    app = Dirac(sys.argv)
    sys.exit(app.run())
