class GenericPlugin(object):

  ID = None
  NAME = None
  DEPENDENCIES = []

  def __init__(self, app, view):
    self._app = app
    self._view = view

  @classmethod
  def id(cls):
    return cls.ID

  @classmethod
  def name(cls):
    return cls.NAME

  @classmethod
  def dependencies(cls):
    return cls.DEPENDENCIES

  @property
  def app(self):
    return self._app

  @property
  def view(self):
    return self._view

  def init(self, fields):
    raise NotImplementedError("Every plugin is required to ovveride the method init()")

  def shutdown(self, fields):
    # by default, this method does not do anything
    return
