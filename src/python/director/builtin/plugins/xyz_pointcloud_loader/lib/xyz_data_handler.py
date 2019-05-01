import os
import numpy as np
from director import objectmodel as om
from director import visualization as vis
from PythonQt import QtGui

from director import applogic
from director import vtkAll as vtk
from director import visualization as vis
from director import vtkNumpy as vnp


class OpenDataHandler(object):

  def __init__(self, mainWindowApp):
    self.app = mainWindowApp
    self.rootFolderName = 'point cloud files'
    self.openAction = QtGui.QAction('&Open XYZ file...', self.app.fileMenu)
    self.app.fileMenu.insertAction(self.app.quitAction, self.openAction)
    self.app.fileMenu.insertSeparator(self.app.quitAction)
    self.openAction.connect('triggered()', self.onOpenDataFile)

  def getRootFolder(self):
    return om.getOrCreateContainer(self.rootFolderName)

  def openGeometry(self, filename):
    # read data
    reader = vtk.vtkDelimitedTextReader()
    reader.SetFileName(filename)
    reader.SetFieldDelimiterCharacters(' ')
    reader.SetHaveHeaders(False)
    reader.SetDetectNumericColumns(True)
    # turn XYZ data into PolyData
    points = vtk.vtkTableToPolyData()
    points.SetInputConnection(reader.GetOutputPort())
    points.SetXColumnIndex(2)
    points.SetYColumnIndex(3)
    points.SetZColumnIndex(4)
    # turn XYZ data into PolyData
    rgb = vtk.vtkTableToPolyData()
    rgb.SetInputConnection(reader.GetOutputPort())
    rgb.SetXColumnIndex(5)
    rgb.SetYColumnIndex(6)
    rgb.SetZColumnIndex(7)
    # get polydata
    points.Update()
    polyData = points.GetOutput()
    if not polyData or not polyData.GetNumberOfPoints():
      self.app.showErrorMessage(
        'Failed to read any data from file: %s' % filename,
        title='Reader error'
      )
      return
    # get colors
    rgb.Update()
    rgb = vnp.getNumpyFromVtk(rgb.GetOutput()).astype(np.uint8)
    # add colors to points
    vnp.addNumpyToVtk(polyData, rgb, 'RGB')
    # show data
    obj = vis.showPolyData(polyData, os.path.basename(filename), parent=self.getRootFolder())
    obj.setProperty('Color By', 'RGB')
    vis.addChildFrame(obj)

  def onOpenDataFile(self):
    fileFilters = 'XYZ Point Cloud File (*.xyz)';
    filename = QtGui.QFileDialog.getOpenFileName(
      self.app.mainWindow,
      'Open...',
      self.getOpenDataDirectory(),
      fileFilters
    )
    if not filename:
      return
    self.storeOpenDataDirectory(filename)
    self.openGeometry(filename)

  def getOpenDataDirectory(self):
    return self.app.settings.value('OpenDataDir') or os.path.expanduser('~')

  def storeOpenDataDirectory(self, filename):
    if os.path.isfile(filename):
      filename = os.path.dirname(filename)
    if os.path.isdir(filename):
      self.app.settings.setValue('OpenDataDir', filename)
