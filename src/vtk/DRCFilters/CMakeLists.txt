

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

find_package(OpenGL REQUIRED)

find_package(Eigen REQUIRED)
include_directories(${EIGEN_INCLUDE_DIRS})

set(sources
  vtkDepthImageUtils.cxx
  vtkGridSource.cxx
  vtkFrameWidget.cxx
  vtkFrameWidgetRepresentation.cxx
  vtkInteractorStyleTerrain2.cxx
  vtkPickCenteredInteractorStyle.cxx
  )

# extra source files to compile but do not python wrap
set(EXTRA_SRCS
  )

set(VTK_LIBRARIES
  vtkInteractionWidgets
  vtkInteractionStyle
  vtkRenderingFreeType
  vtkRenderingCore
  vtkRendering${VTK_RENDERING_BACKEND}
  vtkFiltersExtraction
  vtkFiltersCore
  vtkCommonCore
  )


set(deps
  ${VTK_LIBRARIES}
  ${OPENGL_LIBRARIES}
  )

set(pkg_deps)

if (USE_DRC)

  # requires libbot, lcm, eigen, drc lcmtypes

  find_package(LibBot REQUIRED MODULE)
  include_directories(${LIBBOT_INCLUDE_DIRS})

  find_package(Eigen REQUIRED)
  include_directories(${EIGEN_INCLUDE_DIRS})

  find_package(LCM REQUIRED)
  include_directories(${LCM_INCLUDE_DIRS})

  list(APPEND sources
    vtkMultisenseSource.cxx
    vtkLidarSource.cxx
  )

  list(APPEND deps
    ${LIBBOT_LIBRARIES}
    ${LCM_LIBRARIES}
  )

  list(APPEND pkg_deps
    drc-lcmtypes lcmtypes_maps
  )

endif()

if (USE_DRC_MAPS)
  find_package(Maps REQUIRED)
  find_package(PCL REQUIRED)

  list(APPEND sources vtkMapServerSource.cxx)
  include_directories(${PCL_INCLUDE_DIRS})
  include_directories(${MAPS_INCLUDE_DIRS})
  list(APPEND deps ${MAPS_LIBRARIES} ${PCL_LIBRARIES})
endif()

if (USE_DRC_PLANE_SEG)
  find_package(PlaneSeg REQUIRED)
  find_package(PCL REQUIRED)

  list(APPEND sources
    vtkPlaneSegmentation.cxx
    vtkRobustNormalEstimator.cxx
    vtkSurfaceFitter.cxx
  )

  include_directories(${PLANE_SEG_INCLUDE_DIRS})
  include_directories(${PCL_INCLUDE_DIRS})
  list(APPEND deps ${PLANE_SEG_LIBRARIES} ${PCL_LIBRARIES})
endif()

if(USE_LCMGL)

  find_package(LibBot REQUIRED MODULE)
  include_directories(${LIBBOT_INCLUDE_DIRS})
  list(APPEND sources vtkLCMGLProp.cxx)
  list(APPEND deps ${LIBBOT_LIBRARIES} ${OPENGL_LIBRARIES})

endif()

if(USE_OCTOMAP)

  setup_qt4()

  find_library(OCTOVIS_LIBRARY octovis)
  list(APPEND sources vtkOctomap.cxx)
  list(APPEND deps ${LIBBOT_LIBRARIES} ${OPENGL_LIBRARIES} ${OCTOVIS_LIBRARY})

  list(APPEND pkg_deps
    lcmtypes_octomap-utils
  )

endif()

if (USE_COLLECTIONS)

  list(APPEND sources vtkCollections.cxx)
  list(APPEND deps ${OPENGL_LIBRARIES})

  list(APPEND pkg_deps
    lcmtypes_visualization
  )
endif()


set(library_name vtkDRCFilters)
add_library(${library_name} ${sources} ${EXTRA_SRCS})
target_link_libraries(${library_name} ${deps})

if(pkg_deps)
  use_pkg(${library_name} ${pkg_deps})
endif()

install(TARGETS ${library_name}
    EXPORT ${DD_TARGETS_NAME}
    RUNTIME DESTINATION ${DD_INSTALL_BIN_DIR}
    LIBRARY DESTINATION ${DD_INSTALL_LIB_DIR}
    ARCHIVE DESTINATION ${DD_INSTALL_LIB_DIR})

if(NOT VTK_WRAP_PYTHON)
  message(FATAL_ERROR "VTK was compiled without Python support. "
    "VTK_WRAP_PYTHON is OFF. You must use a version of VTK with Python. "
    "VTK_DIR is: ${VTK_DIR}")
endif()

include_directories(${PYTHON_INCLUDE_DIR})
include(${CMAKE_SOURCE_DIR}/cmake/wrap-python.cmake)
wrap_python(${library_name} "${sources}")
set_target_properties(${library_name}Python
  PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${DD_INSTALL_PYTHON_DIR}/director")
target_link_libraries(${library_name}Python ${PYTHON_LIBRARIES})
target_link_libraries(${library_name}PythonD ${PYTHON_LIBRARIES})


add_executable(TestOpenVR TestOpenVR.cxx)
target_link_libraries(TestOpenVR vtkRenderingOpenVR ${deps} vtkRenderingGL2PSOpenGL2 vtkIOPLY)
