from . import GenericPlugin

class MenuItemPlugin(GenericPlugin):

    def __init__(self, app, view):
      super().__init__(app, view)

    def init(self):
      print "Initialized!"
