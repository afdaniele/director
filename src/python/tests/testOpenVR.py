import vtk
print(vtk.__file__)

def test_openvr():
  renderer =  vtk.vtkOpenVRRenderer()
  renderWindow = vtk.vtkOpenVRRenderWindow()
  iren = vtk.vtkOpenVRRenderWindowInteractor()
  cam = vtk.vtkOpenVRCamera()
  renderer.SetShowFloor(True)

  actor = vtk.vtkActor()
  renderer.SetBackground(0.2, 0.3, 0.4)
  renderWindow.AddRenderer(renderer)
  renderer.AddActor(actor)
  iren.SetRenderWindow(renderWindow)
  renderer.SetActiveCamera(cam)

  #renderer.UseShadowsOn()

  # crazy frame rate requirement
  # need to look into that at some point
  renderWindow.SetDesiredUpdateRate(350.0)
  iren.SetDesiredUpdateRate(350.0)
  iren.SetStillUpdateRate(350.0)

  renderer.RemoveCuller(renderer.GetCullers().GetLastItem())

  light = vtk.vtkLight()
  light.SetLightTypeToSceneLight()
  light.SetPosition(1.0, 1.0, 1.0)
  renderer.AddLight(light)

  fileName = '/home/pat/source/vtk/build/ExternalData/Testing/Data/dragon.ply'

  reader = vtk.vtkPLYReader()
  reader.SetFileName(fileName)

  trans = vtk.vtkTransform()
  trans.Translate(10.0,20.0,30.0)
  trans.Scale(10.0,10.0,10.0)
  tf =  vtk.vtkTransformPolyDataFilter()
  tf.SetTransform(trans)
  tf.SetInputConnection(reader.GetOutputPort())

  mapper = vtk.vtkOpenGLPolyDataMapper()
  mapper.SetInputConnection(tf.GetOutputPort())
  mapper.SetVBOShiftScaleMethod(vtk.vtkOpenGLVertexBufferObject.AUTO_SHIFT_SCALE)
  actor.SetMapper(mapper)
  actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
  actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
  actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
  actor.GetProperty().SetSpecular(0.5)
  actor.GetProperty().SetDiffuse(0.7)
  actor.GetProperty().SetAmbient(0.5)
  actor.GetProperty().SetSpecularPower(20.0)
  actor.GetProperty().SetOpacity(1.0)
  # actor.GetProperty().SetRepresentationToWireframe()

  # the HMD may not be turned on/etc
  renderWindow.Initialize()

  print(renderWindow.ReportCapabilities())
  print('is direct:', renderWindow.IsDirect())
  print('screen size:', renderWindow.GetScreenSize())


  renderer.ResetCamera()
  renderWindow.Render()
  print('calling start')
  iren.Start()
  print('returning!')

if __name__ == '__main__':
  print('main')
  #test_openvr()
