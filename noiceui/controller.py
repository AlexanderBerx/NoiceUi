import os
from Qt import QtWidgets, QtCore
from noiceui.worker import Worker
from noiceui.view import NoiceWindow
from noiceui.model import NoiceModel
from noiceui.prefs import NoicePrefs


class NoiceController(QtCore.QObject):
    """
    NoiceController, controller class, inherits from QObject
    """

    def __init__(self):
        """
        initialises the app and connects the model to the view
        """
        super(NoiceController, self).__init__()
        self._view = NoiceWindow()
        self._model = NoiceModel()
        self._prefs = NoicePrefs()
        self._worker = Worker()

        self._load_prefs()
        self._connect_signals()
        self._bind_model()

    def _bind_model(self):
        """
        binds the model to the view
        :return: None
        """
        self._view.set_aov_model(self._model.aov_model)
        self._view.set_input_model(self._model.input_model)

    def _connect_signals(self):
        """
        connects the signals of the view and worker thread to the controller
        :return: None
        """
        # ui signals
        self._view.signal_browse_noice_app.connect(self.browse_noice_app)
        self._view.signal_add_aov.connect(self.add_aov)
        self._view.signal_window_close.connect(self.window_close)
        self._view.signal_remove_aov[list].connect(self.remove_aovs)
        self._view.signal_add_input.connect(self.add_input)
        self._view.signal_remove_input[list].connect(self.remove_inputs)
        self._view.signal_browse_output.connect(self.browse_output)
        self._view.signal_run.connect(self.run)

        # thread signals
        self._worker.signal_output[str].connect(self._worker_output)
        self._worker.signal_start.connect(self._start)
        self._worker.signal_abort.connect(self._abort)
        self._worker.singal_complete.connect(self._complete)
        self._worker.signal_error.connect(self._error)

    def _load_prefs(self):
        """
        loads the app settings from the pref file
        :return: None
        """
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
        """
        saves the app settings to the pref file
        :return: None
        """
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
        """
        Slot, launches a file browser for setting the noice application
        :return: None
        """
        file_, _ = QtWidgets.QFileDialog.getOpenFileName(self._view, 'Set Noice app')
        if file_:
            self._view.set_noice_app(file_)

    @QtCore.Slot()
    def add_aov(self):
        """
        Slot, launches an input prompt for adding an new AOV
        :return: None
        """
        prompt = QtWidgets.QInputDialog(self._view)
        prompt.setWindowTitle('Add AOV')
        prompt.setLabelText('AOV name:')
        prompt.setOkButtonText('Add')
        if prompt.exec_():
            self._model.add_aov(prompt.textValue())

    @QtCore.Slot(list)
    def remove_aovs(self, aovs):
        """
        Slot, removes the currently selected aov's in the view from the model
        :param list aovs: list of indexes
        :return: None
        """
        for item in aovs:
            self._model.remove_aov(item)

    @QtCore.Slot()
    def add_input(self):
        """
        Slot, launches an file browser for adding .exr files as input
        :return: None
        """
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(self._view, 'Add input', filter='*.exr *.EXR')
        for item in files:
            self._model.add_input(item)

    @QtCore.Slot(list)
    def remove_inputs(self, inputs):
        """
        Slot, removes the selected input items in the view from the model
        :param list inputs: list of indexes
        :return: None
        """
        for item in inputs:
            self._model.remove_input(item)

    @QtCore.Slot()
    def browse_output(self):
        """
        Slot, launches an browser to set the output file
        :return: None
        """
        file_, _ = QtWidgets.QFileDialog.getSaveFileName(self._view, 'Set output', filter='*.exr *.EXR')
        if file_:
            self._view.set_output(file_)

    @QtCore.Slot()
    def window_close(self):
        """
        Slot, connects to window close signal, terminates the worker thread if running and
        saves the app preferences to the pref file
        :return: None
        """
        if self._worker.isRunning():
            self._worker.terminate()

        self._save_prefs()

    # thread slots
    @QtCore.Slot()
    def run(self):
        """
        Slot, launches noice if the worker thread isn't running if the thread
        is running it will be aborted
        :return: None
        """
        if not self._worker.isRunning():
            cmd = self._get_cmd()
            self._view.add_to_log(cmd)
            self._worker.cmd = cmd
            self._worker.start()
        else:
            self._worker.exiting = True
            self._view.toggle_run_btn(False)

    @QtCore.Slot()
    def _start(self):
        """
        Slot, updates the ui options when the worker thread starts
        :return: None
        """
        self._view.set_run_btn_text('Abort')
        self._view.add_to_log('Started Noice')
        self._view.toggle_progress()

    @QtCore.Slot()
    def _complete(self):
        """
        Slot, updates the ui options when the worker thread is done
        :return: None
        """
        self._view.set_run_btn_text('Run')
        self._view.add_to_log('Completed Noice')
        self._view.toggle_progress(False)

    @QtCore.Slot()
    def _abort(self):
        """
        Slot, updates the ui options when the worker thread is aborted
        :return: None
        """
        self._view.set_run_btn_text('Run')
        self._view.toggle_run_btn()
        self._view.add_to_log('Aborted Noice')
        self._view.toggle_progress(False)

    @QtCore.Slot()
    def _error(self):
        """
        Slot, updates the ui options when the worker thread errors
        :return: None
        """
        self._view.set_run_btn_text('Run')
        self._view.add_to_log('Error running noice')
        self._view.toggle_progress(False)

    @QtCore.Slot(str)
    def _worker_output(self, line):
        """
        Slot, connects to the worker thread, adds the given input to the log, removes any enters
        :param str line:
        :return: None
        """
        line = line.replace('\n', '')
        self._view.add_to_log(line)

    def show(self):
        """
        show the view
        :return: None
        """
        self._view.show()

    def _get_cmd(self):
        """
        formats an command string with the set options
        :return: str
        """
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
