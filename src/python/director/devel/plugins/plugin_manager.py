import os
import imp
import traceback
from os.path import isdir, abspath, join, isfile

import director

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
      raise ValueError("The path '%s' does not exist." % plugins_path)
    # print useful info
    print('PluginManager :: Initialized on directory "%s"' % self._plugins_path)
    # cache
    self._packages = None
    self._plugins = None

  def list_packages(self):
    # return cached value if available
    if self._packages:
      return self._packages
    # list packages from disk
    self._packages = [p for p in os.listdir(self._plugins_path)
      if isfile(join(self._plugins_path, p, '__init__.py'))]
    # print useful info
    print('PluginManager :: Found %d plugin packages' % len(self._packages))
    # return list of packages
    return self._packages

  def list_all_plugins(self):
    # return cached value if available
    if self._plugins:
      return self._plugins
    # list plugins from disk
    for package in self.list_packages():
      # define plugin package name
      plugin_pkg_dir = join(self._plugins_path, package)
      pkg_name = 'director_plugin_%s' % package.lower()
      # load plugin
      try:
        pkg = imp.load_package(pkg_name, plugin_pkg_dir)

        setattr(director.devel.plugins, package, pkg)

      except Exception as e:
        exception_msg = "\n".join([
          "An error occurred while loading the plugin '%s'.\n" % package,
          "The error is:\n\t%s.\n" % e.message,
          "The traceback is:\n\t%s" % '\n\t'.join(traceback.format_exc().splitlines())
        ])
        raise PluginLoadException(exception_msg)
