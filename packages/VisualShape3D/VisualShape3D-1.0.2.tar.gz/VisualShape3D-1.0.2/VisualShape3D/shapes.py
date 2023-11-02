from matplotlib import path 
import numpy as np
from math import *
from .mathutils import get_eps,get_sig_figures

"""
    Rapid creation of 3D polygons of simple shapes
    Shape Functions
         (1) Input a 2D Polygon in yz Plane 
         (2) Move it to a 3D position
"""
def add_col(n, dtype=int):
    """
    It adds a column of length n
    return a column of array.
    """
    return np.reshape(np.arange(n, dtype = dtype), (n, 1))


# 1) To create a dictionary list that holds all arguments 
#      for shapes just inputed.
__shapeInputDicts = []

def  shapeInputDict(each_shape_input):
    __shapeInputDicts.append(each_shape_input)
    return each_shape_input

@shapeInputDict
def dict_rectangle(*args):
    return {"shape":"rectangle","W":args[0],"H":args[1]}

@shapeInputDict
def dict_triangle(*args):
    return {"shape":"triangle","W" : args[0], "H" : args[1], "A" : args[2]}

@shapeInputDict
def dict_rectangleWithHole(*args):
    return {
            "shape":"rectangleWithHole",
            "W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4],
            "D" : args[5]}

@shapeInputDict
def dict_fourSided(*args):
    return {
            "shape":"fourSided","W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4]}

@shapeInputDict
def dict_fiveSided(*args):
    return {
            "shape":"fiveSided","W" : args[0],"W" : args[0],
            "H" : args[1], 
            "A" : args[2],
            "B" : args[3],
            "C" : args[4],
            "D" : args[5]}

@shapeInputDict
def dict_regularPolygon(*args):
    return {
            "n": args[0], 
            "R": args[1],
            "Center": args[2]
            }

@shapeInputDict
def dict_polygon(*args):
    # return np.array(list(map(lambda x:x,args)))
    return  np.array(list(map(lambda x:x,args[0])))


#2) to create vertices (0,y,z) for each shape
# define a function collection
__shapeFunctions = []
def shapeFunction(each_definition_func):
    __shapeFunctions.append(each_definition_func)
    return each_definition_func

@shapeFunction
def rectangle(*args):
    W = args[0]
    H = args[1]
    return np.array([(0,0,0),(0,W,0),(0,W,H),(0,0,H)])

@shapeFunction
def triangle(*args):
    W = args[0]
    H = args[1] 
    A = args[2]
    return np.array([(0,0,0),(0,W,0),(0,A,H)])

@shapeFunction
def rectangleWithHole(*args):
    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    D = args[5]

    if D>0 and C>0 and (A+D)<W and (B+C)<H :
        ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,D,H),(0,D,B+C),(0,D+A,B+C),(0,D+A,C),(0,D,C),(0,D,H),(0,0,H)])

    elif D == 0.0 :
        if C == 0.0 and A < W and B < H :
            ret = np.array([(0,A,0),(0,W,0),(0,W,H),(0,0,H),(0,0,B),(0,A,B)])

        if C != 0.0 and A < W and (B+C) < H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,D,H),(0,D,B+C),(0,D+A,B+C),(0,D+A,C),(0,D,C)])

        if C != 0.0 and A < W and (B+C) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,A,H),(0,A,C),(0,0,C)])


    elif D != 0.0 :
        if C == 0.0 and (D+A) < W and B < H :
            ret = np.array([(0,0,0),(0,D,0),(0,D,B),(0,A+D,B),(0,A+D,0),(0,W,0),(0,W,H),(0,0,H)])
                
        if C != 0.0 and (A+D) < W and (B+C) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,H),(0,A+D,H),(0,A+D,C),(0,D,C),(0,D,H),(0,0,H)])

        if C == 0.0 and (A+D) >= W and B < H :
            ret = np.array([(0,0,0),(0,D,0),(0,D,B),(0,W,B),(0,W,H),(0,0,H)])

        if C != 0.0 and (A+D) >= W and (B+C) < H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,C),(0,D,C),(0,D,B+C),(0,W,B+C),(0,W,H),(0,0,H)])

        if C != 0.0 and (A+D) >= W and (B+C) >= H :
            ret = np.array([(0,0,0),(0,W,0),(0,W,C),(0,D,C),(0,D,H),(0,0,H)])

    else :
        raise ValueError(f"Incorrect inputs : W={W}, H={H}, A={A}, B={B}, C={C}, D={D}")

    return ret

