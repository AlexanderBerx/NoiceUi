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
        QtCore.QSettings().setValue(constants.PREF_NOICE_APP, os.path.normpath(value))

    @property
    def patch_radius(self):
        value = QtCore.QSettings().value(constants.PREF_PATCH_RADIUS)
        return int(value or 0)

    @patch_radius.setter
    def patch_radius(self, value):
        QtCore.QSettings().setValue(constants.PREF_PATCH_RADIUS, int(value))

    @property
    def search_radius(self):
        value = QtCore.QSettings().value(constants.PREF_SEARCH_RADIUS)
        return int(value or 0)

    @search_radius.setter
    def search_radius(self, value):
        QtCore.QSettings().setValue(constants.PREF_SEARCH_RADIUS, int(value))

    @property
    def variance(self):
        value = QtCore.QSettings().value(constants.PREF_VARIANCE)
        return float(value or 0)

    @variance.setter
    def variance(self, value):
        QtCore.QSettings().setValue(constants.PREF_VARIANCE, float(value))

    @property
    def aovs(self):
        aovs = []
        settings = QtCore.QSettings()
        for index in range(settings.beginReadArray(constants.PREF_AOVS)):
            settings.setArrayIndex(index)
            aovs.append(settings.value(str(index)))

        return aovs

    @aovs.setter
    def aovs(self, value):
        settings = QtCore.QSettings()
        settings.beginWriteArray(constants.PREF_AOVS)
        for index, item in enumerate(value):
            settings.setArrayIndex(index)
            settings.setValue(str(index), item)

        settings.endArray()

    @property
    def inputs(self):
        aovs = []
        settings = QtCore.QSettings()
        for index in range(settings.beginReadArray(constants.PREF_INPUTS)):
            settings.setArrayIndex(index)
            aovs.append(settings.value(str(index)))

        return aovs

    @inputs.setter
    def inputs(self, value):
        settings = QtCore.QSettings()
        settings.beginWriteArray(constants.PREF_INPUTS)
        for index, item in enumerate(value):
            settings.setArrayIndex(index)
            settings.setValue(str(index), item)

        settings.endArray()

    @property
    def output(self):
        return QtCore.QSettings().value(constants.PREF_OUTPUT)

    @output.setter
    def output(self, value):
        QtCore.QSettings().setValue(constants.PREF_OUTPUT, os.path.normpath(value))
