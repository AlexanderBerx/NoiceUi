try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ImportError:
    from Qt import QtWidgets, QtCore, QtGui


class NoiceWindow(QtWidgets.QWidget):
    TITLE = 'NoiceUi'
    signal_browse_noice_app = QtCore.Signal()
    signal_add_aov = QtCore.Signal()
    signal_remove_aov = QtCore.Signal()

    def __init__(self):
        super(NoiceWindow, self).__init__()
        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self.TITLE)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._create_exe_widget())
        layout.addWidget(self._create_options_widget())

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
        widget = QtWidgets.QGroupBox('Options')
        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel('Patch radius'), 0, 0)
        self._spnb_patch_radius = QtWidgets.QSpinBox()
        layout.addWidget(self._spnb_patch_radius, 0, 1)

        layout.addWidget(QtWidgets.QLabel('Search radius'), 1, 0)
        self._spnb_search_radius = QtWidgets.QSpinBox()
        layout.addWidget(self._spnb_search_radius, 1, 1)

        layout.addWidget(QtWidgets.QLabel('Variance'), 2, 0)
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
        self._btn_remove_aov.clicked.connect(self.signal_remove_aov)
        aov_options_layout.addWidget(self._btn_remove_aov)
        aov_options_layout.setAlignment(self._btn_remove_aov, QtCore.Qt.AlignTop)
        layout.addLayout(aov_options_layout, 3, 2)

        return widget

    # mutators
    def set_noice_app(self, path_to_app):
        self._txt_noice_app.setText(path_to_app)
