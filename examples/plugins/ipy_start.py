import director
from director.devel.plugins import PluginManager



pm = PluginManager()

g = pm.list_all_plugins()

print director.devel.plugins.core


# from director_plugin_geometry import LineRenderer
# p = LineRenderer(1, 1, 1, 1)
