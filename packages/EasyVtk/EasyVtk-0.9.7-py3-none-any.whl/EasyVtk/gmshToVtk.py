import vtkmodules.all as vtk

from . import commonFunctions


def gmshMeshToVtkMesh(ntags, ncoords, etags, entags):
    tags_to_vtk_id = {}

    points = vtk.vtkPoints()
    for i, tag in enumerate(ntags):
        tags_to_vtk_id[tag] = points.InsertNextPoint((ncoords[i * 3], ncoords[i * 3 + 1], ncoords[i * 3 + 2]))

    nodes = int(len(entags) / len(etags))

    cell_func = vtk.vtkTriangle if nodes == 3 else vtk.vtkTetra
    cells = vtk.vtkCellArray()

    for i in range(len(etags)):
        cell = cell_func()
        for j in range(nodes):
            cell.GetPointIds().SetId(j, tags_to_vtk_id[entags[i * nodes + j]])
        cells.InsertNextCell(cell)

    poly_data = vtk.vtkPolyData()
    poly_data.SetPoints(points)
    poly_data.SetPolys(cells)

    return poly_data

def drawGeometry(ntags, ncoords, etags, entags, color, opacity=1):
    poly_data = gmshMeshToVtkMesh(ntags, ncoords, etags, entags)
    mapper = commonFunctions.create_poly_data_mapper(poly_data)

    actor = commonFunctions.create_actor(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)

    return actor

def drawMesh(ntags, ncoords, etags, entags, color, opacity=1, lineWidth=1):
    poly_data = gmshMeshToVtkMesh(ntags, ncoords, etags, entags)
    poly_data = commonFunctions.set_input(vtk.vtkExtractEdges(), poly_data)
    mapper = commonFunctions.create_poly_data_mapper(poly_data)

    actor = commonFunctions.create_actor(mapper)
    actor.GetProperty().SetColor(color)
    actor.GetProperty().SetOpacity(opacity)
    actor.GetProperty().SetLineWidth(lineWidth)

    return actor
