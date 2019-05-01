from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from .lib import camerabookmarks
from PythonQt import QtCore


class Plugin(GenericPlugin):

  ID = 'camera_bookmarks'
  NAME = 'CameraBookmarks'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    cameraBookmarksPanel = camerabookmarks.CameraBookmarkWidget(self.view)
    cameraBookmarksDock = self.app.addWidgetToDock(
      cameraBookmarksPanel.widget,
      QtCore.Qt.RightDockWidgetArea,
      visible=False
    )
    # ---
    return FieldContainer(
      cameraBookmarksPanel=cameraBookmarksPanel,
      cameraBookmarksDock=cameraBookmarksDock
    )
