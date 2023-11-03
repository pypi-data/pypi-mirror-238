import vtk
from os.path import exists
from copy import deepcopy

from . import commonFunctions
from . import commonClasses
from . import colorMaps


class _Object(vtk.vtkActor):
    __dataMode: commonClasses.DataMode
    _type: commonClasses.Type
    _colorTransferFunction: vtk.vtkColorTransferFunction
    _colorTransferFunctionStock: vtk.vtkColorTransferFunction = None
    __childs: list
    _parent = None
    _colorMode: int
    _arrays: tuple
    _arrayIndex: int
    _scalarRange: tuple
    _scalarRangeMagnitude: tuple
    _scalarRangeComponent: tuple
    _hasScalarBarActor = False
    _showScalarBarActor = False
    _RGBPoints = (
        0.0, 0.23137254902000001, 0.298039215686, 0.75294117647100001,
        0.5, 0.86499999999999999, 0.86499999999999999, 0.86499999999999999,
        1.0, 0.70588235294099999, 0.015686274509800001, 0.149019607843
    )
    _title = ''
    _useParentColorTransferFunction = False
    _colorMapIndex = 0
    _hasColors = True
    contentToSave = None

    @classmethod
    def restoreFromSaveData(saveData):
        ...

    @property
    def colorMapIndex(self):
        return self._parent.colorMapIndex if self.useParentColorTransferFunction else  self._colorMapIndex
    
    @colorMapIndex.setter
    def colorMapIndex(self, colorMapIndex):
        if self.useParentColorTransferFunction:
            self._parent.colorMapIndex = colorMapIndex
        else:
            self._colorMapIndex = colorMapIndex

    @property
    def childs(self):
        return tuple(self.__childs)

    @property
    def output(self):
        return self._mainFunction.GetOutput()

    @property
    def outputPort(self):
        return self._mainFunction.GetOutputPort()
    
    @property
    def dataMode(self):
        return self.__dataMode
    
    @property
    def type(self):
        return self._type
    
    @property
    def arrays(self):
        return self._arrays
    
    @property
    def arrayIndex(self):
        return self._arrayIndex
    
    @arrayIndex.setter
    def arrayIndex(self, arrayIndex):
        self._arrayIndex = arrayIndex
        self.changeArray()
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        if self._hasScalarBarActor:
            self.scalarBarActor.SetTitle(self._title)
    
    @property
    def useParentColorTransferFunction(self):
        return self._useParentColorTransferFunction
    
    @useParentColorTransferFunction.setter
    def useParentColorTransferFunction(self, useParentColorTransferFunction):
        if self._parent is not None and self._useParentColorTransferFunction != useParentColorTransferFunction:
            self._useParentColorTransferFunction = useParentColorTransferFunction
            if self._useParentColorTransferFunction:
                self._colorTransferFunctionStock, self._colorTransferFunction = self._colorTransferFunction, self._parent._colorTransferFunction
            else:
                self._colorTransferFunction, self._colorTransferFunctionStock = self._colorTransferFunctionStock, None
            self._mapper.SetLookupTable(self._colorTransferFunction)
            if self._hasScalarBarActor:
                self.scalarBarActor.SetLookupTable(self._colorTransferFunction)
    
    @property
    def opacity(self):
        return self.GetProperty().GetOpacity()
    
    @opacity.setter
    def opacity(self, opacity):
        self.GetProperty().SetOpacity(opacity)
    
    @property
    def RGBPoints(self):
        return self._parent._RGBPoints if self.useParentColorTransferFunction else self._RGBPoints

    @RGBPoints.setter
    def RGBPoints(self, RGBPoints):
        if self.useParentColorTransferFunction:
            self._parent._RGBPoints = RGBPoints
        else:
            self._RGBPoints = RGBPoints
        self._rescaleColorFunction()
    
    @property
    def colorMode(self):
        return self._colorMode
    
    @colorMode.setter
    def colorMode(self, colorMode):
        self._colorMode = colorMode
    
    @property
    def scalarRange(self):
        if self.useParentColorTransferFunction:
            return self._parent.scalarRange
        self._scalarRange = self.output.GetScalarRange()
        if self.__dataMode == commonClasses.DataMode.scalar:
            return self._scalarRange
        elif self.__dataMode == commonClasses.DataMode.vector:
            if self.colorMode == -1:
                return self._scalarRangeMagnitude
            else:
                return self._scalarRangeComponent[self.colorMode]
        else:
            return 0, 1
    
    def addChild(self, child):
        self.__childs.append(child)

    def removeChild(self, child):
        assert child in self.__childs, f'{type(self)} hasn\'t child {type(child)}'
        index = self.childs.index(child)
        obj = self.__childs.pop(index)
        del obj
 
    def update(self):
        self._mainFunction.Update()

    def build(self):
        if self._hasColors:
            if not isinstance(self, PVD):
                if self not in self._parent.childs:
                    self._parent.addChild(self)
                self._arrays = self._parent.arrays
                self._arrayIndex = self._parent.arrayIndex
            else:
                self._arrays = tuple(self._mainFunction.GetPointArrayName(i) for i in range(self._mainFunction.GetNumberOfPointArrays()))
                self._arrayIndex = 0

        self.__childs = list()

        if not isinstance(self, Isoline):
            self._mapper: vtk.vtkDataSetMapper = commonFunctions.create_data_set_mapper(self._mainFunction)
            self.SetMapper(self._mapper)

        numberOfComponents = self.output.GetPointData().GetNumberOfComponents()
        if numberOfComponents == 0:
            self.__dataMode = commonClasses.DataMode.nan
            return
        elif numberOfComponents == 1:
            self.__dataMode = commonClasses.DataMode.scalar
            self._scalarRange = self.output.GetScalarRange()
            self._colorTransferFunction: vtk.vtkColorTransferFunction = commonFunctions.setUpCtf(scalarRange=self._scalarRange, RGBPoints=self._RGBPoints)
        elif numberOfComponents == 3:
            self.__dataMode = commonClasses.DataMode.vector
            self._scalarRangeMagnitude = self.output.GetPointData().GetVectors().GetRange(-1)
            vectors = self.output.GetPointData().GetVectors()
            self._scalarRangeComponent = tuple(vectors.GetRange(i) for i in range(3))
            self._colorTransferFunction: vtk.vtkColorTransferFunction = commonFunctions.setUpCtf(scalarRange=self._scalarRangeMagnitude, RGBPoints=self._RGBPoints)
            self._mapper.SetScalarModeToUsePointFieldData()
            self.setVectorModeToMagnitude()
        elif numberOfComponents == 4:
            self.__dataMode = commonClasses.DataMode.nan
            return
        else:
            raise ValueError(f'Unexpected number of components: {numberOfComponents}')
        self._mapper.SetLookupTable(self._colorTransferFunction)
        self._mapper.InterpolateScalarsBeforeMappingOn()
        if colorMaps.colorMapsNames:
            self.colorMapIndex = 0
            self.RGBPoints = colorMaps.colorMaps[colorMaps.colorMapsNames[0]]
    
    def buildScalarBarActor(self):
        assert hasattr(self, '_colorTransferFunction'), f'{self.type} hasn\'t color transfer function, {self.dataMode=}'
        self._hasScalarBarActor = True
        self.scalarBarActor = ScalarBarActor()
        self.scalarBarActor.SetLookupTable(self._colorTransferFunction)
    
    def _rescaleColorFunction(self, scalarRange=None):
        if self.useParentColorTransferFunction:
            self._parent._rescaleColorFunction()
            return
        if scalarRange is None:
            self._scalarRange = self.output.GetScalarRange()
            if self.__dataMode == commonClasses.DataMode.scalar:
                scalarRange = self._scalarRange
            elif self.__dataMode == commonClasses.DataMode.vector:
                if self.colorMode == -1:
                    scalarRange = self._scalarRangeMagnitude
                else:
                    scalarRange = self._scalarRangeComponent[self.colorMode]
            else:
                scalarRange = 0, 1
        commonFunctions.remakeRGBPoints(self._colorTransferFunction, scalarRange, self._RGBPoints)
    
    def setVectorModeTo(self, index: int):
        if index == 0:
            self.setVectorModeToMagnitude()
        else:
            self.setVectorModeToComponent(index - 1)

    def setVectorModeToMagnitude(self):
        if self.useParentColorTransferFunction:
            self._parent.setVectorModeToMagnitude()
        else:
            self.isVector()
            self.colorMode = -1
            self._colorTransferFunction.SetVectorModeToMagnitude()
            self._mapper.SelectColorArray(self._arrays[self._arrayIndex])
            self._rescaleColorFunction()
        if self._hasScalarBarActor:
            self.scalarBarActor.SetComponentTitle('Magnitude')
    
    def setVectorModeToComponent(self, index: int):
        if self.useParentColorTransferFunction:
            self.colorMode = index
            self._parent.setVectorModeToComponent(index)
        else:
            self.isVector()
            self.colorMode = index
            self._colorTransferFunction.SetVectorModeToComponent()
            self._colorTransferFunction.SetVectorComponent(index)
            self._mapper.ColorByArrayComponent(self._arrays[self._arrayIndex], self.colorMode)
            self._rescaleColorFunction()
        if self._hasScalarBarActor:
            self.scalarBarActor.SetComponentTitle(componentIndexToStr[self.colorMode])

    def changeArray(self):
        if self.colorMode == -1:
            self._mapper.SelectColorArray(self._arrays[self._arrayIndex])
        else:
            self._mapper.ColorByArrayComponent(self._arrays[self._arrayIndex], self.colorMode)

    def isVector(self):
        assert self.__dataMode == commonClasses.DataMode.vector, f'{type(self)}.__dataMode != DataMode.vector'


