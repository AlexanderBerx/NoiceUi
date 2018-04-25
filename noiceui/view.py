from Qt import QtWidgets, QtCore, QtGui


class NoiceWindow(QtWidgets.QWidget):
    """
    NoiceWindow, inherits from QWidget
    """
    TITLE = 'NoiceUi'
    signal_browse_noice_app = QtCore.Signal()
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
        """
        initialise the ui
        :return: None
        """
        self.setWindowTitle(self.TITLE)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._create_exe_widget())
        layout.addWidget(self._create_options_widget())
        layout.addWidget(self._create_progress_widget())
        layout.addWidget(self._create_run_widget())

    def _create_exe_widget(self):
        """
        creates and returns a widget for the noice app to connect to
        :return: QtWidgets.QWidget
        """
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
        """
        creates and returns a widget for the noice options
        :return: QtWidgets.QWidget
        """
        widget = QtWidgets.QGroupBox('Options:')
        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

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
        """
        creates and returns a widget for the run widget
        :return: QtWidgets.QWidget
        """
        self._btn_run = QtWidgets.QPushButton('Run')
        self._btn_run.clicked.connect(self.signal_run)
        return self._btn_run

    def _create_progress_widget(self):
        """
        creates and returns a widget for the progress widget
        :return: QtWidgets.QWidget
        """
        widget = QtWidgets.QGroupBox('Progress:')
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        self._txt_log = QtWidgets.QTextEdit()
        self._txt_log.setReadOnly(True)
        layout.addWidget(self._txt_log)

        self._pbar = QtWidgets.QProgressBar()
        self._pbar.setTextVisible(False)
        layout.addWidget(self._pbar)

        return widget

    # other
    @QtCore.Slot()
    def _signal_aov_removal(self):
        """
        Slot, emits the the indexes of the selected aovs with the signal_remove_aov signal
        :return: None
        """
        self.signal_remove_aov.emit(self._lst_aovs.selectedIndexes())

    @QtCore.Slot()
    def _signal_input_removal(self):
        """
        Slot, emits the the indexes of the selected inputs with the signal_remove_input signal
        :return: None
        """
        self.signal_remove_input.emit(self._lst_input.selectedIndexes())

    # mutator's
    def set_noice_app(self, value):
        """
        sets the path to the noice app
        :param str value: file path
        :return: None
        """
        self._txt_noice_app.setText(value)

    def set_patch_radius(self, value):
        """
        sets the patch radius
        :param int value: patch radius
        :return: None
        """
        self._spnb_patch_radius.setValue(int(value))

    def set_search_radius(self, value):
        """
        sets the search radius
        :param int value: search radius
        :return: None
        """
        return self._spnb_search_radius.setValue(int(value))

    def set_variance(self, value):
        """
        sets the variance
        :param float value: variance
        :return: None
        """
        return self._spnb_variance.setValue(float(value))

    def set_aov_model(self, model):
        """
        sets the aov model
        :param QtGui.QStandardItemModel model:
        :return: None
        """
        self._lst_aovs.setModel(model)

    def set_input_model(self, model):
        """
        sets the input model
        :param QtGui.QStandardItemModel model:
        :return: None
        """
        self._lst_input.setModel(model)

    def set_output(self, value):
        """
        sets the output file
        :param str value: file path
        :return: None
        """
        self._txt_output.setText(value)

    def add_to_log(self, line):
        """
        adds to to the log
        :param str line:
        :return: None
        """
        self._txt_log.append(line)

    def set_run_btn_text(self, text):
        """
        sets the run button text
        :param str text:
        :return: None
        """
        self._btn_run.setText(text)

    def toggle_run_btn(self, toggle=True):
        """
        enables or disables the run button
        :param bool toggle:
        :return: None
        """
        self._btn_run.setEnabled(toggle)

    def toggle_progress(self, toggle=True):
        """
        toggles the progress bar, if on the process bar will run infinitely
        :param bool toggle:
        :return: None
        """
        if toggle:
            self._pbar.setRange(0, 0)
        else:
            self._pbar.setRange(0, 1)

    # accessors
    def get_noice_app(self):
        """
        returns the path to the noice app
        :return: txt
        """
        return self._txt_noice_app.text()

    def get_patch_radius(self):
        """
        returns the patch radius
        :return: int
        """
        return self._spnb_patch_radius.value()

    def get_search_radius(self):
        """
        returns the search radius
        :return: int
        """
        return self._spnb_search_radius.value()

    def get_variance(self):
        """
        returns the variance
        :return: float
        """
        return self._spnb_variance.value()

    def get_output(self):
        """
        returns the output path
        :return: str
        """
        return self._txt_output.text()

    def closeEvent(self, *args, **kwargs):
        """
        overwritten func from QWidget, emits signal_window_close signal before calling
        the original func
        :param args:
        :param kwargs:
        :return: None
        """
        self.signal_window_close.emit()
        super(NoiceWindow, self).closeEvent(*args, **kwargs)
