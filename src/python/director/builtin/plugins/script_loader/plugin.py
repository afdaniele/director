from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from functools import partial
from PythonQt import QtCore


class Plugin(GenericPlugin):

  ID = 'script_loader'
  NAME = 'ScriptLoader'
  DEPENDENCIES = ['MainWindow', 'Globals']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def loadScripts(self, fields):
    for scriptArgs in fields.commandLineArgs.scripts:
      filename = scriptArgs[0]
      globalsDict = fields.globalsDict
      args = dict(
        __file__=filename,
        _argv=scriptArgs,
        _fields=fields
      )
      prev_args = {}
      for k, v in args.items():
        if k in globalsDict:
          prev_args[k] = globalsDict[k]
        globalsDict[k] = v
      try:
        code = compile(open(filename, 'r').read(), filename, 'exec')
        exec(code, globalsDict)
      finally:
        for k in args.keys():
          del globalsDict[k]
        for k, v in prev_args.items():
          globalsDict[k] = v

  def init(self, fields):
    loadScriptsFcn = partial(self.loadScripts, fields)
    self.app.registerStartupCallback(loadScriptsFcn)
