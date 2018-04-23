try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore

import os
import subprocess
from noiceui.view import NoiceWindow
from noiceui.model import NoiceModel
from noiceui.prefs import NoicePrefs
from noiceui.worker import Worker


class NoiceController(QtCore.QObject):
    def __init__(self):
        super(NoiceController, self).__init__()
        self._view = NoiceWindow()
        self._model = NoiceModel()
        self._prefs = NoicePrefs()
        self._worker = Worker()

        self._load_prefs()
        self._connect_signals()
        self._bind_model()

    def _bind_model(self):
        self._view.set_aov_model(self._model.aov_model)
        self._view.set_input_model(self._model.input_model)

    def _connect_signals(self):
        # ui signals
        self._view.signal_browse_noice_app.connect(self.browse_noice_app)
        self._view.signal_reset.connect(self.reset)
        self._view.signal_add_aov.connect(self.add_aov)
        self._view.signal_window_close.connect(self.window_close)
        self._view.signal_remove_aov[list].connect(self.remove_aovs)
        self._view.signal_add_input.connect(self.add_input)
        self._view.signal_remove_input[list].connect(self.remove_inputs)
        self._view.signal_browse_output.connect(self.browse_output)
        self._view.signal_run.connect(self.run)

        # thread signals
        self._worker.singal_done.connect(self.done)
        self._worker.signal_output[str].connect(self._worker_output)

    def _load_prefs(self):
        self._view.set_noice_app(self._prefs.noice_app)
        self._view.set_patch_radius(self._prefs.patch_radius)
        self._view.set_search_radius(self._prefs.search_radius)
        self._view.set_variance(self._prefs.variance)

        for item in self._prefs.aovs:
            self._model.add_aov(item)

        for item in self._prefs.inputs:
            self._model.add_input(item)

        self._view.set_output(self._prefs.output)

    def _save_prefs(self):
        self._prefs.noice_app = self._view.get_noice_app()
        self._prefs.patch_radius = self._view.get_patch_radius()
        self._prefs.search_radius = self._view.get_search_radius()
        self._prefs.variance = self._view.get_variance()
        self._prefs.aovs = self._model.get_aov_list()
        self._prefs.inputs = self._model.get_input_list()
        self._prefs.output = self._view.get_output()

    # ui slots
    @QtCore.Slot()
    def browse_noice_app(self):
        file_, _ = QtWidgets.QFileDialog.getOpenFileName(self._view, 'Set Noice app')
        if file_:
            self._view.set_noice_app(file_)

    @QtCore.Slot()
    def reset(self):
        # TODO: implement reset functionality
        pass

    @QtCore.Slot()
    def add_aov(self):
        prompt = QtWidgets.QInputDialog(self._view)
        prompt.setWindowTitle('Add AOV')
        prompt.setLabelText('AOV name:')
        prompt.setOkButtonText('Add')
        if prompt.exec_():
            self._model.add_aov(prompt.textValue())

    @QtCore.Slot(list)
    def remove_aovs(self, aovs):
        for item in aovs:
            self._model.remove_aov(item)

    @QtCore.Slot()
    def add_input(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self._view, 'Add input', filter='*.exr *.EXR')
        for item in files:
            self._model.add_input(item)

    @QtCore.Slot(list)
    def remove_inputs(self, inputs):
        for item in inputs:
            self._model.remove_input(item)

    @QtCore.Slot()
    def browse_output(self):
        file_, _ = QtWidgets.QFileDialog.getSaveFileName(self._view, 'Set output', filter='*.exr *.EXR')
        if file_:
            self._view.set_output(file_)

    @QtCore.Slot()
    def window_close(self):
        if self._worker.isRunning():
            self._worker.terminate()

        self._save_prefs()

    # thread slots
    @QtCore.Slot()
    def run(self):
        if not self._worker.isRunning():
            cmd = self._get_cmd()
            cmd = r'python "C:\Workspace\NoiceUi\noiceui\temp.py"'
            self._worker.cmd = cmd
            self._worker.start()
        else:
            self._worker.exiting = True

    @QtCore.Slot()
    def done(self):
        print('Done with thread')

    @QtCore.Slot(str)
    def _worker_output(self, line):
        self._view.add_to_log(line)

    def show(self):
        self._view.show()

    def _get_cmd(self):
        cmd = ''
        cmd += '"{}" '.format(os.path.normpath(self._view.get_noice_app()))
        if self._view.get_patch_radius():
            cmd += '-pr {} '.format(self._view.get_patch_radius())

        if self._view.get_search_radius():
            cmd += '-sr {} '.format(self._view.get_search_radius())

        if self._view.get_variance():
            cmd += '-v {} '.format(self._view.get_variance())

        cmd += ''.join(['-i "{}" '.format(item) for item in self._model.get_input_list()])

        if self._model.get_aov_list():
            cmd += ''.join(['-l "{}" '.format(item) for item in self._model.get_aov_list()])

        cmd += '-o "{}" '.format(self._view.get_output())

        return cmd
