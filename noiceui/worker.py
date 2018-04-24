import subprocess
from Qt import QtCore


class Worker(QtCore.QThread):
    signal_start = QtCore.Signal()
    signal_output = QtCore.Signal(str)
    signal_abort = QtCore.Signal()
    signal_error = QtCore.Signal()
    singal_complete = QtCore.Signal()

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
        self.signal_start.emit()
        process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

        while process.poll() == None and self.exiting == False:
            line = process.stdout.readline()
            if line:
                self.signal_output.emit(line)
        else:
            if self.exiting and process.poll() == None:
                process.kill()
                self.signal_abort.emit()
            elif process.poll() != 0:
                self.signal_error.emit()
            else:
                self.singal_complete.emit()
