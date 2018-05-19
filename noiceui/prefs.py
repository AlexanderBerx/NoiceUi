import os
import platform
from Qt import QtCore
from noiceui import constants


class NoicePrefs(object):
    """
    NoicePrefs class, binds to the prefs file using the location provided by the Qt system
    """
    def __init__(self):
        QtCore.QSettings().setDefaultFormat(QtCore.QSettings.IniFormat)
        QtCore.QCoreApplication.setOrganizationName(constants.APP_NAME)
        QtCore.QCoreApplication.setApplicationName(constants.APP_NAME)

    @property
    def noice_app(self):
        """
        reads the set noice app from the prefs, if no pref is set and the host os is windows
        the default location of the noice app will be used if existing
        :return: str
        """
        app = QtCore.QSettings().value(constants.PREF_NOICE_APP)
        if not app and platform.system() == 'Windows':
            if os.path.isfile(constants.DEFAULT_WIN_NOCIE_APP):
                app = constants.DEFAULT_WIN_NOCIE_APP

        if app:
            app = os.path.normpath(app)

        return app

    @noice_app.setter
    def noice_app(self, value):
        """
        sets the noice app in the settings
        :param str value: file path to the noice app
        :return: None
        """
        QtCore.QSettings().setValue(constants.PREF_NOICE_APP, os.path.normpath(value))

    @property
    def patch_radius(self):
        """
        reads & returns the patch radius from the settings if no value was set 0 is returned
        :return: int
        """
        value = QtCore.QSettings().value(constants.PREF_PATCH_RADIUS)
        return int(value or 0)

    @patch_radius.setter
    def patch_radius(self, value):
        """
        sets the patch radius in the settings
        :param int value:
        :return: None
        """
        QtCore.QSettings().setValue(constants.PREF_PATCH_RADIUS, int(value))

    @property
    def search_radius(self):
        """
        reads & returns the search radius from the settings if no value was set 0 is returned
        :return: int
        """
        value = QtCore.QSettings().value(constants.PREF_SEARCH_RADIUS)
        return int(value or 0)

    @search_radius.setter
    def search_radius(self, value):
        """
        sets the search radius in the settings
        :param int value:
        :return: None
        """
        QtCore.QSettings().setValue(constants.PREF_SEARCH_RADIUS, int(value))

    @property
    def variance(self):
        """
        reads & returns the search radius from the settings if no value was set 0.0 is returned
        :return: float
        """
        value = QtCore.QSettings().value(constants.PREF_VARIANCE)
        return float(value or 0.0)

    @variance.setter
    def variance(self, value):
        """
        sets the variance in the settings
        :param float value:
        :return: None
        """
        QtCore.QSettings().setValue(constants.PREF_VARIANCE, float(value))

    @property
    def aovs(self):
        """
        reads and returns the list of aov's from the settings
        :return: list
        """
        aovs = []
        settings = QtCore.QSettings()
        for index in range(settings.beginReadArray(constants.PREF_AOVS)):
            settings.setArrayIndex(index)
            aovs.append(settings.value(str(index)))

        return aovs

    @aovs.setter
    def aovs(self, value):
        """
        writes the given list of aovs to the settings
        :param list value:
        :return: None
        """
        settings = QtCore.QSettings()
        settings.beginWriteArray(constants.PREF_AOVS)
        for index, item in enumerate(value):
            settings.setArrayIndex(index)
            settings.setValue(str(index), item)

        settings.endArray()

    @property
    def inputs(self):
        """
        reads and returns the list of inputs from the settings
        :return: list
        """
        inputs = []
        settings = QtCore.QSettings()
        for index in range(settings.beginReadArray(constants.PREF_INPUTS)):
            settings.setArrayIndex(index)
            inputs.append(settings.value(str(index)))

        return inputs

    @inputs.setter
    def inputs(self, value):
        """
        writes the given list of inputs to the settings
        :param list value:
        :return: None
        """
        settings = QtCore.QSettings()
        settings.beginWriteArray(constants.PREF_INPUTS)
        for index, item in enumerate(value):
            settings.setArrayIndex(index)
            settings.setValue(str(index), item)

        settings.endArray()

    @property
    def output(self):
        """
        reads & returns the output from the settings
        :return: str
        """
        return QtCore.QSettings().value(constants.PREF_OUTPUT)

    @output.setter
    def output(self, value):
        """
        sets the output in the settings
        :param str value:
        :return: None
        """
        QtCore.QSettings().setValue(constants.PREF_OUTPUT, os.path.normpath(value))
