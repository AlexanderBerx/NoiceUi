try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore

from noiceui.view import NoiceWindow
from noiceui.model import NoiceModel
from noiceui.prefs import NoicePrefs

class NoiceController(QtCore.QObject):
    def __init__(self):
        super(NoiceController, self).__init__()
        self._view = NoiceWindow()
        self._model = NoiceModel()
        self._prefs = NoicePrefs()

        self._load_prefs()
        self._connect_signals()
        self._bind_model()

    def _bind_model(self):
        self._view.set_aov_model(self._model.aov_model)
        self._view.set_input_model(self._model.input_model)

    def _connect_signals(self):
        self._view.signal_browse_noice_app.connect(self.browse_noice_app)
        self._view.signal_reset.connect(self.reset)
        self._view.signal_add_aov.connect(self.add_aov)
        self._view.signal_window_close.connect(self.window_close)
        self._view.signal_remove_aov[list].connect(self.remove_aovs)

    def _load_prefs(self):
        self._view.set_noice_app(self._prefs.noice_app)
        self._view.set_patch_radius(self._prefs.patch_radius)
        self._view.set_search_radius(self._prefs.search_radius)
        self._view.set_variance(self._prefs.variance)

        for aov in self._prefs.aovs:
            self._model.add_aov(aov)

    def _save_prefs(self):
        self._prefs.noice_app = self._view.get_noice_app()
        self._prefs.patch_radius = self._view.get_patch_radius()
        self._prefs.search_radius = self._view.get_search_radius()
        self._prefs.variance = self._view.get_variance()
        self._prefs.aovs = self._model.get_aov_names()

    # slots
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
    def window_close(self):
        self._save_prefs()

    def show(self):
        self._view.show()


