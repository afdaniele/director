from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from director import args_parser
from .lib import opendatahandler

class Plugin(GenericPlugin):

  ID = 'mesh_loader'
  NAME = 'MeshLoader'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    openDataHandler = opendatahandler.OpenDataHandler(self.app)
    # ---
    def loadData():
      for filename in args_parser.args().data_files:
        openDataHandler.openGeometry(filename)
    # ---
    self.app.registerStartupCallback(loadData)
    return FieldContainer(
      meshDataHandler=openDataHandler
    )
