from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk
from PySide2 import QtWidgets, QtCore, QtGui

from . import commonClasses
from . import commonFunctions
from . import objects
from . import properties
from . import defaults
from . import items


class VtkWidget(QVTKRenderWindowInteractor):
    focused = QtCore.Signal()
    cameraReset = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.autoResetCamera = True
        self.autoFocus = True
        self.showColorMap = False

        self.renderer = vtk.vtkRenderer()
        # self.renderer.SetBackground(1, 1, 1)

        self.__objects = list()

        self.renderWindow = self.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)
    
        self.renderWindow.GlobalWarningDisplayOff()
        self.renderWindow.StencilCapableOn()

        self.interactor = self.renderWindow.GetInteractor()
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()
        self.interactor.Start()

        self.textProperty = vtk.vtkTextProperty()
        # self.textProperty.SetColor(0, 0, 0)
        self.textProperty.SetBold(False)
        self.textProperty.SetItalic(False)
        self.textProperty.SetShadow(False)

        self.axesActor = vtk.vtkAxesActor()
        self.axesActor.GetXAxisCaptionActor2D().SetCaptionTextProperty(self.textProperty)
        self.axesActor.GetYAxisCaptionActor2D().SetCaptionTextProperty(self.textProperty)
        self.axesActor.GetZAxisCaptionActor2D().SetCaptionTextProperty(self.textProperty)

        self.orientationMarker = vtk.vtkOrientationMarkerWidget()
        self.orientationMarker.SetOrientationMarker(self.axesActor)
        self.orientationMarker.SetInteractor(self.interactor)
        self.orientationMarker.EnabledOn()
        self.orientationMarker.InteractiveOn()
        # self.orientationMarker.SetOutlineColor(0, 0, 0)
        self.theme = 'Light'
        self.setLightTheme()

    def setLightTheme(self):
        self.renderer.SetBackground(1, 1, 1)
        self.orientationMarker.SetOutlineColor(0, 0, 0)
        self.textProperty.SetColor(0, 0, 0)
    
    def setDarkTheme(self):
        self.renderer.SetBackground(0, 0, 0)
        self.orientationMarker.SetOutlineColor(1, 1, 1)
        self.textProperty.SetColor(1, 1, 1)

    def focus(self):
        self.renderWindow.Render()
        self.setFocus()
    
    def getCameraFocalPointPosition(self):
        return self.renderer.GetActiveCamera().GetFocalPoint(), self.renderer.GetActiveCamera().GetPosition()

    def resetCamera(self, saveDistance=True):
        fp, p = self.getCameraFocalPointPosition()

        d = sum(i * i for i in (p[0] - fp[0], p[1] - fp[1], p[2] - fp[2])) ** 0.5

        self.renderer.ResetCamera()

        if saveDistance:
            nfp = self.renderer.GetActiveCamera().GetFocalPoint()
            np = self.renderer.GetActiveCamera().GetPosition()
            mvu = np[0] - nfp[0], np[1] - nfp[1], np[2] - nfp[2]

            nd = sum(pow(i, 2) for i in mvu) ** 0.5

            mvu = mvu[0] / nd, mvu[1] / nd, mvu[2] / nd

            mp = nfp[0] + d * mvu[0], nfp[1] + d * mvu[1], nfp[2] + d * mvu[2]
            md = sum(i * i for i in (mp[0] - nfp[0], mp[1] - nfp[1], mp[2] - nfp[2])) ** 0.5

            if md >= (nd + 0.1):
                self.renderer.GetActiveCamera().SetClippingRange(md - (nd + 0.1), md + (nd + 0.1))
                self.renderer.GetActiveCamera().SetPosition(*mp)
    
    def setCameraPositionViewUp(self, position, viewUp):
        self.renderer.GetActiveCamera().SetPosition(*position)
        self.renderer.GetActiveCamera().SetViewUp(*viewUp[0])

    def resetViewUp(self, viewUp):
        fp, p = self.getCameraFocalPointPosition()
        dist = sum(pow(i, 2) for i in ((p[0] - fp[0]), (p[1] - fp[1]), (p[2] - fp[2]))) ** 0.5
        position = tuple((fp[i] + viewUp[1] * viewUp[2][i] * dist) for i in range(3))
        self.setCameraPositionViewUp(position, viewUp)
    
    def setViewUpToXPlus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 0, 1), 1, (1, 0, 0)))

    def setViewUpToXMinus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 0, 1), -1, (1, 0, 0)))
    
    def setViewUpToYPlus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 0, 1), 1, (0, 1, 0)))
    
    def setViewUpToYMinus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 0, 1), -1, (0, 1, 0)))
    
    def setViewUpToZPlus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 1, 0), 1, (0, 0, 1)))
    
    def setViewUpToZMinus(self):
        self.resetCamera(saveDistance=False)
        self.resetViewUp(((0, 1, 0), -1, (0, 0, 1)))

    def addObject(self, object: objects._Object):
        self.__addActor(object)
        if object.type == commonClasses.Type.outline:
            object.SetCamera(self.renderer.GetActiveCamera())
        if object._hasScalarBarActor and object._showScalarBarActor:
            if not object.scalarBarActor.hasInteractor:
                object.scalarBarActor.interactor = self.interactor
            if self.theme == 'Light':
                object.scalarBarActor.setLightTheme()
            elif self.theme == 'Dark':
                object.scalarBarActor.setDarkTheme()
            object.scalarBarActor.scalarBarWidget.On()
            self.__addActor(object.scalarBarActor)
        if len(self.__objects) == 1:
            self.resetCamera()
        self.tryAutoFocus()

    def removeObject(self, object: objects._Object):
        self.__removeActor(object)
        if object._hasScalarBarActor:
            self.__removeActor(object.scalarBarActor)
            object.scalarBarActor.scalarBarWidget.Off()
        self.tryAutoFocus()

    def clearObjects(self):
        for object in self.__objects:
            if isinstance(object, objects.ScalarBarActor):
                object.scalarBarWidget.Off()
            self.__removeActor(object)

    def __addActor(self, actor: objects._Object):
        if actor not in self.__objects:
            self.renderer.AddActor(actor)
            self.__objects.append(actor)

    def __removeActor(self, actor: objects._Object):
        if actor in self.__objects:
            self.renderer.RemoveActor(actor)
            self.__objects.remove(actor)
    
    def whatInObjects(self):
        print(self.__objects)

    def itemVisibilityChanged(self, check_state: QtCore.Qt.CheckState, item: items.TreeWidgetItem):
        if check_state == QtCore.Qt.Checked:
            self.addObject(item.object)
        elif check_state == QtCore.Qt.Unchecked:
            self.removeObject(item.object)
        else:
            raise TypeError(f'[VtkWidget.itemVisibilityChanged] unexpected CheckState: {check_state}')
        self.tryAutoResetCamera()
        self.tryAutoFocus()

    def changedTitleItem(self, item: items.TreeWidgetItem, _):
        title = item.text(0)
        if item.object.title != title:
            item.object.title = title
            self.tryAutoFocus()

    def tryAutoUpdateVtkWidget(self):
        self.tryAutoResetCamera()
        self.tryAutoFocus()

    def tryAutoFocus(self):
        if self.autoFocus:
            self.focused.emit()
            self.focus()

    def tryAutoResetCamera(self):
        if self.autoResetCamera:
            self.cameraReset.emit()
            self.resetCamera()

    def vtkObjectShowColorMapChanged(self, item: items.TreeWidgetItem):
        if item.object in self.__objects:
            self.removeObject(item.object)
            self.addObject(item.object)


