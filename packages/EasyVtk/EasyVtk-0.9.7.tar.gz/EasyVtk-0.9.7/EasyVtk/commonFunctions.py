import vtk

from . import commonClasses
from . import defaults


def replaceType(iter, typeToReplace):
    return type(iter)(typeToReplace(value) for value in iter)


def checkPermission(parent_type: commonClasses.Type, child_type):
    return parent_type in defaults.creation_permission[child_type]


def create_data_set_mapper(any_input):
    mapper = vtk.vtkDataSetMapper()
    mapper.ScalarVisibilityOn()
    set_input(mapper, any_input)
    return mapper


def create_poly_data_mapper(_input):
	_mapper = vtk.vtkPolyDataMapper()
	_mapper.ScalarVisibilityOff()
	return set_input(_mapper, _input)


def set_input(_here, _input):
	if _input.IsA('vtkPolyData'):
		_here.SetInputData(_input)
	elif _input.IsA('vtkDataSet'):
		_here.SetInputData(_input)
	elif _input.IsA('vtkStructuredGrid'):
		_here.SetInputData(_input)
	elif _input.IsA('vtkUnstructuredGrid'):
		_here.SetInputData(_input)
	elif _input.IsA('vtkAlgorithmOutput'):
		_here.SetInputConnection(_input)
	else:
		_here.SetInputConnection(_input.GetOutputPort())
	return _here


def create_actor(_mapper):
	_actor = vtk.vtkActor()
	_actor.SetMapper(_mapper)
	return _actor


def remakeRGBPoints(colorTransferFunction: vtk.vtkColorTransferFunction, scalarRange, RGBPoints: tuple):
    colorTransferFunction.RemoveAllPoints()
    a = scalarRange[1] - scalarRange[0]
    for i in range(int(len(RGBPoints) / 4)):
        colorTransferFunction.AddRGBPoint(a * RGBPoints[i * 4] + scalarRange[0], *RGBPoints[i * 4 + 1: i * 4 + 4])


def setUpCtf(scalarRange, RGBPoints):
    colorTransferFunction = vtk.vtkColorTransferFunction()
    remakeRGBPoints(colorTransferFunction, scalarRange, RGBPoints)
    return colorTransferFunction