class ScalarBarActor(vtk.vtkScalarBarActor):
    def __init__(self):
        self.hasInteractor = False
        self.hasTextProperty = False
        self.scalarBarWidgetOn = False

        self.textProperty = vtk.vtkTextProperty()
        self.textProperty.SetFontSize(14)
        # self.textProperty.SetColor(0, 0, 0)
        self.textProperty.SetBold(False)
        self.textProperty.SetItalic(False)
        self.textProperty.SetShadow(False)

        self.SetLabelTextProperty(self.textProperty)
        self.SetTitleTextProperty(self.textProperty)
        self.SetBarRatio(0.2)
        self.UnconstrainedFontSizeOn()

        self.scalarBarWidget = vtk.vtkScalarBarWidget()
        self.scalarBarWidget.SetScalarBarActor(self)
        # self.scalarBarWidget.GetBorderRepresentation().SetBorderColor(0, 0, 0)
        self.scalarBarWidget.GetScalarBarRepresentation().ProportionalResizeOn()
    
    def setLightTheme(self):
        self.textProperty.SetColor(0, 0, 0)
        self.scalarBarWidget.GetBorderRepresentation().SetBorderColor(0, 0, 0)
    
    def setDarkTheme(self):
        self.textProperty.SetColor(1, 1, 1)
        self.scalarBarWidget.GetBorderRepresentation().SetBorderColor(1, 1, 1)
    
    @property
    def interactor(self):
        return self.scalarBarWidget.GetInteractor()
    
    @interactor.setter
    def interactor(self, interactor):
        self.hasInteractor = True
        self.scalarBarWidget.SetInteractor(interactor)
    
    @property
    def textProperty(self):
        return self.GetLabelTextProperty()

    @textProperty.setter
    def textProperty(self, textProperty):
        self.hasTextProperty = True
        self.SetLabelTextProperty(textProperty)
        self.SetTitleTextProperty(textProperty)


