from os.path import join
import networkx as nx
from utils import ProgressBar, FileReader

ENVIRONMENT = "director"
DATA_DIR = "/code/dependencies_analysis/data"
ALLOWED_SOURCE_PKG = None
ALLOWED_TARGET_PKG = [
  "/code/director/src/python",
  "/usr/lib/python2.7",
	"/usr/lib/python2.7/dist-packages",
	"/usr/local/lib/python2.7/dist-packages"
	"/usr/local/lib/python2.7/site-packages"
]
ENTRYPOINT_PKG = "/code/director_entrypoint"
PLUGINS_PKG = "/code/director_plugins"

def file_path(file_id):
  return join(DATA_DIR, ENVIRONMENT, file_id)

def cut_zero_in_degree_nodes(G, packages):
  cut = []
  for n in G.in_degree_iter():
    if n[1] == 0:
      parts = n[0].split('/')
      pack_id = int(parts[0][1:])
      if pack_id in [packages[ENTRYPOINT_PKG], packages[PLUGINS_PKG]]: continue
      cut.append(n[0])
      G.remove_node(n[0])
  return cut

def main():
  all, dependencies, errors = [], [], []
  for section in ["director", "entrypoint", "plugins"]:
    files_to_load = ['all_imports.list', 'dependencies.list', 'import_errors.list']
    data = []
    for file in files_to_load:
      fname = '_'.join([section, file])
      fr = FileReader(file_path(fname))
      print "Loading file '%s'... " % fname,
      data.append(fr.lines())
      print "Done!"
    # unpack data
    sec_all, sec_dependencies, sec_errors = data
    # extend data
    all.extend(sec_all)
    dependencies.extend(sec_dependencies)
    errors.extend(sec_errors)
  # filter dependencies
  packages = {
    ENTRYPOINT_PKG : 0,
    PLUGINS_PKG : 1
  }
  pbar = ProgressBar(len(dependencies))
  G = nx.DiGraph()
  excluded_source = set()
  excluded_target = set()
  print "Processing dependencies... ",
  for dep in dependencies:
    # convert string -> tuple
    dep = eval(dep)
    source, target = dep
    pbar.next()
    # ignore package if not allowed
    if ALLOWED_SOURCE_PKG and source[0] not in ALLOWED_SOURCE_PKG:
      excluded_source.add(source[0])
      continue
    if ALLOWED_TARGET_PKG and target[0] not in ALLOWED_TARGET_PKG:
      excluded_target.add(target[0])
      continue
    # get source package id
    source_pkg_id = len(packages)
    if source[0] in packages:
      source_pkg_id = packages[source[0]]
    else:
      packages[source[0]] = source_pkg_id
    # get target package id
    target_pkg_id = len(packages)
    if target[0] in packages:
      target_pkg_id = packages[target[0]]
    else:
      packages[target[0]] = target_pkg_id
    # create unique ID for file
    source = 'P%d/%s' % (source_pkg_id, source[1])
    target = 'P%d/%s' % (target_pkg_id, target[1])
    # add dependency edge to the graph
    G.add_edge(source, target)
  # print excluded
  print "Excluded sources: %d" % len(excluded_source)
  for p in excluded_source:
    print "\t%s" % p
  print ""
  print "Excluded targets: %d" % len(excluded_target)
  for p in excluded_target:
    print "\t%s" % p
  print ""
  # print packages
  print "Packages:"
  for p,i in packages.items():
    print "\tP%d : %s" % (i,p)
  print ""
  # print stats
  print nx.info(G)
  print "Nodes with self-loops:"
  for n in G.nodes_with_selfloops():
    print "\t"+str(n)
  print ""

  print "Trimming nodes:"
  step = 1
  files_to_remove = []
  cut = cut_zero_in_degree_nodes(G, packages)
  while len(cut) > 0:
    files_to_remove.extend(cut)
    print "Step %d. Pruned %d nodes." % (step, len(cut))
    print "Modules pruned:"
    print "\t" + "\n\t".join(cut)
    print "Graph stats:"
    print nx.info(G)
    step += 1
    cut = cut_zero_in_degree_nodes(G, packages)

  # print stats
  print "Graph pruned!"
  print nx.info(G)

  dot = nx.nx_pydot.to_pydot(G)

  # print dir(dot)
  # pos = nx.nx_pydot.graphviz_layout(G) #nx.kamada_kawai_layout(G)

  # dot.set_layout(pos)

  # with open(join(DATA_DIR, 'graph.dot'), "wb") as fo:
  #   # fo.write(dot)
  #   fo.write(pos)


  # dot.set_size(2000, 2000)
  # dot.set_nodesep(20)
  # # dot.set_ranksep(20)
  #
  # dot.write_pdf( join(DATA_DIR, 'graph.pdf'), prog='neato' )


  nx.drawing.nx_pydot.write_dot(G, join(DATA_DIR, 'graph.dot'))


  print "Files we can remove:"
  pkg_id_to_pkg_path = { v : k for k,v in packages.items() }
  for f in files_to_remove:
    parts = f.split('/')
    pack_id = int(parts[0][1:])
    pack_path = pkg_id_to_pkg_path[pack_id]
    print "\t%s" % join(pack_path, "/".join(parts[1:]))


if __name__ == '__main__':
  main()
