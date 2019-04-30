import os
import uuid
import importlib
import traceback
from os.path import isdir, abspath, join, isfile

import director

def make_id():
  return str(uuid.uuid4())

class PluginLoadException(Exception):

  def __init__(self, message):
    super(PluginLoadException, self).__init__(message)


class PluginManager(object):

  def __init__(self, plugins_path=None):
    self._plugins_path = None
    # use custom path if it exists
    if plugins_path:
      plugins_path = abspath(plugins_path)
      if isdir(plugins_path):
        self._plugins_path = plugins_path
    # check if the envirnment variable is set (if necessary)
    if not self._plugins_path:
      if 'DIRECTOR_PLUGINS_DIR' not in os.environ:
        raise ValueError("The environment variable 'DIRECTOR_PLUGINS_DIR' is not set.")
      # set plugin path
      self._plugins_path = abspath(os.environ['DIRECTOR_PLUGINS_DIR'])
    # check if the path exists
    if not isdir(self._plugins_path):
      raise ValueError("The plugins path '%s' does not exist." % plugins_path)
    # print useful info
    print('PluginManager :: Initialized on directory "%s"' % self._plugins_path)
    # cache
    self._plugins = None

  def list_plugins(self):
    # return cached value if available
    if self._plugins:
      return self._plugins
    # list plugins from disk
    self._plugins = [p for p in os.listdir(self._plugins_path)
      if isfile(join(self._plugins_path, p, '__init__.py'))
      and isfile(join(self._plugins_path, p, 'plugin.py'))]
    # print useful info
    print('PluginManager :: Found %d plugins' % len(self._plugins))
    # return list of plugins
    return self._plugins

  def load_plugin(self, plugin_id):
    plugin = None
    # (try to) load plugin from file
    try:
      plugin = importlib.machinery.SourceFileLoader(
        make_id(),
        os.path.join(self._plugins_path, plugin_id, 'plugin')+'.py'
        ).load_module();
    except Exception as e:
      exception_msg = "\n".join([
        "An error occurred while loading the plugin '%s'.\n" % plugin_id,
        "The error is:\n\t%s.\n" % str(e),
        "The traceback is:\n\t%s" % '\n\t'.join(traceback.format_exc().splitlines())
      ])
      raise PluginLoadException(exception_msg)
    # make sure that this module defines a plugin
    if not hasattr(plugin, 'Plugin') or not issubclass(plugin.Plugin, director.devel.plugin.GenericPlugin):
      raise PluginLoadException(
        'The plugin file "%s/%s.py" does not define a class "Plugin(GenericPlugin)"' % (plugin_id, 'plugin')
      )
    print('PluginManager :: Loaded plugin %s (ID: %s)' % (plugin.Plugin.name(), plugin.Plugin.id()))
    # return loaded plugin
    return plugin.Plugin

  def load_plugins(self):
    plugins = []
    for plugin_id in self.list_plugins():
      p = self.load_plugin(plugin_id)
      plugins.append(p)
    # return loaded plugins
    return plugins