class Outline(vtk.vtkCubeAxesActor):
    __name__ = 'Outline'

    def __init__(self, parent: _Object):
        self._parent = parent

        self._title = ''
        self._type = commonClasses.Type.outline
        self._hasScalarBarActor = False
        self._showScalarBarActor = False
        self.useParentColorTransferFunction = False
        self.colorMapIndex = False
        self.arrays = ['None']
        self.arrayIndex = 0
        self.dataMode = commonClasses.DataMode.nan
        self._colorMode = False
        self.opacity = 1
        self.RGBPoints = []
        self.scalarRange = (0, 1)

        self.bounds = [0, 0, 0, 0, 0, 0]
        self._parent.output.GetBounds(self.bounds)

        self.SetUseTextActor3D(True)
        self.SetBounds(self.bounds)

        # self.setColor((0, 0, 0))
    
    def setLightTheme(self):
        self.setColor((0, 0, 0))
    
    def setLightTheme(self):
        self.setColor((1, 1, 1))

    @property
    def type(self):
        return self._type
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title

    def update(self, eps=1e-6):
        self._parent.GetBounds(self.bounds)
        for i in range(3):
            s = self.bounds[i * 2 + 1] - self.bounds[i * 2]
            if abs(s) < eps:
                self.bounds[i * 2] += s / 2
                self.bounds[i * 2 + 1] -= s / 2
        self.SetBounds(self.bounds)

    def setColor(self, color):
        self.GetTitleTextProperty(0).SetColor(color)
        self.GetLabelTextProperty(0).SetColor(color)

        self.GetTitleTextProperty(1).SetColor(color)
        self.GetLabelTextProperty(1).SetColor(color)

        self.GetTitleTextProperty(2).SetColor(color)
        self.GetLabelTextProperty(2).SetColor(color)

        self.GetXAxesLinesProperty().SetColor(color)
        self.GetYAxesLinesProperty().SetColor(color)
        self.GetZAxesLinesProperty().SetColor(color)


