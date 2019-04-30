from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from PythonQt import QtCore
from .lib import cameracontrolpanel


class Plugin(GenericPlugin):

  ID = 'camera_control_panel'
  NAME = 'CameraControlPanel'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    cameraControlPanel = cameracontrolpanel.CameraControlPanel(self.view)
    cameraControlDock = self.app.addWidgetToDock(
      cameraControlPanel.widget,
      QtCore.Qt.RightDockWidgetArea,
      visible=False
    )
    # ---
    return FieldContainer(
      cameraControlPanel=cameraControlPanel,
      cameraControlDock=cameraControlDock
    )
