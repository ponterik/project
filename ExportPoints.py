import vtk
import os
import sys
import numpy as np

# Change working directory to allow script to be run from the ParaView shell
datapath = os.path.dirname(os.path.abspath(__file__))
os.chdir(datapath)

# This should allow modules to be imported correctly in the ParaView shell
sys.path.append(datapath)
from ReadPointsCSV import readPoints
#if using python from pandas, uncomment line below and comment line above
#from ReadPoints3 import readPoints

# Read the data in CSV format
filename = "data_365days.txt"
points, scalars, tid, depth = readPoints(filename)
print(tid)
scalars.SetName("magnitude")
tid.SetName("time")
depth.SetName("depth")
data = vtk.vtkPolyData()
print(points)
data.SetPoints(points)
data.GetPointData().AddArray(scalars)
data.GetPointData().AddArray(tid)
data.GetPointData().AddArray(depth)
data.GetPointData().SetActiveScalars("magnitude")

# Write data to VTK legacy format that Paraview can import
writer = vtk.vtkPolyDataWriter()
writer.SetFileName("earthquake365_points.vtk")
writer.SetFileTypeToBinary()
writer.SetInputData(data)
writer.Write()
