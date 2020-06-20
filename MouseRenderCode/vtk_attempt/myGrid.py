#!/usr/bin/env python

"""
This example shows how to create an unstructured grid.
"""

import vtk
import numpy as np
import pickle as pkl

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

    for index in range(len(indices)):
        x=Data['points_'+str(index)]
        triangles = Data['triangles_'+str(index)]
        print(index,x.shape, triangles.shape,'\r',end='')

        points = vtk.vtkPoints()
        for i in range(0, x.shape[0]):
            points.InsertPoint(i, x[i,:])

        ugrid = vtk.vtkUnstructuredGrid()
        ugrid.Allocate(triangles.shape[0])
        for i in range(triangles.shape[0]):
            ugrid.InsertNextCell(vtk.VTK_TRIANGLE, 3, triangles[i,:])

        ugrid.SetPoints(points)


        uGridNormals = vtk.vtkPolyDataNormals()
        uGridNormals.SetInputData(ugrid)
        uGridNormals.SetFeatureAngle(30.0)

        #uGridNormals.ComputePointNormalsOn()
        uGridNormals.SplittingOn()

        print(uGridNormals)
        uGridNormals.Update()  # causes an error

        normalsPolyData = vtk.vtkPolyData()
        normalsPolyData.DeepCopy(uGridNormals.GetOutput())
        
        ugridMapper = vtk.vtkPolyDataMapper()
        ugridMapper.SetInputData(normalsPolyData)
        ugridMapper.ScalarVisibilityOff()
        
        # ugridMapper = vtk.vtkDataSetMapper()
        # ugridMapper.SetInputData(ugrid)

        ugridActor = vtk.vtkActor()
        ugridActor.SetMapper(ugridMapper)
        # print(index,indices[index],struct_D[indices[index][0]])
        color = struct_D[indices[index][0]]
        ugridActor.GetProperty().SetDiffuseColor(colors.GetColor3d(color))
        ugridActor.GetProperty().SetDiffuse(.7)
        ugridActor.GetProperty().SetSpecularPower(20)
        ugridActor.GetProperty().SetSpecular(.5)
         
        ugridActor.GetProperty().EdgeVisibilityOff()
        ugridActor.GetProperty().SetOpacity(0.5)
        ugridActor.GetProperty().SetInterpolationToGouraud()

        renderer.AddActor(ugridActor)
        break

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
