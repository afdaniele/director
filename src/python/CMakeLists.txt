set(python_files
  director/__init__.py
  director/applogic.py
  director/appsettings.py
  director/botspy.py
  director/callbacks.py
  director/cameracontrol.py
  director/componentgraph.py
  director/consoleapp.py
  director/debugVis.py
  director/args_parser.py
  director/fieldcontainer.py
  director/filterUtils.py
  director/frameupdater.py
  director/geometryencoder.py
  director/ioUtils.py
  director/mainwindowapp.py
  director/objectmodel.py
  director/openscope.py
  director/pointpicker.py
  director/propertyset.py
  director/shallowCopy.py
  director/simpletimer.py
  director/timercallback.py
  director/transformUtils.py
  director/uuidutil.py
  director/viewbehaviors.py
  director/viewcolors.py
  director/vieweventfilter.py
  director/visualization.py
  director/vtkAll.py
  director/vtkNumpy.py

	# director devel
	director/devel/__init__.py
	director/devel/plugin/__init__.py
	director/devel/plugin/generic_plugin.py
	director/devel/plugin/plugin_manager.py

	# director plugins (placeholder package)
	director/plugins/__init__.py

	# built-in plugins: camera_bookmarks
	director/builtin/plugins/camera_bookmarks/__init__.py
	director/builtin/plugins/camera_bookmarks/plugin.py
	director/builtin/plugins/camera_bookmarks/lib/__init__.py
	director/builtin/plugins/camera_bookmarks/lib/camerabookmarks.py

	# built-in plugins: camera_control_panel
	director/builtin/plugins/camera_control_panel/__init__.py
	director/builtin/plugins/camera_control_panel/plugin.py
	director/builtin/plugins/camera_control_panel/lib/__init__.py
	director/builtin/plugins/camera_control_panel/lib/cameracontrolpanel.py

	# built-in plugins: grid
	director/builtin/plugins/grid/__init__.py
	director/builtin/plugins/grid/plugin.py

	# built-in plugins: history_manager
	director/builtin/plugins/history_manager/__init__.py
	director/builtin/plugins/history_manager/plugin.py

	# built-in plugins: measurement_tool
	director/builtin/plugins/measurement_tool/__init__.py
	director/builtin/plugins/measurement_tool/plugin.py
	director/builtin/plugins/measurement_tool/lib/__init__.py
	director/builtin/plugins/measurement_tool/lib/measurementpanel.py
	director/builtin/plugins/measurement_tool/lib/uipanel.py

	# built-in plugins: mesh_loader
	director/builtin/plugins/mesh_loader/__init__.py
	director/builtin/plugins/mesh_loader/plugin.py
	director/builtin/plugins/mesh_loader/lib/__init__.py
	director/builtin/plugins/mesh_loader/lib/opendatahandler.py

	# built-in plugins: output_console
	director/builtin/plugins/output_console/__init__.py
	director/builtin/plugins/output_console/plugin.py
	director/builtin/plugins/output_console/lib/__init__.py
	director/builtin/plugins/output_console/lib/outputconsole.py

	# built-in plugins: screen_grabber
	director/builtin/plugins/screen_grabber/__init__.py
	director/builtin/plugins/screen_grabber/plugin.py
	director/builtin/plugins/screen_grabber/lib/__init__.py
	director/builtin/plugins/screen_grabber/lib/screengrabberpanel.py

	# built-in plugins: script_loader
	director/builtin/plugins/script_loader/__init__.py
	director/builtin/plugins/script_loader/plugin.py

	# built-in plugins: terrain_mode
	director/builtin/plugins/terrain_mode/__init__.py
	director/builtin/plugins/terrain_mode/plugin.py

	# tasks
  director/tasks/__init__.py
  director/tasks/robottasks.py
  director/tasks/taskmanagerwidget.py
  director/tasks/taskuserpanel.py
  director/tasks/descriptions/__init__.py
  director/tasks/descriptions/drillTask.py
  director/tasks/descriptions/taskLibrary.py

  director/thirdparty/__init__.py
  director/thirdparty/qhull_2d.py
  director/thirdparty/min_bounding_rect.py
  director/thirdparty/NumericStringParser.py
  director/thirdparty/numpyjsoncoder.py
  director/thirdparty/transformations.py
  director/thirdparty/conversions.py
  director/thirdparty/geometry_msgs_mock.py
  director/thirdparty/naming.py
  director/thirdparty/osm_utils.py
  director/thirdparty/pysdf.py
  director/thirdparty/toposort.py

  urdf_parser_py/__init__.py
  urdf_parser_py/sdf.py
  urdf_parser_py/urdf.py
  urdf_parser_py/xml_reflection/__init__.py
  urdf_parser_py/xml_reflection/basics.py
  urdf_parser_py/xml_reflection/core.py
)


set(python_module_dir "${CMAKE_BINARY_DIR}/${DD_INSTALL_PYTHON_DIR}")

# Copy python files
set(copied_python_files)
foreach(file ${python_files})
  set(src "${CMAKE_CURRENT_SOURCE_DIR}/${file}")
  set(tgt "${python_module_dir}/${file}")
  get_filename_component(tgtDir ${tgt} PATH)
  get_filename_component(tgtExt ${tgt} EXT)
  get_filename_component(tgt_we ${tgt} NAME_WE)

  file(MAKE_DIRECTORY ${tgtDir})

  if(${tgtExt} STREQUAL ".py.in")
    set(tgt "${tgtDir}/${tgt_we}.py")
    configure_file(${src} ${tgt} @ONLY)
  else()
    add_custom_command(DEPENDS ${src}
                       COMMAND ${CMAKE_COMMAND} -E copy ${src} ${tgt}
                       OUTPUT ${tgt}
                       COMMENT "source copy")
  endif()


  set(copied_python_files ${copied_python_files} ${tgt})
  get_filename_component(installDirSuffix ${file} PATH)
  install(FILES ${tgt} DESTINATION ${DD_INSTALL_PYTHON_DIR}/${installDirSuffix} COMPONENT Runtime)
endforeach(file)


# Byte compile python files
set(compile_all_script "${CMAKE_CURRENT_BINARY_DIR}/compile_all.py")
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/compile_all.py.in"
               ${compile_all_script}
               @ONLY IMMEDIATE)

add_custom_command(
  COMMAND ${PYTHON_EXECUTABLE}
  ARGS  "${compile_all_script}"
  DEPENDS ${copied_python_files}  ${compile_all_script}
  OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/compile_complete"
)

add_custom_target(python_byte_compile ALL DEPENDS "${CMAKE_CURRENT_BINARY_DIR}/compile_complete")

add_subdirectory(extensions)
add_subdirectory(tests)
