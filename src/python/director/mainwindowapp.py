import os
import functools
import PythonQt
from PythonQt import QtCore, QtGui
import director

from director.componentgraph import ComponentFactory
from director import consoleapp
import director.objectmodel as om
import director.visualization as vis
from director.fieldcontainer import FieldContainer
from director import applogic
from director import appsettings
from director import args_parser
from director.devel import PluginManager



class MainWindowApp(object):

  def __init__(self):
    self.mainWindow = QtGui.QMainWindow()
    self.mainWindow.resize(768 * (16/9.0), 768)
    self.settings = QtCore.QSettings()

    self.fileMenu = self.mainWindow.menuBar().addMenu('&File')
    self.editMenu = self.mainWindow.menuBar().addMenu('&Edit')
    self.viewMenu = self.mainWindow.menuBar().addMenu('&View')
    self.toolbarMenu = self.viewMenu.addMenu('&Toolbars')
    self.toolsMenu = self.mainWindow.menuBar().addMenu('&Tools')
    self.helpMenu = self.mainWindow.menuBar().addMenu('&Help')
    self.viewMenuManager = PythonQt.dd.ddViewMenu(self.viewMenu)
    self.toolbarMenuManager = PythonQt.dd.ddViewMenu(self.toolbarMenu)

    self.quitAction = self.fileMenu.addAction('&Quit')
    self.quitAction.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
    self.quitAction.connect('triggered()', self.quit)
    self.fileMenu.addSeparator()

    self.pythonConsoleAction = self.toolsMenu.addAction('&Python Console')
    self.pythonConsoleAction.setShortcut(QtGui.QKeySequence('F8'))
    self.pythonConsoleAction.connect('triggered()', self.showPythonConsole)
    self.toolsMenu.addSeparator()

    helpAction = self.helpMenu.addAction('Online Documentation')
    helpAction.connect('triggered()', self.showOnlineDocumentation)
    self.helpMenu.addSeparator()

    helpKeyboardShortcutsAction = self.helpMenu.addAction('Keyboard Shortcuts')
    helpKeyboardShortcutsAction.connect('triggered()', self.showOnlineKeyboardShortcuts)
    self.helpMenu.addSeparator()

  def quit(self):
    MainWindowApp.applicationInstance().quit()

  def exit(self, exitCode=0):
    MainWindowApp.applicationInstance().exit(exitCode)

  def start(self, enableAutomaticQuit=True, restoreWindow=True):
    if not consoleapp.ConsoleApp.getTestingEnabled() and restoreWindow:
      self.initWindowSettings()
    self.mainWindow.show()
    self.mainWindow.raise_()
    return consoleapp.ConsoleApp.start(enableAutomaticQuit)

  @staticmethod
  def applicationInstance():
    return QtCore.QCoreApplication.instance()

  def showPythonConsole(self):
    applogic.showPythonConsole()

  def showOnlineDocumentation(self):
    QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://openhumanoids.github.io/director/'))

  def showOnlineKeyboardShortcuts(self):
    QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://openhumanoids.github.io/director/user_guide/keyboard_shortcuts.html#director'))

  def showErrorMessage(self, message, title='Error'):
    QtGui.QMessageBox.warning(self.mainWindow, title, message)

  def showInfoMessage(self, message, title='Info'):
    QtGui.QMessageBox.information(self.mainWindow, title, message)

  def wrapScrollArea(self, widget):
    w = QtGui.QScrollArea()
    w.setWidget(widget)
    w.setWidgetResizable(True)
    w.setWindowTitle(widget.windowTitle)
    return w

  def addWidgetToViewMenu(self, widget):
    self.viewMenuManager.addWidget(widget, widget.windowTitle)

  def addViewMenuSeparator(self):
    self.viewMenuManager.addSeparator()

  def addWidgetToDock(self, widget, dockArea, visible=True):
    dock = QtGui.QDockWidget()
    dock.setWidget(widget)
    dock.setWindowTitle(widget.windowTitle)
    dock.setObjectName(widget.windowTitle + ' Dock')
    dock.setVisible(visible)
    self.mainWindow.addDockWidget(dockArea, dock)
    self.addWidgetToViewMenu(dock)
    return dock

  def addToolBar(self, title, area=QtCore.Qt.TopToolBarArea):
    toolBar = QtGui.QToolBar(title)
    toolBar.objectName = toolBar.windowTitle
    self.mainWindow.addToolBar(area, toolBar)
    self.toolbarMenuManager.addWidget(toolBar, toolBar.windowTitle)
    return toolBar

  def addToolBarAction(self, toolBar, text, icon=None, callback=None):
    if isinstance(icon, str):
      icon = QtGui.QIcon(icon)
    action = toolBar.addAction(icon, text)
    if callback:
      action.connect('triggered()', callback)
    return action

  def registerStartupCallback(self, func, priority=1):
    consoleapp.ConsoleApp._startupCallbacks.setdefault(priority, []).append(func)

  def _restoreWindowState(self, key):
    appsettings.restoreState(self.settings, self.mainWindow, key)

  def _saveWindowState(self, key):
    appsettings.saveState(self.settings, self.mainWindow, key)
    self.settings.sync()

  def _saveCustomWindowState(self):
    self._saveWindowState('MainWindowCustom')

  def restoreDefaultWindowState(self):
    self._restoreWindowState('MainWindowDefault')

  def initWindowSettings(self):
    self._saveWindowState('MainWindowDefault')
    self._restoreWindowState('MainWindowCustom')
    self.applicationInstance().connect('aboutToQuit()', self._saveCustomWindowState)


