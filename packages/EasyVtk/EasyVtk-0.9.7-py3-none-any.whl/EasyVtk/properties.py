from PySide2 import QtWidgets, QtCore, QtGui

from copy import deepcopy

import QtTables
from . import commonFunctions
from . import items
from . import commonClasses
from . import colorMaps


class Property(QtWidgets.QWidget):
    _item: items.TreeWidgetItem
    dataChanged = QtCore.Signal()
    removed = QtCore.Signal()
    customWidgetIndex = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._useParentColorTransferFunctionWidget = QtWidgets.QCheckBox('Use parent color map', self)
        self._colorMapWidget = commonClasses.ColorMapWidget(self)
        self._dataModeWidget = commonClasses.DataModeWidget(self)
        self._dataModeWidget.setParent(None)
        self._opacityWidget = commonClasses.OpacityWidget(self)
        self._colorMapPointsWidget = colorMaps.ColorMap.ColorMapWidget(self.colorMapPointChanged)

        self._useParentColorTransferFunctionWidget.stateChanged.connect(self.changeParentColorTransferFunction)
        self._colorMapWidget.currentIndexChanged.connect(self.colorMapComboBoxIndexChanged)
        self._dataModeWidget.currentArrayIndexChanged.connect(self.dataModeArrayComboBoxIndexChanged)
        self._dataModeWidget.currentIndexChanged.connect(self.dataModeComboBoxIndexChanged)
        self._opacityWidget.sliderMoved.connect(self.changeOpacity)

        self.removeButton = QtWidgets.QPushButton('Remove')
        self.textLabel = QtWidgets.QLabel('TEXT')

        first_layout = QtWidgets.QHBoxLayout()
        first_layout.addWidget(self.textLabel)
        first_layout.addWidget(self.removeButton)
        self.removeButton.clicked.connect(self.removed.emit)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.layout().addLayout(first_layout)
        self.layout().addWidget(self._opacityWidget)
        self.layout().addWidget(self._colorMapWidget)
        self.layout().addWidget(self._colorMapPointsWidget)
        self.layout().addWidget(self._useParentColorTransferFunctionWidget)

        self.layout().addStretch()
    
    def colorMapPointChanged(self):
        points = deepcopy(self._colorMapPointsWidget.getColorMap().points)
        zero = points[0]
        maximum = points[0]
        for i in range(0, len(points), 4):
            if points[i] > maximum:
                maximum = points[i]
            if points[i] < zero:
                zero = points[i]
            for j in range(1, 4):
                points[i + j] = int(points[i + j]) / 255
        for i in range(0, len(points), 4):
            points[i] = (zero - points[i]) / (zero - maximum)
        self._item.object.RGBPoints = points
        self.dataChanged.emit()
    
    def changeParentColorTransferFunction(self, state: QtCore.Qt.CheckState):
        self._item.object.useParentColorTransferFunction = state == QtCore.Qt.Checked
        self._colorMapWidget.colorMapComboBox.setCurrentIndex(self._item.object.colorMapIndex)
        self._colorMapPointsWidget.setColorMap(
            colorMaps.ColorMap.ColorMap(
                RGBPoints=list(self._item.object.RGBPoints),
                scalarRange=list(self._item.object.scalarRange)
            )
        )
        self.dataChanged.emit()
    
    def changeOpacity(self, value):
        self._item.object.opacity = value / 99
        self.dataChanged.emit()
    
    def colorMapComboBoxIndexChanged(self, index):
        name = colorMaps.colorMapsNames[index]
        RGBPoints = colorMaps.colorMaps[name]
        self._item.object.colorMapIndex = index
        self._item.object.RGBPoints = RGBPoints
        self.dataChanged.emit()
        self._colorMapPointsWidget.setColorMap(
            colorMaps.ColorMap.ColorMap(
                RGBPoints=list(self._item.object.RGBPoints),
                scalarRange=list(self._item.object.scalarRange)
            )
        )
    
    def dataModeArrayComboBoxIndexChanged(self, index):
        ...
    
    def dataModeComboBoxIndexChanged(self, index):
        self._item.object.setVectorModeTo(index)
        self.dataChanged.emit()

    @property
    def item(self):
        self._item.content = self.content
        return self._item

    @item.setter
    def item(self, item: items.TreeWidgetItem):
        self._item = item
        self._useParentColorTransferFunctionWidget.setChecked(self._item.object.useParentColorTransferFunction)
        self._colorMapWidget.colorMapComboBox.setCurrentIndex(self._item.object.colorMapIndex)
        self._dataModeWidget.arrays = self._item.object.arrays
        self._dataModeWidget.arrayIndex = self._item.object.arrayIndex
        self._dataModeWidget.dataMode = self._item.object.dataMode
        if self._item.object.dataMode == commonClasses.DataMode.vector:
            self._dataModeWidget.colorMode = self._item.object._colorMode + 1
        self._opacityWidget.setValue(int(self._item.object.opacity * 99))
        self.content = self._item.content
        self._colorMapPointsWidget.setColorMap(
            colorMaps.ColorMap.ColorMap(
                RGBPoints=list(self._item.object.RGBPoints),
                scalarRange=list(self._item.object.scalarRange)
            )
        )


