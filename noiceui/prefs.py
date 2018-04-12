try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from Qt import QtWidgets, QtCore
import os
import platform
from noiceui import constants


class NoicePrefs(object):
    def __init__(self):
        QtCore.QSettings().setDefaultFormat(QtCore.QSettings.IniFormat)
        QtCore.QCoreApplication.setOrganizationName(constants.APP_NAME)
        QtCore.QCoreApplication.setApplicationName(constants.APP_NAME)

    @property
    def noice_app(self):
        app = QtCore.QSettings().value(constants.PREF_NOICE_APP)
        if not app and platform.system() == 'Windows':
            app = constants.DEFAULT_WIN_NOCIE_APP

        if app:
            app = os.path.normpath(app)

        return app

    @noice_app.setter
    def noice_app(self, value):
        if value:
            QtCore.QSettings().setValue(constants.PREF_NOICE_APP, os.path.normpath(value))