class ToolBar(QtWidgets.QToolBar):
    checkToolBarItems = QtCore.Signal(items.TreeWidgetItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Полезный тулбар')

        self.x_p = self.addAction('x+')
        self.x_m = self.addAction('x-')
        self.y_p = self.addAction('y+')
        self.y_m = self.addAction('y-')
        self.z_p = self.addAction('z+')
        self.z_m = self.addAction('z-')
        self.toggleAxesVisibility = self.addAction('Toggle axes visibility')
        self.sep_1 = self.addSeparator()
        self.addOutline = self.addAction('Outline')
        self.sep_2 = self.addSeparator()
        self.addIsoline = self.addAction('Isoline')
        self.addCut = self.addAction('Cut')
        self.addClip = self.addAction('Clip')
        self.addThreshold = self.addAction('Threshold')
        self.sep_3 = self.addSeparator()
        self.showColorMap = self.addAction('Show color map')
        self.sep_4 = self.addSeparator()
        self.addPointCalculator = self.addAction('Point calculator')
        self.addPileCalculator = self.addAction('Pile calculator')

    def currentItemChanged(self, item: items.TreeWidgetItem, _):
        if isinstance(item, items.TreeWidgetItem):
            if item.object.type == commonClasses.Type.pvd:
                self.updateToolBar(cut=False, clip=False, threshold=False, colorMap=False, calculator=False, outline=False)
            elif item.object.type == commonClasses.Type.cut:
                self.updateToolBar(isoline=False, threshold=False, colorMap=False, outline=False)
            elif item.object.type == commonClasses.Type.isoline:
                self.updateToolBar()
            elif item.object.type == commonClasses.Type.clip:
                self.updateToolBar(cut=False, clip=False, threshold=False, colorMap=False, outline=False)
            elif item.object.type == commonClasses.Type.threshold:
                self.updateToolBar(cut=False, clip=False, threshold=False, colorMap=False, outline=False)
            else:
                self.updateToolBar()
                self.checkToolBarItems.emit(item)
        else:
            self.updateToolBar()
            self.checkToolBarItems.emit(item)

    def updateToolBar(self, cut=True, isoline=True, clip=True, threshold=True, colorMap=True, calculator=True, outline=True):
        self.addCut.setDisabled(cut)
        self.addIsoline.setDisabled(isoline)
        self.addClip.setDisabled(clip)
        self.addThreshold.setDisabled(threshold)
        self.showColorMap.setDisabled(colorMap)
        self.addPileCalculator.setDisabled(calculator)
        self.addPointCalculator.setDisabled(calculator)
        self.addOutline.setDisabled(outline)


class TreeWidget(QtWidgets.QTreeWidget):
    itemVisibilityChanged = QtCore.Signal(QtCore.Qt.CheckState, items.TreeWidgetItem)
    vtkObjectShowColorMapChanged = QtCore.Signal(items.TreeWidgetItem)
    clearAll = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHeaderHidden(True)

        self.itemClicked.connect(self.itemClick)

    def itemClick(self, item: items.TreeWidgetItem, _):
        check_state, changes = item.isChecked()
        if changes:
            self.itemVisibilityChanged.emit(check_state, item)
    
    def addOutline(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        outline = objects.Outline(currentItem.object)
        tree_widget_item = items.TreeWidgetItem(outline)
        tree_widget_item.content = {}
        currentItem.addChild(tree_widget_item)
        currentItem.setExpanded(True)

    def addCut(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        assert commonFunctions.checkPermission(currentItem.object.type, commonClasses.Type.cut), f'Can\'t create cut from {currentItem.object.type}'
        cut = objects.Cut(currentItem.object)
        content = defaults.cut.copy()
        content['origin'] = commonFunctions.replaceType(cut.origin, str)
        tree_widget_item = items.TreeWidgetItem(cut)
        tree_widget_item.content = content
        currentItem.addChild(tree_widget_item)
        currentItem.setExpanded(True)
    
    def addIsoline(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        assert commonFunctions.checkPermission(currentItem.object.type, commonClasses.Type.isoline), f'Can\'t create isoline from {currentItem.object.type}'
        isoline = objects.Isoline(currentItem.object)
        tree_widget_item = items.TreeWidgetItem(isoline)
        tree_widget_item.content = defaults.isoline.copy()
        currentItem.addChild(tree_widget_item)
        currentItem.setExpanded(True)
    
    def showColorMap(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        vtkObject: objects._Object = currentItem.object
        if vtkObject._hasScalarBarActor:
            vtkObject._showScalarBarActor = not vtkObject._showScalarBarActor
            self.vtkObjectShowColorMapChanged.emit(currentItem)
    
    def addClip(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        assert commonFunctions.checkPermission(currentItem.object.type, commonClasses.Type.clip), f'Can\'t create clip from {currentItem.object.type}'
        clip = objects.Clip(currentItem.object)
        content = defaults.clip.copy()
        content['origin'] = commonFunctions.replaceType(clip.origin, str)
        tree_widget_item = items.TreeWidgetItem(clip)
        tree_widget_item.content = content
        currentItem.addChild(tree_widget_item)
        currentItem.setExpanded(True)
    
    def addThreshold(self):
        currentItem: items.TreeWidgetItem = self.currentItem()
        assert commonFunctions.checkPermission(currentItem.object.type, commonClasses.Type.threshold), f'Can\'t create clip from {currentItem.object.type}'
        threshold = objects.Threshold(currentItem.object)
        content = defaults.threshold.copy()
        content['range'] = commonFunctions.replaceType(threshold.range, str)
        tree_widget_item = items.TreeWidgetItem(threshold)
        tree_widget_item.content = content
        currentItem.addChild(tree_widget_item)
        currentItem.setExpanded(True)
    
    def clear(self):
        self.clearAll.emit()
        super().clear()


class PropertiesDockWidget(QtWidgets.QDockWidget):
    dataChanged = QtCore.Signal()
    removeFromTree = QtCore.Signal(items.TreeWidgetItem)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Настройки')
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setWidget(self.scrollArea)

    def currentItemChange(self, current: items.TreeWidgetItem, previous: items.TreeWidgetItem):
        if previous is not None and isinstance(previous, items.TreeWidgetItem):
            previous_widget: properties.Property = self.scrollArea.takeWidget()
            previous_widget.item  # save data
            previous_widget.deleteLater()
        if current is not None and isinstance(current, items.TreeWidgetItem):
            current_widget: properties.Property = ItemObjectTypeToWidget[current.object.type]()
            current_widget.dataChanged.connect(self.dataChanged.emit)
            current_widget.item = current
            current_widget.removed.connect(lambda: self.removeFromTree.emit(current))
            self.scrollArea.setWidget(current_widget)


class VisualizationDockWidget(QtWidgets.QDockWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Обозреватель')
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)

        self.treeWidget = TreeWidget(self)

        widget = QtWidgets.QWidget(self)
        widget.setLayout(QtWidgets.QVBoxLayout())
        widget.layout().addWidget(self.treeWidget)
        widget.layout().setContentsMargins(0, 0, 0, 0)

        self.setWidget(widget)
    
    def removeFromTree(self, item: items.TreeWidgetItem):
        self.treeWidget.itemVisibilityChanged.emit(QtCore.Qt.CheckState.Unchecked, item)
        for i in range(item.childCount()):
            self.removeFromTreeChild(item.child(i))
        item.parent().removeChild(item)
    
    def removeFromTreeChild(self, item):
        self.treeWidget.itemVisibilityChanged.emit(QtCore.Qt.CheckState.Unchecked, item)
        for i in range(item.childCount()):
            self.removeFromTreeChild(item.child(i))
        item.parent().removeChild(item)

    def loadPvdFile(self, filename: str, timeStep: str, piles, piles_settings, startTime):
        pvd = objects.PVD(filename, timeStep, piles, piles_settings, startTime)
        tree_widget_item = items.TreeWidgetItem(pvd)
        tree_widget_item.content = defaults.pvd.copy()
        self.treeWidget.addTopLevelItem(tree_widget_item)
        return tree_widget_item

    def save(self):
        itemsToSave = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item: items.TreeWidgetItem = self.treeWidget.topLevelItem(i)
            itemsToSave.append((item.object.__name__, (item.object.contentToSave, item.content), item.text(0), self.saveChilds(item), item.checkState(0) == QtCore.Qt.Checked))
        return itemsToSave

    def saveChilds(self, item):
        childsToSave = []
        for i in range(item.childCount()):
            child = item.child(i)
            childsToSave.append((child.object.__name__, child.content, child.text(0), self.saveChilds(child), child.checkState(0) == QtCore.Qt.Checked))
        return childsToSave

    def load(self, itemsToLoad):
        for item in itemsToLoad:
            object = nameToObject[item[0]].restoreFromSaveData(**item[1][0])
            tree_widget_item = items.TreeWidgetItem(object)
            tree_widget_item.content = item[1][1]
            self.treeWidget.addTopLevelItem(tree_widget_item)
            tree_widget_item.setText(0, item[2])
            tree_widget_item.setCheckState(0, QtCore.Qt.Checked if item[4] else QtCore.Qt.Unchecked)
            tree_widget_item.isChecked()
            self.treeWidget.itemVisibilityChanged.emit(QtCore.Qt.Checked if item[4] else QtCore.Qt.Unchecked, tree_widget_item)
            self.loadChilds(tree_widget_item, item[3])

    def loadChilds(self, parent, childsToLoad):
        if childsToLoad is not None and childsToLoad:
            for item in childsToLoad:
                object = nameToObject[item[0]](parent.object)
                tree_widget_item = items.TreeWidgetItem(object)
                tree_widget_item.content = item[1]
                parent.addChild(tree_widget_item)
                tree_widget_item.setText(0, item[2])
                tree_widget_item.setCheckState(0, QtCore.Qt.Checked if item[4] else QtCore.Qt.Unchecked)
                tree_widget_item.isChecked()
                self.treeWidget.itemVisibilityChanged.emit(QtCore.Qt.Checked if item[4] else QtCore.Qt.Unchecked, tree_widget_item)
                self.loadChilds(tree_widget_item, item[3])
            if not parent.isExpanded():
                parent.setExpanded(True)


def connect(widget: VtkWidget=None, prop_dock_widget: PropertiesDockWidget=None, tool_bar: ToolBar=None, vis_dock_widget: VisualizationDockWidget=None):
    if vis_dock_widget is not None:
        if prop_dock_widget is not None:
            vis_dock_widget.treeWidget.currentItemChanged.connect(prop_dock_widget.currentItemChange)
            prop_dock_widget.removeFromTree.connect(vis_dock_widget.removeFromTree)
        if tool_bar is not None:
            tool_bar.addCut.triggered.connect(vis_dock_widget.treeWidget.addCut)
            tool_bar.addIsoline.triggered.connect(vis_dock_widget.treeWidget.addIsoline)
            tool_bar.showColorMap.triggered.connect(vis_dock_widget.treeWidget.showColorMap)
            tool_bar.addClip.triggered.connect(vis_dock_widget.treeWidget.addClip)
            tool_bar.addThreshold.triggered.connect(vis_dock_widget.treeWidget.addThreshold)
            tool_bar.addOutline.triggered.connect(vis_dock_widget.treeWidget.addOutline)
            vis_dock_widget.treeWidget.currentItemChanged.connect(tool_bar.currentItemChanged)
    
    if widget is not None:
        if tool_bar is not None:
            tool_bar.x_p.triggered.connect(widget.setViewUpToXPlus)
            tool_bar.x_m.triggered.connect(widget.setViewUpToXMinus)
            tool_bar.y_p.triggered.connect(widget.setViewUpToYPlus)
            tool_bar.y_m.triggered.connect(widget.setViewUpToYMinus)
            tool_bar.z_p.triggered.connect(widget.setViewUpToZPlus)
            tool_bar.z_m.triggered.connect(widget.setViewUpToZMinus)
            tool_bar.x_p.triggered.connect(widget.tryAutoFocus)
            tool_bar.x_m.triggered.connect(widget.tryAutoFocus)
            tool_bar.y_p.triggered.connect(widget.tryAutoFocus)
            tool_bar.y_m.triggered.connect(widget.tryAutoFocus)
            tool_bar.z_p.triggered.connect(widget.tryAutoFocus)
            tool_bar.z_m.triggered.connect(widget.tryAutoFocus)
        if vis_dock_widget is not None:
            vis_dock_widget.treeWidget.itemVisibilityChanged.connect(widget.itemVisibilityChanged)
            vis_dock_widget.treeWidget.vtkObjectShowColorMapChanged.connect(widget.vtkObjectShowColorMapChanged)
            vis_dock_widget.treeWidget.vtkObjectShowColorMapChanged.connect(widget.tryAutoFocus)
            vis_dock_widget.treeWidget.clearAll.connect(widget.clearObjects)
            vis_dock_widget.treeWidget.itemChanged.connect(widget.changedTitleItem)
        if prop_dock_widget is not None:
            prop_dock_widget.dataChanged.connect(widget.tryAutoResetCamera)
            prop_dock_widget.dataChanged.connect(widget.tryAutoFocus)


def build(main_window, widget=True, vis_dock_widget=True, prop_dock_widget=True, tool_bar=True):
    widgets = []
    if widget:
        widget = VtkWidget(main_window)
        widgets.append(widget)
    if vis_dock_widget:
        vis_dock_widget = VisualizationDockWidget(main_window)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, vis_dock_widget)
        widgets.append(vis_dock_widget)
    if prop_dock_widget:
        prop_dock_widget = PropertiesDockWidget(main_window)
        main_window.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, prop_dock_widget)
        widgets.append(prop_dock_widget)
    if tool_bar:
        tool_bar = ToolBar(widget)
        main_window.addToolBar(tool_bar)
        tool_bar.updateToolBar()
        widgets.append(tool_bar)

    return widgets


ItemObjectTypeToWidget = {
    commonClasses.Type.pvd: properties.PVD,
    commonClasses.Type.cut: properties.Cut,
    commonClasses.Type.isoline: properties.Isoline,
    commonClasses.Type.clip: properties.Clip,
    commonClasses.Type.threshold: properties.Threshold,
    commonClasses.Type.outline: properties.Outline
}

nameToObject = {
    'PVD': objects.PVD,
    'Outline': objects.Outline,
    'Cut': objects.Cut,
    'Isoline': objects.Isoline,
    'Clip': objects.Clip,
    'Threshold': objects.Threshold,
}

typeToDefault = {
    commonClasses.Type.pvd: defaults.pvd
}