class PVD(_Object):
    __name__ = 'PVD'

    def __init__(self, filename: str, timeStep: str, piles, piles_settings, startTime):
        assert filename.endswith('.pvd'), 'Unsupported type of PVD filename'

        self.contentToSave = {'filename': filename, 'timeStep': timeStep, 'piles': piles, 'piles_settings': piles_settings, 'startTime': startTime}

        self._type = commonClasses.Type.pvd

        filename = filename.replace('\\', '/')
        self._filenames = []

        self._directoryName = '/'.join(filename.split('/')[:-1])

        treeReader = vtk.vtkXMLTreeReader()
        treeReader.SetFileName(filename)
        treeReader.Update()
        treeReader.GetOutput().GetVertexData().SetActivePedigreeIds('file')

        self.__time = 0
        self._maxTime = treeReader.GetOutput().GetVertexData().GetPedigreeIds().GetNumberOfValues()
        for value in range(self._maxTime):
            in_filename = treeReader.GetOutput().GetVertexData().GetPedigreeIds().GetValue(value)
            if in_filename and exists(f'{self._directoryName}/{in_filename}'):
                self._filenames.append(in_filename)
        self._maxTime = len(self._filenames)

        self.__reader = vtk.vtkXMLUnstructuredGridReader()
        self.__reader.SetFileName(self._directoryName + '/' + self._filenames[self.__time])
        self.__reader.Update()

        self.build()
        self.buildScalarBarActor()

        if self.dataMode == commonClasses.DataMode.vector:
            self.scalarBarActor.SetComponentTitle('Magnitude')

        self._useParentColorTransferFunction = False
    
    @classmethod
    def restoreFromSaveData(cls, filename, timeStep, piles, piles_settings, startTime):
        instance = cls(filename, timeStep, piles, piles_settings, startTime)
        return instance

    @property
    def _mainFunction(self):
        return self.__reader

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time: int):
        if 0 <= time <= self._maxTime - 1:
            self.__time = time
        elif 0 > time:
            self.__time = 0
        elif self._maxTime - 1 < time:
            self.__time = self._maxTime - 1

        self._mainFunction.SetFileName(self._directoryName + '/' + self._filenames[self.__time])

        self.update()
        self._rescaleColorFunction()
        self.contentToSave['timeStep'] = self.__time


