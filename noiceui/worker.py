import subprocess
from Qt import QtCore


class Worker(QtCore.QThread):
    """
    Workers class, inherits from QtCore.QThread
    """
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
        """
        property, returns whether the thread needs to be aborting it's current process or not
        :return: bool
        """
        return self._exititng

    @exiting.setter
    def exiting(self, value):
        """
        property, when set to true the current process will be aborted if an process is active
        :param bool value:
        :return: None
        """
        self._exititng = bool(value)

    @property
    def cmd(self):
        """
        returns the command the thread will execute
        :return: str
        """
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        """
        sets the command the thread will execute
        :param set value:
        :return:
        """
        self._cmd = value

    def start(self, *args, **kwargs):
        """
        overwritten function from parent class, sets the exiting property to false
        :param args:
        :param kwargs:
        :return: None
        """
        self.exiting = False
        super(Worker, self).start(*args, **kwargs)

    def run(self):
        """
        thread main event loop
        :return: None
        """
        self.signal_start.emit()
        process = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)

        while process.poll() is None and not self.exiting:
            line = process.stdout.readline()
            if line:
                self.signal_output.emit(line)
        else:
            if self.exiting and not process.poll():
                process.kill()
                self.signal_abort.emit()
            elif process.poll() != 0:
                self.signal_error.emit()
            else:
                self.singal_complete.emit()
