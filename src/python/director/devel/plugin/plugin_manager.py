import os
import uuid
import imp
import traceback
from os.path import isdir, abspath, join, isfile

import director
import director.plugins


def make_id():
  return str(uuid.uuid4())


class PluginLoadException(Exception):

  def __init__(self, message):
    super(PluginLoadException, self).__init__(message)


class PluginManager(object):

  def __init__(self, plugins_path=None, quiet=False):
    self._plugins_path = None
    self.quiet = quiet
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
    if not self.quiet:
      print('PluginManager :: Initialized on directory "%s"' % self._plugins_path)
    # cache
    self._plugins = None

  def list_plugins(self):
    # return cached value if available
    if self._plugins:
      return self._plugins
    # list plugins from disk
    self._plugins = [p for p in os.listdir(self._plugins_path)
      if isfile(join(self._plugins_path, p, '__init__.py'))]
    tot_num_plugins = len(self._plugins)
    # remove disabled plugins
    self._plugins = [p for p in self._plugins
      if not isfile(join(self._plugins_path, p, 'disabled.flag'))]
    # print useful info
    if not self.quiet:
      print(
        'PluginManager :: Found %d plugins (%d disabled)' % (
          tot_num_plugins,
          tot_num_plugins-len(self._plugins)
        )
      )
    # return list of plugins
    return self._plugins

  def load_plugin(self, plugin_id):
    plugin = None
    # make sure this plugin is not registered already
    if hasattr(director.plugins, plugin_id):
      raise PluginLoadException("Two or more plugins tried to register with the same name '%s'" % plugin_id)
    # (try to) load plugin from file
    try:
      # look for the plugin module
      f, filename, description = imp.find_module(
        plugin_id,
        [os.path.join(self._plugins_path)]
      )
      # load module from file
      plugin = imp.load_module(make_id(), f, filename, description)
      # add plugin to director package
      setattr(director.plugins, plugin_id, plugin)
    except Exception as e:
      exception_msg = "\n".join([
        "An error occurred while loading the plugin '%s'.\n" % plugin_id,
        "The error is:\n\t%s.\n" % str(e),
        "The traceback is:\n\t%s" % '\n\t'.join(traceback.format_exc().splitlines())
      ])
      raise PluginLoadException(exception_msg)
    # make sure that this module defines a plugin
    if not hasattr(plugin, 'Plugin') or not issubclass(plugin.Plugin, director.devel.plugin.GenericPlugin):
      plugin_module_file = os.path.join(self._plugins_path, plugin_id, '__init__')+'.py'
      raise PluginLoadException(
        'The plugin module file "%s" does not define a class "Plugin(GenericPlugin)"' % plugin_module_file
      )
    # print info
    if not self.quiet:
      print('PluginManager :: Loaded plugin %s (ID: %s)' % (plugin.Plugin.name(), plugin.Plugin.id()))
    # return loaded plugin
    return plugin.Plugin

  def load_plugins(self):
    plugins = []
    for plugin_id in self.list_plugins():
      try:
        p = self.load_plugin(plugin_id)
      except PluginLoadException as e:
        print('PluginManager :: An error occurred while loading the plugin with ID "%s". The plugin will be disabled.' % (plugin_id))
        continue
      plugins.append(p)
    # return loaded plugins
    return plugins
