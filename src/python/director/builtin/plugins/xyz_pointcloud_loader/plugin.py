from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from director import args_parser
from .lib import xyz_data_handler

class Plugin(GenericPlugin):

  ID = 'xyz_pointcloud_loader'
  NAME = 'XYZPointCloudLoader'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    openDataHandler = xyz_data_handler.OpenDataHandler(self.app)
    # ---
    def loadData():
      if hasattr(args_parser.args(), 'xyz'):
        for filename in args_parser.args().xyz:
          openDataHandler.openGeometry(filename)
    # ---
    self.app.registerStartupCallback(loadData)
    return FieldContainer(
      xyzDataHandler=openDataHandler
    )
