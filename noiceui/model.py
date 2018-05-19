from Qt import QtGui


class NoiceModel(object):
    """
    NoiceModel, model class stores the aov's and inputs
    """

    def __init__(self):
        self._aov_model = QtGui.QStandardItemModel()
        self._input_model = QtGui.QStandardItemModel()

    @property
    def aov_model(self):
        """
        returns the aov model object
        :return: QtGui.QStandardItemModel
        """
        return self._aov_model

    @property
    def input_model(self):
        """
        returns the input model object
        :return: QtGui.QStandardItemModel
        """
        return self._input_model

    def add_aov(self, aov):
        """
        adds the given aov to the model
        :param str aov: name of the aov
        :return: None
        """
        item = QtGui.QStandardItem(aov)
        self._aov_model.appendRow(item)

    def remove_aov(self, index):
        """
        removes the given aov by the given model index row
        :param QtCore.QModelIndex index:
        :return: None
        """
        self._aov_model.removeRow(index.row())

    def get_aov_list(self):
        """
        gathers a list of all the names of the aov's in the model and returns it
        :return: list
        """
        names = []
        for index in range(self._aov_model.rowCount()):
            item = self._aov_model.item(index)  # type:QtGui.QStandardItem
            names.append(item.text())

        return names

    def add_input(self, input_):
        """
        adds input to the model
        :param str input_: path to the input
        :return: None
        """
        item = QtGui.QStandardItem(input_)
        self._input_model.appendRow(item)

    def remove_input(self, index):
        """
        removes the input by the row of the given index
        :param QtCore.QModelIndex index:
        :return: None
        """
        self._input_model.removeRow(index.row())

    def get_input_list(self):
        """
        gathers a list of all the names of the inputs's in the model and returns it
        :return: list
        """
        names = []
        for index in range(self._input_model.rowCount()):
            item = self._input_model.item(index)  # type:QtGui.QStandardItem
            names.append(item.text())

        return names