class Cut(_Object):
    __name__ = 'Cut'

    def __init__(self, parent: _Object):
        super().__init__()

        self._type = commonClasses.Type.cut

        self._parent = parent

        x_min, x_max, y_min, y_max, z_min, z_max = self._parent.output.GetBounds()
        self.__origin = (x_max + x_min) / 2, (y_max + y_min) / 2, (z_max + z_min) / 2
        self.__normal = (0, 0, 1)

        self.contentToSave = {
            'origin': deepcopy(self.__origin),
            'normal': deepcopy(self.__normal)
        }
    
        self.__cutterFunc = vtk.vtkPlane()
        self.__cutterFunc.SetOrigin(*self.__origin)
        self.__cutterFunc.SetNormal(*self.__normal)

        self.__cutter = vtk.vtkCutter()
        self.__cutter.SetCutFunction(self.__cutterFunc)
        self.__cutter.SetInputConnection(self._parent.outputPort)

        self.__stripper = vtk.vtkStripper()
        self.__stripper.SetInputConnection(self.__cutter.GetOutputPort())
        self.__stripper.Update()

        self.build()
        self.buildScalarBarActor()
    
    @classmethod
    def restoreFromSaveData(cls, parent, origin, normal):
        instance = cls(parent)
        instance.origin = origin
        instance.normal = normal
        return instance

    @property
    def _mainFunction(self):
        return self.__stripper
    
    @property
    def normal(self):
        return self.__normal
    
    @normal.setter
    def normal(self, normal: tuple):
        self.__normal = normal
        self.__cutterFunc.SetNormal(*self.__normal)
        self.contentToSave['normal'] = deepcopy(self.__normal)

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin: tuple):
        self.__origin = origin
        self.__cutterFunc.SetOrigin(*self.__origin)
        self.contentToSave['origin'] = deepcopy(self.__origin)


