try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore


class NoiceWindow(QtWidgets.QWidget):
    TITLE = 'NoiceUi'
    signal_browse_noice_app = QtCore.Signal()

    def __init__(self):
        super(NoiceWindow, self).__init__()
        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self.TITLE)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self._create_exe_widget())

    def _create_exe_widget(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel('Noice App:'))
        self._txt_noice_app = QtWidgets.QLineEdit()
        layout.addWidget(self._txt_noice_app)

        self._btn_browse_noice_app = QtWidgets.QPushButton()
        self._btn_browse_noice_app.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))
        self._btn_browse_noice_app.clicked.connect(self.signal_browse_noice_app)

        layout.addWidget(self._btn_browse_noice_app)
        return widget

    # mutators
    def set_noice_app(self, path_to_app):
        self._txt_noice_app.setText(path_to_app)