class PluginManagerFactory(object):

  def __init__(self):
    pm = PluginManager()
    self._plugins = pm.load_plugins(suppressErrors=True)
    self.init()

  def init(self):
    # create initXYZ for each plugin
    for plugin in self._plugins:
      init_fcn_name = str('init%s' % plugin.name())
      init_fcn = functools.partial(PluginManagerFactory.initPlugin, plugin)
      setattr(self, init_fcn_name, init_fcn)

  @classmethod
  def initPlugin(cls, plugin, fields):
    # initialize instance of plugin
    app = fields.app if hasattr(fields, 'app') else None
    view = fields.view if hasattr(fields, 'view') else None
    plugin_instance = plugin(app, view)
    return plugin_instance.init(fields)

  def getComponents(self):
    components = dict()
    for plugin in self._plugins:
      components[plugin.name()] = plugin.dependencies()
    return components, []


class BuiltInPluginManagerFactory(PluginManagerFactory):

  def __init__(self):
    director_path = os.path.abspath(os.path.dirname(director.__file__))
    builtin_plugins_path = os.path.join(director_path, 'builtin', 'plugins')
    pm = PluginManager(plugins_path=builtin_plugins_path)
    self._plugins = pm.load_plugins()
    self.init()


class MainWindowAppFactory(object):

  def getComponents(self):
    components = {
      'View' : [],
      'Globals' : [],
      'ObjectModel' : [],
      'GlobalModules' : ['Globals'],
      'ViewBehaviors' : ['View'],
      'AdjustedClippingRange' : ['View'],
      'ViewOptions' : ['View', 'ObjectModel'],
      'MainWindow' : ['View', 'ObjectModel'],
      'MainToolBar' : ['MainWindow']
    }
    disabledComponents = []
    return components, disabledComponents

  def initView(self, fields):
    view = PythonQt.dd.ddQVTKWidgetView()
    applogic._defaultRenderView = view
    applogic.setCameraTerrainModeEnabled(view, True)
    applogic.resetCamera(viewDirection=[-1, -1, -0.3], view=view)
    return FieldContainer(view=view)

  def initGlobals(self, fields):
    try:
      globalsDict = fields.globalsDict
    except AttributeError:
      globalsDict = dict()
    if globalsDict is None:
      globalsDict = dict()
    return FieldContainer(globalsDict=globalsDict)

  def initObjectModel(self, fields):
    om.init()
    objectModel = om.getDefaultObjectModel()
    objectModel.getTreeWidget().setWindowTitle('Scene Browser')
    objectModel.getPropertiesPanel().setWindowTitle('Properties Panel')
    return FieldContainer(objectModel=objectModel)

  def initGlobalModules(self, fields):
    from PythonQt import QtCore, QtGui
    from director import objectmodel as om
    from director import visualization as vis
    from director import applogic
    from director import transformUtils
    from director import filterUtils
    from director import ioUtils
    from director import vtkAll as vtk
    from director import vtkNumpy as vnp
    from director.debugVis import DebugData
    from director.timercallback import TimerCallback
    from director.fieldcontainer import FieldContainer
    import numpy as np
    # create dictionary of modules
    modules = dict(locals())
    del modules['fields']
    del modules['self']
    fields.globalsDict.update(modules)

  def initViewBehaviors(self, fields):
    from director import viewbehaviors
    viewBehaviors = viewbehaviors.ViewBehaviors(fields.view)
    return FieldContainer(viewBehaviors=viewBehaviors)

  def initAdjustedClippingRange(self, fields):
    '''This setting improves the near plane clipping resolution.
    Drake often draws a very large ground plane which is detrimental to
    the near clipping for up close objects.  The trade-off is Z buffer
    resolution but in practice things look good with this setting.'''
    fields.view.renderer().SetNearClippingPlaneTolerance(0.0005)

  def initViewOptions(self, fields):
    viewOptions = vis.ViewOptionsItem(fields.view)
    fields.objectModel.addToObjectModel(viewOptions, parentObj=fields.objectModel.findObjectByName('scene'))
    viewOptions.setProperty('Background color', [0.3, 0.3, 0.35])
    viewOptions.setProperty('Background color 2', [0.95,0.95,1])
    return FieldContainer(viewOptions=viewOptions)

  def initMainWindow(self, fields):
    organizationName = 'RIPL'
    applicationName = 'DirectorMainWindow'
    windowTitle = 'Director Viewer App'
    # use custom params (if passed)
    if hasattr(fields, 'organizationName'):
      organizationName = fields.organizationName
    if hasattr(fields, 'applicationName'):
      applicationName = fields.applicationName
    if hasattr(fields, 'windowTitle'):
      windowTitle = fields.windowTitle
    # set app info
    MainWindowApp.applicationInstance().setOrganizationName(organizationName)
    MainWindowApp.applicationInstance().setApplicationName(applicationName)
    # create main window
    app = MainWindowApp()
    app.mainWindow.setCentralWidget(fields.view)
    app.mainWindow.setWindowTitle(windowTitle)
    app.mainWindow.setWindowIcon(QtGui.QIcon(':/images/drake_logo.png'))
    # browser dock
    sceneBrowserDock = app.addWidgetToDock(
      fields.objectModel.getTreeWidget(),
      QtCore.Qt.LeftDockWidgetArea,
      visible=True
    )
    # properties dock
    propertiesDock = app.addWidgetToDock(
      app.wrapScrollArea(fields.objectModel.getPropertiesPanel()),
      QtCore.Qt.LeftDockWidgetArea,
      visible=True
    )
    # separator
    app.addViewMenuSeparator()
    # ---
    def toggleObjectModelDock():
      newState = not sceneBrowserDock.visible
      sceneBrowserDock.setVisible(newState)
      propertiesDock.setVisible(newState)
    # ---
    applogic.addShortcut(app.mainWindow, 'F1', toggleObjectModelDock)
    # pack everything in a FieldContainer
    return FieldContainer(
      app=app,
      mainWindow=app.mainWindow,
      sceneBrowserDock=sceneBrowserDock,
      propertiesDock=propertiesDock,
      toggleObjectModelDock=toggleObjectModelDock,
      commandLineArgs=args_parser.args()
    )

  def initMainToolBar(self, fields):
    app = fields.app
    toolBar = app.addToolBar('Main Toolbar')
    app.addToolBarAction(toolBar, 'Python Console', ':/images/python_logo.png', callback=app.showPythonConsole)
    toolBar.addSeparator()
    app.addToolBarAction(toolBar, 'Reset Camera', ':/images/reset_camera.png', callback=applogic.resetCamera)
    return FieldContainer(mainToolBar=toolBar)


def construct(globalsDict=None):
  fact = ComponentFactory()
  fact.register(MainWindowAppFactory)
  fact.register(BuiltInPluginManagerFactory)
  fact.register(PluginManagerFactory)
  return fact.construct(globalsDict=globalsDict)


def main(globalsDict=None):
  app = construct(globalsDict)
  # ---
  if globalsDict is not None:
    globalsDict.update(**dict(app))
  # launch app
  app.app.start()


if __name__ == '__main__':
  main(globals())
