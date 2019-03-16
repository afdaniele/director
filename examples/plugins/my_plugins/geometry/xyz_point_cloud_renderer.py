import numpy as np
from director.devel.plugins import GenericPlugin
from director.fieldcontainer import FieldContainer
from director import applogic
from director import vtkAll as vtk
from director import visualization as vis
from director import vtkNumpy as vnp


class XYZPointCloudRenderer(GenericPlugin):

  def __init__(self, app, view, position, name, parent='data', color=[1,1,1], alpha=1.0):
    super(XYZPointCloudRenderer, self).__init__(app, view)
    self._position = position
    self._name = name
    self._parent = parent
    self._color = color
    self._alpha = alpha
    self._data = None

  def init(self):

    data = self.load_data()

    self._data = vis.showPolyData(data, self._name, view=self.view(), alpha=self._alpha, color=self._color, visible=True, parent=self._parent)
    self._data.setProperty('Surface Mode', 'Points')
    self._data.setProperty('Color', self._color)
    self._data.setProperty('Alpha', self._alpha)
    return FieldContainer(pointCloudObj=self._data)

  def load_data(self):
    # format: u, v, x, y, z, r, g, b
    filename = '/code/data/sparse_1_20.xyz'

    reader = vtk.vtkDelimitedTextReader()
    reader.SetFileName(filename)
    reader.SetFieldDelimiterCharacters(' ')
    reader.SetHaveHeaders(False)
    reader.SetDetectNumericColumns(True)

    points = vtk.vtkTableToPolyData()
    points.SetInputConnection(reader.GetOutputPort())
    points.SetXColumnIndex(2)
    points.SetYColumnIndex(3)
    points.SetZColumnIndex(4)


    # points = vtk.vtkTableToPolyData()
    # points.SetInputConnection(reader.GetOutputPort())
    # points.SetXColumnIndex(2)
    # points.SetYColumnIndex(3)
    # points.SetZColumnIndex(4)





#     inputFile = 'test.txt'
#
# import numpy
#
# data = numpy.genfromtxt(inputFile, delimiter=' ')
# assert(data.shape[1] == 6)
#
# numberOfPoints = data.shape[0]
#
# points = vtk.vtkPoints()
# points.SetNumberOfPoints(numberOfPoints)
#
# colors = vtk.vtkUnsignedCharArray()
# colors.SetName("RGB255")
# colors.SetNumberOfComponents(3)
# colors.SetNumberOfTuples(numberOfPoints)
#
# for i in xrange(numberOfPoints):
#     points.SetPoint(i, data[i][:3])
#     colors.SetTuple(i, data[i][3:])
#
# polyData = vtk.vtkPolyData()
# polyData.SetPoints(points)
# polyData.GetPointData().AddArray(colors)
#
# mask = vtk.vtkMaskPoints()
# mask.SetOnRatio(1)
# mask.GenerateVerticesOn()
# mask.SingleVertexPerCellOn()
# mask.SetInput(polyData)
# mask.Update()
#
# self.GetOutput().ShallowCopy(mask.GetOutput())












    points.Update()
    return points.GetOutput()
