# Read the CSV file and convert the latitude and longitude into x,y-coordinates into Kilometers.
# Anders Hast 5/6-2013 (modified by Fredrik Nysjo 2020)

import vtk

import string
import math
import time


#Read Points
def add_value(probabilities, key):
    if key in probabilities.keys():
        probabilities[key] = probabilities[key] + 1
    else:
        probabilities[key] = 1

def generate_key(x, y, z, max_x, min_x, max_y, min_y, max_z, min_z, density_x, density_y, density_z):
    #print("x_key_________________________")
    x_key = generate_sub_key(x, max_x, min_x, density_x)
    #print("y_key______________________")
    y_key = generate_sub_key(y, max_y, min_y, density_y)
    #print("z_key____________________")
    z_key = generate_sub_key(z, max_z, min_z, density_z)
    return (x_key, y_key, z_key)

def generate_sub_key(value, t_max, t_min, density):
    for nr in range(density):
        if (value >= nr*t_max/density) and (value <= ((nr+1)*t_max/density)+0.001):
            return nr
        else:
            #print("value")
            #print(value)
            #print("lower threshold")
           # print(nr*t_max/density)
            #print("higher threshold")
            #print((nr+1)*t_max/density)
            pass
    assert(False)

def readPoints(file, depth_scaling=0.01, max_x = 47.5837, min_x = 35.1255, max_y = 19.8247, min_y = 5.5433, max_z = 4.991, min_z = 0, density_x = 20, density_y = 10, density_z = 5):
    # Create an array of Points
    points = vtk.vtkPoints()
    # Create arrays of Scalars
    scalars = vtk.vtkFloatArray()
    tid     = vtk.vtkFloatArray()
    depth   = vtk.vtkFloatArray()

    probabilities = {}
    # Initialize
    LatMax=0
    LatMin=360
    LonMax=0
    LonMin=360
    tMin=99999999999999

    # Open the file
    file = open(file)

    # Read one line
    line = file.readline()

    # Loop through lines
    tMin = 1.0e15
    while line:
        # Split the line into data
        data = line.split('|')
        # Skip the commented lines
        if data and data[0][0] != '#':
            # Convert data into float
            #print(data[0], data[1], data[2], data[3], data[4].split('--')[0], data[10])
            date, x, y, z, r = data[1], float(data[2]), float(data[3]),  float(data[4]), float(data[10])
            z_scaled = z * depth_scaling
            key = generate_key(x, y, z_scaled, max_x, min_x, max_y, min_y, max_z, min_z, density_x, density_y, density_z) 
            add_value(probabilities, key)



            row=date.split('T')
            adate=row[0].split('-')
            atime=row[1].split(':')
            temp=atime[2].split('.')
            atime[2]=temp[0]

            if atime[2]=='':
                atime[2]='00'
            t= time.mktime((int(adate[0]),int(adate[1]),int(adate[2]),int(atime[0]),int(atime[1]),int(atime[2]),0,0,0))
            if x > LatMax:
                LatMax=x
            if x< LatMin:
                LatMin=x
            if y > LonMax:
                LonMax=y
            if y< LonMin:
                LonMin=y
            if t< tMin:
                 tMin=t

            # Insert floats into the point array
            
            
            #points.InsertNextPoint(x, y, z_scaled)
            #scalars.InsertNextValue(r)
            #t -= 1467247524.0  #FIXME
            #tid.InsertNextValue(t)
            #depth.InsertNextValue(z_scaled)
        # read next line
        line = file.readline()

    x_step_length = max_x/density_x
    y_step_length = max_y/density_y
    z_step_length = max_z/density_z

    print(x_step_length)
    print(y_step_length)
    print(z_step_length)

    for key, value in probabilities.items():
        points.InsertNextPoint(key[0]*x_step_length, key[1]*y_step_length, key[2]*z_step_length)
        scalars.InsertNextValue(value)
        t -= 1467247524.0  #FIXME
        tid.InsertNextValue(t)
        depth.InsertNextValue(z_scaled*max_z/density_z)

    #print(LatMin, LatMax, LonMin, LonMax)
    #print(probabilities)
    return points, scalars, tid, depth
