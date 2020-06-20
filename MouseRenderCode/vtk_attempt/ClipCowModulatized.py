#!/usr/bin/env python


# In this example vtkClipPolyData is used to cut a polygonal model
# of a cow in half. In addition, the open clip is closed by triangulating
# the resulting complex polygons.

import vtk
from vtk.util.misc import vtkGetDataRoot
from vtk.util.colors import peacock, tomato,green
from Clipping_Functions import make_clipper,make_actors

VTK_DATA_ROOT = vtkGetDataRoot()

# First start by reading a cow model. We also generate surface normals for
# prettier rendering.
cow = vtk.vtkBYUReader()   # Data Source
cow.SetGeometryFileName("cow.g")

#Compute Normals
cowNormals = vtk.vtkPolyDataNormals()
cowNormals.SetInputConnection(cow.GetOutputPort())

plane = vtk.vtkPlane()
plane.SetOrigin(0.25, 0, 0)
plane.SetNormal(0, 1, 0)

clipper=make_clipper(plane,cowNormals)

clipActor,cutActor,restActor = make_actors(plane,clipper,cowNormals,tomato)

# Create graphics stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(clipActor)
ren.AddActor(cutActor)
ren.AddActor(restActor)


ren.SetBackground(1, 1, 1)
ren.ResetCamera()
ren.GetActiveCamera().Azimuth(30)
ren.GetActiveCamera().Elevation(30)
ren.GetActiveCamera().Dolly(1.5)
ren.ResetCameraClippingRange()


renWin.SetSize(300, 300)
iren.Initialize()

# Lets you move the cut plane back and forth by invoking the function
# Cut with the appropriate plane value (essentially a distance from
# the original plane).  This is not used in this code but should give
# you an idea of how to define a function to do this.
def Cut(v):
    clipper.SetValue(v)
    cutEdges.SetValue(0, v)
    cutStrips.Update()
    cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
    cutPoly.SetPolys(cutStrips.GetOutput().GetLines())
    cutMapper.Update()
    renWin.Render()

renWin.Render()
iren.Start()
