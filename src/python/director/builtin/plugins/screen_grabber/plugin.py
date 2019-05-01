from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from .lib import screengrabberpanel
from PythonQt import QtCore


class Plugin(GenericPlugin):

  ID = 'screen_grabber'
  NAME = 'ScreenGrabber'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    screenGrabberPanel = screengrabberpanel.ScreenGrabberPanel(self.view)
    screenGrabberDock = self.app.addWidgetToDock(
      screenGrabberPanel.widget,
      QtCore.Qt.RightDockWidgetArea,
      visible=False
    )
    # ---
    return FieldContainer(
      screenGrabberPanel=screenGrabberPanel,
      screenGrabberDock=screenGrabberDock
    )
