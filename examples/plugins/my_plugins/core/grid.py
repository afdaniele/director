from director.devel.plugins import GenericPlugin
from director.fieldcontainer import FieldContainer
from director import applogic
from director import vtkAll as vtk
from director import visualization as vis


class Grid(GenericPlugin):

  def __init__(self, app, view, cellSize=0.5, numberOfCells=25, name='grid', parent='sensors', color=[1,1,1], alpha=0.05, gridTransform=None, viewBoundsFunction=None):
    super(Grid, self).__init__(app, view)
    self._cellSize = cellSize
    self._numberOfCells = numberOfCells
    self._name = name
    self._parent = parent
    self._color = color
    self._alpha = alpha
    self._gridTransform = gridTransform
    self._viewBoundsFunction = viewBoundsFunction

  def init(self):
    grid = vtk.vtkGridSource()
    grid.SetScale(self._cellSize)
    grid.SetGridSize(self._numberOfCells)
    grid.SetSurfaceEnabled(True)
    grid.Update()

    gridObj = vis.showPolyData(grid.GetOutput(), self._name, view=self.view(), alpha=self._alpha, color=self._color, visible=True, parent=self._parent)
    gridObj.gridSource = grid
    gridObj.actor.GetProperty().LightingOff()
    gridObj.actor.SetPickable(False)

    gridTransform = self._gridTransform or vtk.vtkTransform()
    gridObj.actor.SetUserTransform(gridTransform)
    vis.showFrame(gridTransform, self._name + ' frame', scale=0.2, visible=False, parent=gridObj, view=self._view)

    gridObj.setProperty('Surface Mode', 'Wireframe')

    viewBoundsFunction = self._viewBoundsFunction or self._computeViewBoundsNoGrid
    def onViewBoundsRequest():
      if self._view not in gridObj.views or not gridObj.getProperty('Visible'):
        return
      bounds = viewBoundsFunction(self.view(), gridObj)
      if vtk.vtkMath.AreBoundsInitialized(bounds):
        self.view().addCustomBounds(bounds)
      else:
        self.view().addCustomBounds([-1, 1, -1, 1, -1, 1])
    self.view().connect('computeBoundsRequest(ddQVTKWidgetView*)', onViewBoundsRequest)

    gridObj.setProperty('Surface Mode', 'Wireframe')
    gridObj.setProperty('Color', [0,0,0])
    gridObj.setProperty('Alpha', 0.1)
    applogic.resetCamera(viewDirection=[-1, -1, -0.3], view=self.view())
    return FieldContainer(gridObj=gridObj)

  @staticmethod
  def _computeViewBoundsNoGrid(view, gridObj):
    gridObj.actor.SetUseBounds(False)
    bounds = view.renderer().ComputeVisiblePropBounds()
    gridObj.actor.SetUseBounds(True)
    return bounds
