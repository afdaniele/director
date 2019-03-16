from director.devel.plugins import GenericPlugin
from director.fieldcontainer import FieldContainer
from director import applogic
from director import vtkAll as vtk
from director import visualization as vis


class LineRenderer(GenericPlugin):

  def __init__(self, app, view, position, name, parent='data', color=[1,1,1], alpha=1.0):
    super(LineRenderer, self).__init__(app, view)
    self._position = position
    self._name = name
    self._parent = parent
    self._color = color
    self._alpha = alpha

  def init(self):
    pointObj = vis.showPolyData(np.asarray(self._position), self._name, view=self.view(), alpha=self._alpha, color=self._color, visible=True, parent=self._parent)

    pointObj.setProperty('Surface Mode', 'Points')
    pointObj.setProperty('Color', self._color)
    pointObj.setProperty('Alpha', self._alpha)
    return FieldContainer(pointObj=pointObj)
