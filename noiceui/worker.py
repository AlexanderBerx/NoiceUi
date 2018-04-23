import sys
import time
import subprocess
import threading

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore


class Worker(QtCore.QThread):
    singal_done = QtCore.Signal()
    signal_output = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self._exititng = False
        self._cmd = ''

    @property
    def exiting(self):
        return self._exititng

    @exiting.setter
    def exiting(self, value):
        self._exititng = bool(value)

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = value

    def start(self, *args, **kwargs):
        self._exititng = False
        super(Worker, self).start(*args, **kwargs)

    def run(self):
        process = subprocess.Popen(self.cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        while process.poll() == None and self.exiting == False:
            line = process.stdout.readline()
            if line:
                self.signal_output.emit(line)
        else:
            if self.exiting and process.poll()==None:
                process.kill()
                sys.stdout.write('aborted')
            else:
                sys.stdout.write('Process completed\n')
