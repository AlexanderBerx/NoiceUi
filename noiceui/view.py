try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ImportError:
    from Qt import QtWidgets, QtCore, QtGui


class NoiceWindow(QtWidgets.QWidget):
    TITLE = 'NoiceUi'
    signal_browse_noice_app = QtCore.Signal()
    signal_reset = QtCore.Signal()
    signal_add_aov = QtCore.Signal()
    signal_remove_aov = QtCore.Signal(list)
    signal_add_input = QtCore.Signal()
    signal_remove_input = QtCore.Signal(list)
    signal_browse_output = QtCore.Signal()
    signal_run = QtCore.Signal()
    signal_window_close = QtCore.Signal()

    def __init__(self):
        super(NoiceWindow, self).__init__()
        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self.TITLE)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._create_exe_widget())
        layout.addWidget(self._create_options_widget())
        layout.addWidget(self._create_progress_widget())
        layout.addWidget(self._create_run_widget())

    def _create_exe_widget(self):
        widget = QtWidgets.QGroupBox('Noice App:')
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        self._txt_noice_app = QtWidgets.QLineEdit()
        layout.addWidget(self._txt_noice_app)

        self._btn_browse_noice_app = QtWidgets.QPushButton()
        self._btn_browse_noice_app.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        self._btn_browse_noice_app.clicked.connect(self.signal_browse_noice_app)

        layout.addWidget(self._btn_browse_noice_app)
        return widget

    def _create_options_widget(self):
        widget = QtWidgets.QGroupBox('Options:')
        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

        self._btn_reset = QtWidgets.QPushButton()
        self._btn_reset.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_BrowserReload))
        self._btn_reset.clicked.connect(self.signal_reset)

        layout.addWidget(self._btn_reset, 0, 3)

        layout.addWidget(QtWidgets.QLabel('Patch radius:'), 0, 0)
        self._spnb_patch_radius = QtWidgets.QSpinBox()
        layout.addWidget(self._spnb_patch_radius, 0, 1)

        layout.addWidget(QtWidgets.QLabel('Search radius:'), 1, 0)
        self._spnb_search_radius = QtWidgets.QSpinBox()
        layout.addWidget(self._spnb_search_radius, 1, 1)

        layout.addWidget(QtWidgets.QLabel('Variance:'), 2, 0)
        self._spnb_variance = QtWidgets.QDoubleSpinBox()
        layout.addWidget(self._spnb_variance, 2, 1)

        layout.addWidget(QtWidgets.QLabel('AOV\'s:'), 3, 0)
        self._lst_aovs = QtWidgets.QListView()
        layout.addWidget(self._lst_aovs, 3, 1)

        aov_options_layout = QtWidgets.QVBoxLayout()
        self._btn_add_aov = QtWidgets.QPushButton()
        self._btn_add_aov.setIcon(QtGui.QIcon(':/plus_icon'))
        self._btn_add_aov.clicked.connect(self.signal_add_aov)
        aov_options_layout.addWidget(self._btn_add_aov)

        self._btn_remove_aov = QtWidgets.QPushButton()
        self._btn_remove_aov.setIcon(QtGui.QIcon(':/minus_icon'))
        self._btn_remove_aov.clicked.connect(self._signal_aov_removal)
        aov_options_layout.addWidget(self._btn_remove_aov)
        aov_options_layout.setAlignment(self._btn_remove_aov, QtCore.Qt.AlignTop)
        layout.addLayout(aov_options_layout, 3, 2)

        layout.addWidget(QtWidgets.QLabel('Input:'), 4, 0)
        self._lst_input = QtWidgets.QListView()
        layout.addWidget(self._lst_input, 4, 1)

        input_options_layout = QtWidgets.QVBoxLayout()
        self._btn_add_input = QtWidgets.QPushButton()
        self._btn_add_input.setIcon(QtGui.QIcon(':/plus_icon'))
        self._btn_add_input.clicked.connect(self.signal_add_input)
        input_options_layout.addWidget(self._btn_add_input)

        self._btn_remove_input = QtWidgets.QPushButton()
        self._btn_remove_input.setIcon(QtGui.QIcon(':/minus_icon'))
        self._btn_remove_input.clicked.connect(self._signal_input_removal)
        input_options_layout.addWidget(self._btn_remove_input)
        input_options_layout.setAlignment(self._btn_remove_input, QtCore.Qt.AlignTop)
        layout.addLayout(input_options_layout, 4, 2)

        layout.addWidget(QtWidgets.QLabel('Output:'), 5, 0)
        self._txt_output = QtWidgets.QLineEdit()
        layout.addWidget(self._txt_output, 5, 1)
        self._btn_browse_output = QtWidgets.QPushButton()
        self._btn_browse_output.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        self._btn_browse_output.clicked.connect(self.signal_browse_output)
        layout.addWidget(self._btn_browse_output, 5, 2)

        return widget

    def _create_run_widget(self):
        self._btn_run = QtWidgets.QPushButton('Run')
        self._btn_run.clicked.connect(self.signal_run)
        return self._btn_run

    def _create_progress_widget(self):
        widget = QtWidgets.QGroupBox('Progress:')
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        #self._txt_log = QtWidgets.QTextEdit()
        #layout.addWidget(self._txt_log)
        self._pbar = QtWidgets.QProgressBar()
        layout.addWidget(self._pbar)

        return widget

    # other
    @QtCore.Slot()
    def _signal_aov_removal(self):
        self.signal_remove_aov.emit(self._lst_aovs.selectedIndexes())

    @QtCore.Slot()
    def _signal_input_removal(self):
        self.signal_remove_input.emit(self._lst_input.selectedIndexes())

    # mutator's
    def set_noice_app(self, value):
        self._txt_noice_app.setText(value)

    def set_patch_radius(self, value):
        self._spnb_patch_radius.setValue(int(value))

    def set_search_radius(self, value):
        return self._spnb_search_radius.setValue(int(value))

    def set_variance(self, value):
        return self._spnb_variance.setValue(float(value))

    def set_aov_model(self, model):
        self._lst_aovs.setModel(model)

    def set_input_model(self, model):
        self._lst_input.setModel(model)

    def set_output(self, value):
        self._txt_output.setText(value)

    # accessors
    def get_noice_app(self):
        return self._txt_noice_app.text()

    def get_patch_radius(self):
        return self._spnb_patch_radius.value()

    def get_search_radius(self):
        return self._spnb_search_radius.value()

    def get_variance(self):
        return self._spnb_variance.value()

    def get_output(self):
        return self._txt_output.text()

    def closeEvent(self, *args, **kwargs):
        self.signal_window_close.emit()
        super(NoiceWindow, self).closeEvent(*args, **kwargs)



