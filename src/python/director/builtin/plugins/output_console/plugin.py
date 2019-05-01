from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from .lib import outputconsole

class Plugin(GenericPlugin):

  ID = 'output_console'
  NAME = 'OutputConsole'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    outputConsole = outputconsole.OutputConsole()
    outputConsole.addToAppWindow(self.app, visible=False)
    return FieldContainer(
      outputConsole=outputConsole
    )