@shapeFunction
def fourSided(*args):
    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    return np.array([(0,0,0),(0,W,0),(0,A+C,H),(0,A,B)])

@shapeFunction
def fiveSided(*args):
    W = args[0]
    H = args[1] 
    A = args[2]
    B = args[3]
    C = args[4]
    D = args[5]
    return np.array([(0,0,0),(0,W,0),(0,W+C,D),(0,A+B,H),(0,A,H)])

@shapeFunction
def regularPolygon(*args):
    if len(args) < 3 :
        raise ValueError("arguments are : n , R, Center ")
        return
    dict_regularPolygon(*args)

    n     = args[0]
    R     = args[1] 
    Center= args[2]

    if n < 3 :
        return

    theta = pi/n
    s = R * sin(theta)
    a = R * cos(theta)

    theta = 2*pi/n
    vertices = []
    for i in range(n):
        angle = i * theta
        x = 0.0
        y = R * cos(angle)
        z = R * sin(angle)
        vertices.append((x,y,z))

    return np.array(vertices)  #,s,a

@shapeFunction
def polygon(*args):
    value = args[0]
    if isinstance(value,list):
        vertices = np.array(value)
    elif isinstance(value,np.ndarray) :
        vertices = value
    else :
        raise ValueError('Shapes.polygon : a list/np.array for vertices is needed !!!')

    dict_polygon(*args)

    if vertices.shape[1] == 2:
    # from Utilities import add_col
        vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))

    # return np.array(list(map(lambda x:x,args)))
    return np.array(vertices)
    

# create a namelist of these function
__shapeNames = [func.__name__ for func in __shapeFunctions ]

def createShape(shapeName,*args):
    name = [x.lower() for x in __shapeNames]
    i = name.index(shapeName.lower())
    __shapeInputDicts[i](*args)
    return __shapeFunctions[i](*args)

def shapes():
    for each in __shapeNames:
        print(each)

def getShapeInputDict(shapeName,*args):
    name = [x.lower() for x in __shapeNames]
    i = name.index(shapeName.lower())
    return __shapeInputDicts[i](*args)

# For a 2D shape created at the initial position,
# one can move it to a desired position by a matrix below
def tranMatrix(alpha, beta):
    al = radians(alpha)
    be = radians(beta)
    X = [cos(be)*cos(al), -sin(al), -sin(be)*cos(al)]
    Y = [cos(be)*sin(al),  cos(al), -sin(be)*sin(al)]
    Z = [sin(be),                0,          cos(be)]
    return np.vstack([X,Y,Z])

# move from the intial position to a desired position
def move(shape = rectangle(1.0,1.0), reference = (0.0,0.0,0.0), to = (0.0,0.0,0.0), by = (30.0,0.0)):
    (alpha, beta) = by
    # Comment them out for fast run
    # if (type(shape) is list) or type(shape) is tuple:
    #     vertices = np.array(shape)
    # elif type(shape) is np.ndarray :
    #     vertices = shape
    # else :
    #     raise ValueError('move() needs a list/np.array for a polygon')

    # print(f" to rotate by {by}")

    vertices = shape
    if vertices.shape[1] == 2:
        vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))
    
    facet = vertices.transpose() 

    R0 = np.array(reference).reshape(-1,1) 
    R1 = np.array(to).reshape(-1,1)
    dR = R1 - R0

    U = tranMatrix(alpha,beta)
    facet_new = U.dot(facet) + dR


    return facet_new.transpose()

def main():
    pass

if __name__ == '__main__':
    main()