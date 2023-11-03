from PySide2 import QtWidgets, QtCore, QtGui
from copy import deepcopy

from . import objects
from . import commonFunctions
from . import defaults


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    __content: dict

    def __init__(self, object: objects._Object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

        self.__checkable = not isinstance(object, objects.Calculator)

        if self.__checkable:
            self.setCheckState(0, QtCore.Qt.Unchecked)
            self.__checked = QtCore.Qt.Unchecked
    
        self.__object = object

        self.setText(0, defaults.TypeToString[self.__object.type])

    @property
    def itemType(self):
        return self.__object.type

    @property
    def object(self):
        return self.__object

    @property
    def content(self):
        self.__content['opacity'] = self.__object.opacity
        return deepcopy(self.__content)
    
    @content.setter
    def content(self, content: dict):
        self.__content = deepcopy(content)
        if 'opacity' in self.__content:
            self.__object.opacity = self.__content['opacity']

    def isChecked(self):
        if self.__checkable:
            current_check_state = super().checkState(0)
            changed = current_check_state != self.__checked
            if changed:
                self.__checked = current_check_state
            return current_check_state, changed
        return False, False
