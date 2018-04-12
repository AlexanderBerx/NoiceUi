try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ImportError:
    from Qt import QtWidgets, QtCore, QtGui


class NoiceModel(object):
    def __init__(self):
        self._aov_model = QtGui.QStandardItemModel()
        self._input_model = QtGui.QStandardItemModel()

    @property
    def aov_model(self):
        return self._aov_model

    @property
    def input_model(self):
        return self._input_model

    def add_aov(self, aov):
        item = QtGui.QStandardItem(aov)
        self._aov_model.appendRow(item)

    def remove_aov(self, index):
        """
        :param QtCore.QModelIndex index:
        :return:
        """
        self._aov_model.removeRow(index.row())

    def get_aov_names(self):
        """
        :return: list
        """
        names = []
        for index in range(self._aov_model.rowCount()):
            item = self._aov_model.item(index)  #type:QtGui.QStandardItem
            names.append(item.text())

        return names

    def add_input(self, input_):
        self._input_model.append(input_)

    def remove_input(self, index):
        """
        :param QtCore.QModelIndex index:
        :return:
        """
        self._input_model.removeRow(index.row())