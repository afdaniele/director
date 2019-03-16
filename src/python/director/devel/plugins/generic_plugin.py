class GenericPlugin(object):

  def __init__(self, app, view):
    self._app = app
    self._view = view

  def app(self):
    return self._app

  def view(self):
    return self._view

  def init(self):
    raise NotImplementedError("Every plugin is required to ovveride the method init()")

  def shutdown(self):
    # by default, this method does not do anything
    return
