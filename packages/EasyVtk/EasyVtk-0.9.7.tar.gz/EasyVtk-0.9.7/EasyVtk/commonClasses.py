from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum

from . import commonFunctions
from . import colorMaps


class DataMode(Enum):
    nan = 0
    scalar = 1
    vector = 2


class Type(Enum):
    pvd = 0
    cut = 1
    isoline = 2
    clip = 3
    threshold = 4
    calculator = 5
    outline = 6
    another = 7


class OpacityWidget(QtWidgets.QWidget):
    sliderMoved = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setValue(99)

        self.slider.sliderMoved.connect(self.sliderMoved.emit)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(QtWidgets.QLabel('Opacity', self))
        self.layout().addWidget(self.slider)
    
    def setValue(self, value):
        self.slider.setValue(value)


class ColorMapWidget(QtWidgets.QWidget):
    currentIndexChanged = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.colorMapComboBox = QtWidgets.QComboBox(self)
        self.colorMapWidget = None

        self.colorMapComboBox.addItems(colorMaps.colorMapsNames)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(QtWidgets.QLabel('Color map', self))
        self.layout().addWidget(self.colorMapComboBox)

        self.colorMapComboBox.currentIndexChanged.connect(self.currentIndexChanged.emit)


class DataModeWidget(QtWidgets.QWidget):
    __arrays: tuple
    __dataMode: DataMode
    __colorMode: int
    currentArrayIndexChanged = QtCore.Signal(int)
    currentIndexChanged = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        title = QtWidgets.QLabel('Array and data mode', self)
        title.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        self.__arraysComboBox = QtWidgets.QComboBox(self)
        self.__dataModeComboBox = QtWidgets.QComboBox(self)
        self.__dataModeComboBox.addItems(('Magnitude', 'X', 'Y', 'Z'))

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.__arraysComboBox)
        layout.addWidget(self.__dataModeComboBox)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(title)
        self.layout().addLayout(layout)
    
        self.__arraysComboBox.currentIndexChanged.connect(self.currentArrayIndexChanged.emit)
        self.__dataModeComboBox.currentIndexChanged.connect(self.currentIndexChanged.emit)
    
    @property
    def arrays(self):
        return self.__arrays
    
    @arrays.setter
    def arrays(self, arrays):
        self.__arrays = arrays
        self.__arraysComboBox.clear()
        self.__arraysComboBox.addItems(self.__arrays)
    
    @property
    def arrayIndex(self):
        return self.__arraysComboBox.currentIndex()
    
    @arrayIndex.setter
    def arrayIndex(self, arrayIndex):
        self.__arraysComboBox.setCurrentIndex(arrayIndex)
    
    @property
    def dataMode(self):
        return self.__dataMode
    
    @dataMode.setter
    def dataMode(self, dataMode):
        self.__dataMode = dataMode
        if self.__dataMode == DataMode.vector:
            self.__dataModeComboBox.setEnabled(True)
        else:
            self.__dataModeComboBox.setDisabled(True)
    
    @property
    def colorMode(self):
        return self.__colorMode
    
    @colorMode.setter
    def colorMode(self, colorMode):
        self.__colorMode = colorMode
        self.__dataModeComboBox.setCurrentIndex(colorMode)
