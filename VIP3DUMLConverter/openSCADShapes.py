from __future__ import division
import os, sys, re

from solid import *
from solid.utils import *
from math import *


def triangle(a, b, angle, height=3, heights=None,
             center=None, centerXYZ=[False,False,False]):


    angle = radians(angle)
    # Calculate Heights at each point
    heightAB = (height if (heights==None) else heights[0])/2
    heightBC = (height if (heights==None) else heights[1])/2
    heightCA = (height if (heights==None) else heights[2])/2
    centerZ = 0 if (center or (center==None and centerXYZ[2])) else max(heightAB,heightBC,heightCA)

    #Calculate Offsets for centering
    offsetX =  ((cos(angle)*a)+b)/3 if (center or (center==None and centerXYZ[0])) else 0
    offsetY =  (sin(angle)*a)/3 if  (center or (center==None and centerXYZ[1])) else 0


    pointAB1 = [-offsetX,-offsetY, centerZ-heightAB]
    pointAB2 = [-offsetX,-offsetY, centerZ+heightAB]
    pointBC1 = [b-offsetX,-offsetY, centerZ-heightBC]
    pointBC2 = [b-offsetX,-offsetY, centerZ+heightBC]
    pointCA1 = [(cos(angle)*a)-offsetX,(sin(angle)*a)-offsetY, centerZ-heightCA]
    pointCA2 = [(cos(angle)*a)-offsetX,(sin(angle)*a)-offsetY, centerZ+heightCA]

    return polyhedron(
            points=[	pointAB1, pointBC1, pointCA1,
                        pointAB2, pointBC2, pointCA2 ],
            triangles=[	
                    [0, 1, 2],
                    [3, 5, 4],
                    [0, 3, 1],
                    [1, 3, 4],
                    [1, 4, 2],
                    [2, 4, 5],
                    [2, 5, 0],
                    [0, 5, 3] ]
            )

def generate_solid_arrow (height):
    half_arrow = triangle(a = height, b = height, angle = 90, centerXYZ = [False, False, True])

    full_arrow = union () ((rotate(a = 180, v = RIGHT_VEC)(half_arrow)), half_arrow)
    
    arrow = rotate(a = 180, v = UP_VEC) (left(2.5)((rotate(a = 180, v = RIGHT_VEC)(full_arrow))))

    return arrow

def generate_diamond (height):
    quarter_diamond = triangle(a = height, b = (1.33*height), angle = 90, centerXYZ = [False, False, True])

    half_diamond = union () ((rotate(a = 180, v = RIGHT_VEC)(quarter_diamond)), quarter_diamond)

    diamond = right(1.33*height)(union ()((rotate(a = 180, v = FORWARD_VEC)(half_diamond)), half_diamond))

    return diamond

def dashed_line (line_length):
        l = line_length
        slab = cube([l,2, 3], center = False)
        dashes = []
        for i in range (10):
                dash =  translate([((i/10)*l),0,0])(
                cube([3, 2, 4], center = False))
                dashes.append(dash)
        final_product = union() (dashes, slab)
        return rotate(a = 90, v = UP_VEC)(final_product)