class Isoline(_Object):
    __name__ = 'Isoline'

    def __init__(self, parent: _Object):
        super().__init__()

        self._type = commonClasses.Type.isoline

        self._parent = parent
        self.__numberOfLines = 10
        self.__labelColor = (0, 0, 0)
        self.__isolineColor = (1, 1, 1)
        self.__showLabels = False

        self.contentToSave = {
            'numberOfLines': deepcopy(self.__numberOfLines),
            'labelColor': deepcopy(self.__labelColor),
            'isolineColor': deepcopy(self.__isolineColor),
            'showLabels': deepcopy(self.__showLabels)
        }

        self.__contour = vtk.vtkContourFilter()
        self.__contour.SetInputConnection(self._parent.outputPort)
        self.__contour.GenerateValues(self.__numberOfLines, self._parent.output.GetScalarRange())
        self.__contour.Update()

        stripper = vtk.vtkStripper()
        stripper.SetInputConnection(self.__contour.GetOutputPort())
        stripper.Update()

        self._mapper = vtk.vtkLabeledContourMapper()
        self._mapper.SetInputConnection(stripper.GetOutputPort())
        self._mapper.GetPolyDataMapper().ScalarVisibilityOff()
        self._mapper.LabelVisibilityOff()
    
        self._mapper.GetTextProperties().GetItem(0).SetColor(*self.__labelColor)  # values color
        self.GetProperty().SetColor(*self.__isolineColor)  # isolines color

        self.SetMapper(self._mapper)

        self.build()
    
    @classmethod
    def restoreFromSaveData(cls, parent, numberOfLines, labelColor, isolineColor, showLabels):
        instance = cls(parent)
        instance.numberOfLines = numberOfLines
        instance.labelColor = labelColor
        instance.isolineColor = isolineColor
        instance.showLabels = showLabels
        return instance
    
    @property
    def _mainFunction(self):
        return self.__contour
    
    @property
    def showLabels(self):
        return self.__showLabels
    
    @showLabels.setter
    def showLabels(self, showLabels):
        self.__showLabels = showLabels
        if self.__showLabels:
            self._mapper.LabelVisibilityOn()
        else:
            self._mapper.LabelVisibilityOff()
        self.contentToSave['showLabels'] = deepcopy(self.__showLabels)

    @property
    def numberOfLines(self):
        return self.__numberOfLines
    
    @numberOfLines.setter
    def numberOfLines(self, numberOfLines):
        self.__numberOfLines = numberOfLines
        self.__contour.GenerateValues(self.__numberOfLines, self._parent.output.GetScalarRange())
        self.contentToSave['numberOfLines'] = deepcopy(self.__numberOfLines)
    
    @property
    def isolineColor(self):
        return self.__isolineColor
    
    @isolineColor.setter
    def isolineColor(self, isolineColor):
        self.__isolineColor = isolineColor
        self.GetProperty().SetColor(*self.__isolineColor)
        self.contentToSave['isolineColor'] = deepcopy(self.__isolineColor)
    
    @property
    def labelColor(self):
        return self.__labelColor
    
    @labelColor.setter
    def labelColor(self, labelColor):
        self.__labelColor = labelColor
        self._mapper.GetTextProperties().GetItem(0).SetColor(*self.__labelColor)
        self.contentToSave['labelColor'] = deepcopy(self.labelColor)


class Clip(_Object):
    __name__ = 'Clip'

    def __init__(self, parent: _Object):
        super().__init__()

        self._type = commonClasses.Type.clip

        self._parent = parent
        self.__invert = False

        x_min, x_max, y_min, y_max, z_min, z_max = self._parent.output.GetBounds()
        self.__origin = (x_max + x_min) / 2, (y_max + y_min) / 2, (z_max + z_min) / 2
        self.__normal = (0, 0, 1)

        self.contentToSave = {
            'origin': deepcopy(self.__origin),
            'normal': deepcopy(self.__normal),
            'invert': deepcopy(self.__invert)
        }

        self.__clipFunction = vtk.vtkPlane()
        self.__clipFunction.SetOrigin(*self.__origin)
        self.__clipFunction.SetNormal(*self.__normal)

        self.__clipper = vtk.vtkTableBasedClipDataSet()
        self.__clipper.SetClipFunction(self.__clipFunction)
        self.__clipper.SetInputConnection(self._parent.outputPort)
        self.__clipper.SetValue(0.0)
        self.__clipper.GenerateClippedOutputOn()
        self.__clipper.InsideOutOff()
        self.__clipper.Update()

        self.build()
        self.buildScalarBarActor()
    
    @classmethod
    def restoreFromSaveData(cls, parent, origin, normal, invert):
        instance = cls(parent)
        instance.origin = origin
        instance.normal = normal
        instance.invert = invert
        return instance
    
    @property
    def _mainFunction(self):
        return self.__clipper
    
    @property
    def normal(self):
        return self.__normal
    
    @normal.setter
    def normal(self, normal: tuple):
        self.__normal = normal
        self.__clipFunction.SetNormal(*self.__normal)
        self.contentToSave['normal'] = deepcopy(self.__normal)

    @property
    def origin(self):
        return self.__origin

    @origin.setter
    def origin(self, origin: tuple):
        self.__origin = origin
        self.__clipFunction.SetOrigin(*self.__origin)
        self.contentToSave['origin'] = deepcopy(self.__origin)
    
    @property
    def invert(self):
        return self.__invert
    
    @invert.setter
    def invert(self, invert: bool):
        self.__invert = invert
        if self.__invert:
            self.__clipper.InsideOutOn()
        else:
            self.__clipper.InsideOutOff()
        self.contentToSave['invert'] = deepcopy(self.__invert)


