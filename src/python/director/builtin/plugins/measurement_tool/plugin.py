from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from .lib import measurementpanel
from PythonQt import QtCore


class Plugin(GenericPlugin):

  ID = 'measurement_tool'
  NAME = 'MeasurementTool'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    measurementPanel = measurementpanel.MeasurementPanel(self.app, self.view)
    measurementDock = self.app.addWidgetToDock(
      measurementPanel.widget,
      QtCore.Qt.RightDockWidgetArea,
      visible=False
    )
    # ---
    return FieldContainer(
      measurementToolPanel=measurementPanel,
      measurementToolDock=measurementDock
    )