class PVD(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.maxTime = QtWidgets.QLabel('0')
        maxTimeLabel = QtWidgets.QLabel('Max time:')
        maxTimeLabel.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

        maxTimeLayout = QtWidgets.QHBoxLayout()
        maxTimeLayout.addWidget(maxTimeLabel)
        maxTimeLayout.addWidget(self.maxTime)

        previousPushButton = QtWidgets.QPushButton('<')
        self.timeLineEdit = QtWidgets.QLineEdit()
        nextPushButton = QtWidgets.QPushButton('>')

        time_layout = QtWidgets.QHBoxLayout()
        time_layout.addWidget(QtWidgets.QLabel('Time:'))
        time_layout.addWidget(previousPushButton)
        time_layout.addWidget(self.timeLineEdit)
        time_layout.addWidget(nextPushButton)

        previousPushButton.clicked.connect(self.previousTime)
        self.timeLineEdit.editingFinished.connect(self.setTime)
        nextPushButton.clicked.connect(self.nextTime)

        self.textLabel.setText('PVD')
        self.removeButton.setParent(None)
        self.layout().insertLayout(self.customWidgetIndex, time_layout)
        self.layout().insertLayout(self.customWidgetIndex, maxTimeLayout)

        self._useParentColorTransferFunctionWidget.setVisible(False)
    
    def previousTime(self):
        self._item.object.time -=1
        self.timeLineEdit.setText(str(self._item.object.time))
        self.dataChanged.emit()
    
    def setTime(self):
        self._item.object.time = int(self.timeLineEdit.text())
        self.timeLineEdit.setText(str(self._item.object.time))
        self.dataChanged.emit()
    
    def nextTime(self):
        self._item.object.time += 1
        self.timeLineEdit.setText(str(self._item.object.time))
        self.dataChanged.emit()
    
    @property
    def content(self):
        return {
            'time': self.timeLineEdit.text()
        }
    
    @content.setter
    def content(self, content):
        self.timeLineEdit.setText(content['time'])
        self.maxTime.setText(str(self._item.object._maxTime))


class Cut(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        normalXEditLine = QtWidgets.QLineEdit()
        normalYEditLine = QtWidgets.QLineEdit()
        normalZEditLine = QtWidgets.QLineEdit()

        normalLayout = QtWidgets.QHBoxLayout()
        normalLayout.addWidget(QtWidgets.QLabel('Normal:'))
        normalLayout.addWidget(normalXEditLine)
        normalLayout.addWidget(normalYEditLine)
        normalLayout.addWidget(normalZEditLine)

        originLayout = QtWidgets.QHBoxLayout()

        originXEditLine = QtWidgets.QLineEdit()
        originYEditLine = QtWidgets.QLineEdit()
        originZEditLine = QtWidgets.QLineEdit()

        originLayout = QtWidgets.QHBoxLayout()
        originLayout.addWidget(QtWidgets.QLabel('Origin:'))
        originLayout.addWidget(originXEditLine)
        originLayout.addWidget(originYEditLine)
        originLayout.addWidget(originZEditLine)

        self.textLabel.setText('Cut')
        self.layout().insertLayout(self.customWidgetIndex, originLayout)
        self.layout().insertLayout(self.customWidgetIndex, normalLayout)

        self.normalEditLines = (
            normalXEditLine,
            normalYEditLine,
            normalZEditLine,
        )

        self.originEditLines = (
            originXEditLine,
            originYEditLine,
            originZEditLine,
        )

        for normalEditLine in self.normalEditLines:
            normalEditLine.editingFinished.connect(self.normalEditingFinished)
        
        for originEditLine in self.originEditLines:
            originEditLine.editingFinished.connect(self.originEditingFinished)
    
    def normalEditingFinished(self):
        self._item.object.normal = commonFunctions.replaceType(self.normal, float)
        self.dataChanged.emit()
    
    def originEditingFinished(self):
        self._item.object.origin = commonFunctions.replaceType(self.origin, float)
        self.dataChanged.emit()

    @property
    def normal(self):
        return tuple(normalEditLine.text() for normalEditLine in self.normalEditLines)
    
    @normal.setter
    def normal(self, normal):
        for normalEditLine, value in zip(self.normalEditLines, normal):
            normalEditLine.setText(str(value))

    @property
    def origin(self):
        return tuple(originEditLine.text() for originEditLine in self.originEditLines)
    
    @origin.setter
    def origin(self, origin):
        for originEditLine, value in zip(self.originEditLines, origin):
            originEditLine.setText(str(value))
    
    @property
    def content(self):
        return {
            'normal': self.normal,
            'origin': self.origin
        }
    
    @content.setter
    def content(self, content):
        self.normal = content['normal']
        self.origin = content['origin']


class Isoline(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.numberOfLineEditLine = QtWidgets.QLineEdit(self)

        numberLayout = QtWidgets.QHBoxLayout()
        numberLayout.addWidget(QtWidgets.QLabel('Number of lines:'))
        numberLayout.addWidget(self.numberOfLineEditLine)

        self.showLabelsButton = QtWidgets.QCheckBox('Show labels')

        self.textLabel.setText('Isoline')
        self.layout().insertWidget(self.customWidgetIndex, self.showLabelsButton)
        self.layout().insertLayout(self.customWidgetIndex, numberLayout)

        self.numberOfLineEditLine.editingFinished.connect(self.changeNumberOfLines)
        self.showLabelsButton.stateChanged.connect(self.showLabelsToggled)
    
    def showLabelsToggled(self, state):
        self._item.object.showLabels = state == QtCore.Qt.Checked
        self.dataChanged.emit()
    
    def changeNumberOfLines(self):
        number_of_lines = int(self.numberOfLineEditLine.text())
        self._item.object.numberOfLines = number_of_lines
        self.dataChanged.emit()

    @property
    def content(self):
        return {
            'numberOfLines': self.numberOfLineEditLine.text(),
            'showLabels': self.showLabelsButton.checkState() == QtCore.Qt.Checked
        }
    
    @content.setter
    def content(self, content):
        self.numberOfLineEditLine.setText(str(content['numberOfLines']))
        self.showLabelsButton.setCheckState(QtCore.Qt.Checked if content['showLabels'] else QtCore.Qt.Unchecked)


class Clip(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        normalXEditLine = QtWidgets.QLineEdit()
        normalYEditLine = QtWidgets.QLineEdit()
        normalZEditLine = QtWidgets.QLineEdit()

        normalLayout = QtWidgets.QHBoxLayout()
        normalLayout.addWidget(QtWidgets.QLabel('Normal:'))
        normalLayout.addWidget(normalXEditLine)
        normalLayout.addWidget(normalYEditLine)
        normalLayout.addWidget(normalZEditLine)

        originLayout = QtWidgets.QHBoxLayout()

        originXEditLine = QtWidgets.QLineEdit()
        originYEditLine = QtWidgets.QLineEdit()
        originZEditLine = QtWidgets.QLineEdit()

        originLayout = QtWidgets.QHBoxLayout()
        originLayout.addWidget(QtWidgets.QLabel('Origin:'))
        originLayout.addWidget(originXEditLine)
        originLayout.addWidget(originYEditLine)
        originLayout.addWidget(originZEditLine)

        self.invertButton = QtWidgets.QCheckBox('Invert', self)
        
        self.textLabel.setText('Clip')
        self.layout().insertWidget(self.customWidgetIndex, self.invertButton)
        self.layout().insertLayout(self.customWidgetIndex, originLayout)
        self.layout().insertLayout(self.customWidgetIndex, normalLayout)

        self.normalEditLines = (
            normalXEditLine,
            normalYEditLine,
            normalZEditLine,
        )

        self.originEditLines = (
            originXEditLine,
            originYEditLine,
            originZEditLine,
        )

        for normalEditLine in self.normalEditLines:
            normalEditLine.editingFinished.connect(self.normalEditingFinished)
        
        for originEditLine in self.originEditLines:
            originEditLine.editingFinished.connect(self.originEditingFinished)

        self.invertButton.stateChanged.connect(self.invertChanged)
    
    def invertChanged(self, state: QtCore.Qt.CheckState):
        self._item.object.invert = state == QtCore.Qt.Checked
        self.dataChanged.emit()

    def normalEditingFinished(self):
        self._item.object.normal = commonFunctions.replaceType(self.normal, float)
        self.dataChanged.emit()
    
    def originEditingFinished(self):
        self._item.object.origin = commonFunctions.replaceType(self.origin, float)
        self.dataChanged.emit()

    @property
    def normal(self):
        return tuple(normalEditLine.text() for normalEditLine in self.normalEditLines)
    
    @normal.setter
    def normal(self, normal):
        for normalEditLine, value in zip(self.normalEditLines, normal):
            normalEditLine.setText(str(value))

    @property
    def origin(self):
        return tuple(originEditLine.text() for originEditLine in self.originEditLines)
    
    @origin.setter
    def origin(self, origin):
        for originEditLine, value in zip(self.originEditLines, origin):
            originEditLine.setText(str(value))
    
    @property
    def content(self):
        return {
            'invert': self.invertButton.isChecked(),
            'normal': self.normal,
            'origin': self.origin
        }

    @content.setter
    def content(self, content):
        self.invertButton.setChecked(content['invert'])
        self.normal = content['normal']
        self.origin = content['origin']


class Threshold(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.invertButton = QtWidgets.QCheckBox('Invert', self)
        
        leftRangeLineEdit = QtWidgets.QLineEdit()
        rightRangeLineEdit = QtWidgets.QLineEdit()

        self.resetRangeButton = QtWidgets.QPushButton('Reset')

        rangeLayout = QtWidgets.QHBoxLayout()
        rangeLayout.addWidget(leftRangeLineEdit)
        rangeLayout.addWidget(rightRangeLineEdit)
        rangeLayout.addWidget(self.resetRangeButton)

        self.rangeEditLines = (
            leftRangeLineEdit,
            rightRangeLineEdit
        )

        self.textLabel.setText('Threshold')
        self.layout().insertWidget(self.customWidgetIndex, self.invertButton)
        self.layout().insertLayout(self.customWidgetIndex, rangeLayout)

        for rangeEditLine in self.rangeEditLines:
            rangeEditLine.editingFinished.connect(self.rangeChanged)
        self.resetRangeButton.clicked.connect(self.resetRange)
        self.invertButton.stateChanged.connect(self.invertChanged)
    
    def resetRange(self):
        self._item.object.resetRange()
        self.range = commonFunctions.replaceType(self._item.object.range, str)
        self.dataChanged.emit()
    
    def invertChanged(self, state: QtCore.Qt.CheckState):
        self._item.object.invert = state == QtCore.Qt.Checked
        self.dataChanged.emit()
    
    def rangeChanged(self):
        self.__range = commonFunctions.replaceType(self.range, float)
        self._item.object.range = self.__range
        self.dataChanged.emit()

    @property
    def range(self):
        return tuple(rangeEditLine.text() for rangeEditLine in self.rangeEditLines)
    
    @range.setter
    def range(self, range):
        for rangeEditLine, value in zip(self.rangeEditLines, range):
            rangeEditLine.setText(str(value))
    
    @property
    def content(self):
        return {
            'invert': self.invertButton.isChecked(),
            'range': self.range
        }

    @content.setter
    def content(self, content):
        self.invertButton.setChecked(content['invert'])
        self.range = content['range']


class Calculator(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._useParentColorTransferFunctionWidget.setParent(None)
        self._colorMapWidget.setParent(None)
        self._dataModeWidget.setParent(None)
        self._opacityWidget.setParent(None)
        self._useParentColorTransferFunctionWidget.deleteLater()
        self._colorMapWidget.deleteLater()
        self._dataModeWidget.deleteLater()
        self._opacityWidget.deleteLater()

        self.textLabel.setText('Calculator')

        self.table = QtTables.TableWidget.Table(
            self,
            (
                QtTables.Creators.lineEditCreator(validator=QtTables.Validators.negative_double_validator),
                QtTables.Creators.lineEditCreator(validator=QtTables.Validators.negative_double_validator),
                QtTables.Creators.lineEditCreator(validator=QtTables.Validators.negative_double_validator),
                QtTables.Creators.lineEditCreator(),
            ),
            horizontal_labels=('X', 'Y', 'Z', 'Times')
        )

        self.layout().insertWidget(1, self.table)

    @property
    def content(self):
        return {
            'table': self.table.getAllContents().copy()
        }

    @content.setter
    def content(self, content):
        self.table.setAllContents(content['table'].copy())


class Outline(Property):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._useParentColorTransferFunctionWidget.setParent(None)
        self._colorMapWidget.setParent(None)
        self._dataModeWidget.setParent(None)
        self._opacityWidget.setParent(None)
        self._colorMapPointsWidget.setParent(None)
        self.textLabel.setText('Outline')
