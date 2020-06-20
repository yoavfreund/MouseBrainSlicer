#!/usr/bin/env python

"""
This example shows how to create an unstructured grid.
"""

import vtk
import numpy as np
import pickle as pkl
from vtk.util.colors import peacock, tomato,green
from Clipping_Functions import make_clipper,make_actors

colors_list = pkl.load(open('permuted_colors.pkl','rb'))
meta = pkl.load(open('v_atlas/meta_information.pkl','rb'))

def main():
    colors = vtk.vtkNamedColors()

    Data=np.load('tessaltions_compressed.npz')

    indices=meta['sorted_keys']
    struct_D={}                 # a mapping of structure names to colors.
    for i,s in enumerate(set([x[0] for x in indices])):
        struct_D[s]=colors_list[i]
    
    renderer = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    #Clipping plane
    # We clip with an implicit function. Here we use a plane positioned near
    # the center of the cow model and oriented at an arbitrary angle.
    plane = vtk.vtkPlane()
    plane.SetOrigin(300, 300, 300)
    plane.SetNormal(0, -1, 0)
    
    for index in range(len(indices)):
        x=Data['points_'+str(index)]
        triangles = Data['triangles_'+str(index)]
        print(index,x.shape, triangles.shape,'\r',end='')
        
        points = vtk.vtkPoints()
        #print(np.min(x,axis=0),np.max(x,axis=0))

        for i in range(0, x.shape[0]):
            points.InsertPoint(i, x[i,:])

        ugrid = vtk.vtkPolyData()
        ugrid.Allocate(triangles.shape[0])
        for i in range(triangles.shape[0]):
            ugrid.InsertNextCell(vtk.VTK_TRIANGLE, 3, triangles[i,:])

        ugrid.SetPoints(points)

        uGridNormals = vtk.vtkPolyDataNormals()
        uGridNormals.SetInputData(ugrid)
        #uGridNormals.SetFeatureAngle(30.0)

        #uGridNormals.ComputePointNormalsOn()
        #uGridNormals.SplittingOn()

        uGridNormals.Update()  # causes an error

        #normalsPolyData = vtk.vtkPolyData()
        #normalsPolyData.DeepCopy(uGridNormals.GetOutput())

        # vtkClipPolyData requires an implicit function to define what it is to
        # clip with. Any implicit function, including complex boolean combinations
        # can be used. Notice that we can specify the value of the implicit function
        # with the SetValue method.
        clipper=make_clipper(plane,uGridNormals)

        color_name = struct_D[indices[index][0]]
        color=colors.GetColor3d(color_name)
        clipActor,cutActor,restActor = make_actors(plane,clipper,uGridNormals,color)

        #### Start of Change
        # ugridMapper = vtk.vtkPolyDataMapper()
        # ugridMapper.SetInputData(uGridNormals.GetOutput())
        # ugridMapper.ScalarVisibilityOff()
        
        # ugridActor = vtk.vtkActor()
        # ugridActor.SetMapper(ugridMapper)
        # # print(index,indices[index],struct_D[indices[index][0]])
        # color = struct_D[indices[index][0]]
        # ugridActor.GetProperty().SetDiffuseColor(colors.GetColor3d(color))
        # ugridActor.GetProperty().SetDiffuse(.7)
        # ugridActor.GetProperty().SetSpecularPower(5)
        # ugridActor.GetProperty().SetSpecular(.2)
         
        # #ugridActor.GetProperty().EdgeVisibilityOff()
        # ugridActor.GetProperty().SetOpacity(0.5)
        # #ugridActor.GetProperty().SetInterpolationToGouraud()

        # renderer.AddActor(ugridActor)
        renderer.AddActor(clipActor)
        renderer.AddActor(cutActor)
        renderer.AddActor(restActor)

        #### End of change
        
    renderer.SetBackground(colors.GetColor3d('Beige'))

    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(60.0)
    renderer.GetActiveCamera().Azimuth(30.0)
    renderer.GetActiveCamera().Dolly(1.2)

    renWin.SetSize(640, 480)

    # Interact with the data.
    renWin.Render()

    iren.Start()


if __name__ == "__main__":
    main()