class Threshold(_Object):
    __name__ = 'Threshold'

    def __init__(self, parent: _Object):
        super().__init__()

        assert parent.dataMode == commonClasses.DataMode.scalar, f'{parent.type} must have scalar dataMode, {parent.dataMode=}'

        self._type = commonClasses.Type.threshold

        self._parent = parent
        self.__invert = False
        self.__range = self._parent.output.GetScalarRange()

        self.__threshold = vtk.vtkThreshold()
        commonFunctions.set_input(self.__threshold, self._parent.outputPort)
        self.__threshold.ThresholdBetween(*self.__range)
        self.__threshold.Update()

        self.contentToSave = {
            'invert': deepcopy(self.__invert),
            'range': deepcopy(self.__range)
        }

        self.build()
        self.buildScalarBarActor()
    
    @classmethod
    def restoreFromSaveData(cls, parent, invert, range):
        instance = cls(parent)
        instance.invert = invert
        instance.range = range
        return instance
    
    def resetRange(self):
        self.range = self._parent.output.GetScalarRange()
    
    @property
    def _mainFunction(self):
        return self.__threshold
    
    @property
    def invert(self):
        return self.__invert
    
    @invert.setter
    def invert(self, invert: bool):
        self.__invert = invert
        if self.__invert:
            self.__threshold.InvertOn()
        else:
            self.__threshold.InvertOff()
        self.contentToSave['invert'] = deepcopy(self.__invert)
    
    @property
    def range(self):
        return self.__range
    
    @range.setter
    def range(self, range):
        self.__range = range
        self.__threshold.ThresholdBetween(*self.__range)
        self.contentToSave['range'] = deepcopy(self.__range)


class Calculator(_Object):
    def __init__(self, parent: PVD):
        super().__init__()

        assert parent.dataMode == commonClasses.DataMode.scalar, 'Can calculate only scalar field'

        self._type = commonClasses.Type.calculator

        self._parent = parent
        self.raw_points = {}
        self.points = {}
        self.progressEnd = 0
        self.results = {}

    def setPoints(self, points: dict):
        self.raw_points = points.copy()
        self.points = {}
        self.progressEnd = len(points)

        for t, points in points.items():
            vtk_points = vtk.vtkPoints()
            for point in points:
                vtk_points.InsertNextPoint(*map(float, point))
            point_poly_data = vtk.vtkPolyData()
            point_poly_data.SetPoints(vtk_points)
            self.points[t] = point_poly_data

    def calculate(self, say=None):
        self.results = {}
        reader = vtk.vtkXMLUnstructuredGridReader()
        callable_say = callable(say)
        for i, (t, points) in enumerate(self.points.items()):
            # set time
            reader.SetFileName(self._parent._directoryName + '/' + self._parent._filenames[t])
            reader.Update()
            result = []

            # calculate
            probe_filter = vtk.vtkProbeFilter()
            probe_filter.SetInputData(points)
            probe_filter.SetSourceData(reader.GetOutput())
            probe_filter.Update()

            data_array = probe_filter.GetOutput().GetPointData().GetScalars()
            for j in range(data_array.GetNumberOfTuples()):
                result.append(data_array.GetTuple(j)[0])
            self.results[t] = result

            if callable_say:
                say(int((i + 1) / self.progressEnd * 100))


class Another(_Object):
    def __init__(self):
        super().__init__()

        self._type = commonClasses.Type.another


componentIndexToStr = {
    0: 'X',
    1: 'Y',
    2: 'Z'
}
