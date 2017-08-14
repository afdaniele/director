#include <Python.h>
#include <PythonQt.h>
#include <QApplication>
#include "ddPythonManager.h"
#include "QVTKOpenGLInit.h"

#include "py3main.h"

int main(int argc, char **argv)
{
  QVTKOpenGLInit init;
  QApplication app(argc, argv);
  ddPythonManager* pythonManager = new ddPythonManager;
  PythonQt::self()->addVariable(PythonQt::self()->importModule("sys"), "executable", QCoreApplication::applicationFilePath());
  int result = Py3_Main(argc, argv);

  delete pythonManager;
  return result;
}
