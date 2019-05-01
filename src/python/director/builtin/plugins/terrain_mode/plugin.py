from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from director import applogic
from PythonQt import QtCore


class Plugin(GenericPlugin):

  ID = 'terrain_mode'
  NAME = 'TerrainMode'
  DEPENDENCIES = ['View', 'MainToolBar']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    terrainModeAction = fields.app.addToolBarAction(
      fields.mainToolBar,
      'Camera Free Rotate',
      ':/images/camera_mode.png'
    )
    # create lambda functions
    def getFreeCameraMode():
      return not applogic.getCameraTerrainModeEnabled(fields.view)

    def setFreeCameraMode(enabled):
      applogic.setCameraTerrainModeEnabled(fields.view, not enabled)
    # ---
    terrainToggle = applogic.ActionToggleHelper(
      terrainModeAction,
      getFreeCameraMode,
      setFreeCameraMode
    )
    # ---
    return FieldContainer(
      terrainToggle=terrainToggle
    )
