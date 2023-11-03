import PySide2.QtWidgets
import PySide2.QtCore
import PySide2.QtGui
import json
import os


class ColorMap:
    color_map: dict
    color_space: str
    name: str
    nan_color: tuple
    points: list
    range: tuple

    def __init__(self, filename=None, RGBPoints=None, scalarRange=None):
        if filename is not None:
            self.load(filename)
            self.restore()
        elif RGBPoints is not None and scalarRange is not None:
            self.color_space = None
            self.name = None
            self.nan_color = None
            self.points = RGBPoints
            a = scalarRange[1] - scalarRange[0]
            for i in range(0, len(self.points), 4):
                self.points[i] = a * RGBPoints[i] + scalarRange[0]
                for j in range(1, 4):
                    self.points[i + j] = str(int(self.points[i + j] * 255))
            self.range = scalarRange
        else:
            raise ValueError

    def load(self, filename):
        with open(filename, 'r') as file:
            self.color_map = json.loads(file.read())[0]

    def restore(self):
        self.color_space = self.color_map['ColorSpace']
        self.name = self.color_map['Name']
        self.nan_color = tuple(self.color_map['NanColor'])
        self.points = self.color_map['RGBPoints']
        for i in range(0, len(self.points), 4):
            for j in range(1, 4):
                self.points[i + j] = str(int(self.points[i + j] * 255))
        self.range = (0, 1)

    def setColors(self, colors):
        for i, color in enumerate(colors):
            for j in range(1, 4):
                self.points[i * 4 + j] = color[j - 1]

    def getColors(self):
        return [[self.points[i + j] for j in range(1, 4)] for i in range(0, len(self.points), 4)]

    def setPointPosition(self, index, position):
        self.points[index * 4] = position

    def getPointPosition(self, index):
        return self.points[index * 4]

    def setPoints(self, points):
        for i in range(0, len(self.points), 4):
            self.points[i] = points[int(i / 4)]

    def getPoints(self):
        return [self.points[i] for i in range(0, len(self.points), 4)]

    def setRange(self, left, right):
        if left == right:
            return
        points = self.getPoints()
        for i in range(len(points)):
            points[i] = (points[i] - self.range[0]) / (self.range[1] - self.range[0])
            points[i] = points[i] * (right - left) + left
        self.setPoints(points)
        self.range = left, right

    def getRange(self):
        return self.range

    def asStyleSheet(self):
        colors = ', '.join([f'stop: {(self.points[i] - self.range[0]) / (self.range[1] - self.range[0])} rgba({self.points[i + 1]}, {self.points[i + 2]}, {self.points[i + 3]}, 255)' for i in range(0, len(self.points), 4)])
        style_sheet = 'qlineargradient(x1: 0, x2: 1, colors)'
        style_sheet = style_sheet.replace('colors', colors)
        return style_sheet


class ColorMapWidget(PySide2.QtWidgets.QFrame):
    def __init__(self, func_then_changed):
        super().__init__()
        self.color_map = None
        self.func_then_changed = func_then_changed
        self.ellipse_radius = 10
        self.grab = -1
        self.setFixedHeight(30)

    def setColorMap(self, color_map):
        self.color_map = color_map
        self.updateStyleSheet()

    def getColorMap(self):
        return self.color_map

    def updateStyleSheet(self):
        if self.color_map:
            self.setStyleSheet(f'ColorMapWidget {{background-color: {self.color_map.asStyleSheet()}; border: 1px solid; border-radius: 2px}}')

    def drawPoints(self):
        if self.color_map is not None:
            size = self.size()
            black_pen = PySide2.QtGui.QPen(PySide2.QtCore.Qt.black)
            white_pen = PySide2.QtGui.QPen(PySide2.QtCore.Qt.white)
            painter = PySide2.QtGui.QPainter()
            painter.begin(self)
            painter.setRenderHint(PySide2.QtGui.QPainter.Antialiasing)
            for point in self.color_map.getPoints():
                point = PySide2.QtCore.QPointF((point - self.color_map.range[0]) / (self.color_map.range[1] - self.color_map.range[0]) * size.width(), size.height() / 2)
                painter.setPen(black_pen)
                painter.setBrush(PySide2.QtCore.Qt.black)
                painter.drawEllipse(point, self.ellipse_radius, self.ellipse_radius)
                painter.setPen(white_pen)
                painter.setBrush(PySide2.QtCore.Qt.white)
                painter.drawEllipse(point, self.ellipse_radius / 2 + 1, self.ellipse_radius / 2 + 1)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.drawPoints()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.color_map is not None:
            self.grab = -1
            pos = event.pos()
            for i, point in enumerate(self.color_map.getPoints()):
                size = self.size()
                x = ((point - self.color_map.range[0]) * size.width() / (self.color_map.range[1] - self.color_map.range[0]) - pos.x()) ** 2
                y = (size.height() / 2 - pos.y()) ** 2
                if x + y <= self.ellipse_radius ** 2:
                    self.grab = i
                    PySide2.QtWidgets.QToolTip.showText(event.globalPos(), str(point))
                    break

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.color_map is not None:
            self.grab = -1
            PySide2.QtWidgets.QToolTip.hideText()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.color_map is not None:
            if self.grab != -1:
                x = event.pos().x() / self.size().width() * (self.color_map.range[1] - self.color_map.range[0]) + self.color_map.range[0]
                x = self.color_map.range[1] if x > self.color_map.range[1] else x
                x = self.color_map.range[0] if x < self.color_map.range[0] else x
                self.color_map.setPointPosition(self.grab, x)
                self.updateStyleSheet()
                PySide2.QtWidgets.QToolTip.showText(event.globalPos(), str(x))
                if self.func_then_changed is not None:
                    self.func_then_changed()


color_maps = []
for root, directories, files in os.walk('Resources/ColorMaps'):
    color_maps.extend(files)
