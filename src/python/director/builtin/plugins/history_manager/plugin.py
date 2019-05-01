from director.devel.plugin import GenericPlugin
from director.fieldcontainer import FieldContainer

from PythonQt import QtCore, QtGui


class Plugin(GenericPlugin):

  ID = 'history_manager'
  NAME = 'HistoryManager'
  DEPENDENCIES = ['MainWindow']

  def __init__(self, app, view):
    super(Plugin, self).__init__(app, view)

  def init(self, fields):
    # create undo stack/dock
    undoStack = QtGui.QUndoStack()
    undoView = QtGui.QUndoView(undoStack)
    undoView.setEmptyLabel('Start')
    undoView.setWindowTitle('History')
    undoDock = self.app.addWidgetToDock(
      undoView,
      QtCore.Qt.LeftDockWidgetArea,
      visible=False
    )
    # create undo/redo actions
    undoAction = undoStack.createUndoAction(undoStack)
    redoAction = undoStack.createRedoAction(undoStack)
    undoAction.setShortcut(QtGui.QKeySequence('Ctrl+Z'))
    redoAction.setShortcut(QtGui.QKeySequence('Ctrl+Shift+Z'))
    # add actions to menu
    self.app.editMenu.addAction(undoAction)
    self.app.editMenu.addAction(redoAction)
    # ---
    return FieldContainer(
      undoDock=undoDock,
      undoStack=undoStack,
      undoView=undoView,
      undoAction=undoAction,
      redoAction=redoAction
    )
