# from __future__ import absolute_import
import warnings
from matplotlib import path 
import numpy as np
import math
from .mathutils import get_eps,get_sig_figures

### Computation on the intersection of 3D Lines and 3D Polygons
'''
    All vertices follow the form of numpy.array(N,3)
'''
# Vectors

warnings.simplefilter(action='ignore', category=FutureWarning)

def array_to_tuple(array): # two dimensional tuple
    return tuple([tuple(e) for e in array])

def Repmat(M,m,n):          # matlab alternative to broadcasting of Python
    return np.tile(M,(m,n)) 

def Array(x):
    return np.array(x)

def Matrix(x):
    return np.matrix(x)

def MatShape(v):
    ret = v.shape
    n = len(v)
    if len(ret) == 1:
        ret = (1,n)
    return ret
    
def Cross(u,v):
    return np.cross(u,v)

def Dot(u,v):
    return np.dot(u,v)

# M --- np.array or np.matrix
def Inv(M):
    return np.linalg.inv(M)

def Det(M):
    return np.linalg.det(M)

# Fast Version
def Length(v):
    with warnings.catch_warnings():
        # warnings.filterwarnings('error')
        np.seterr(all='raise')
        try:
            answer = np.sqrt(v.dot(v))
        except Warning as e:
            print(f' error found in Length() : {e}:')
            print(f" The vector is given as {v}")
    return answer
    # return np.sqrt(v.dot(v))

def UnitVector(v): 
    return v/Length(v)   

def Mask(v,bSelected):
    """
    It returns an array made of elements selected ( bSelected == True ).
    """
    P = np.array(v)
    return P[bSelected]

# To check whether the two vectors are equal. If they are,  it returns True
def Equal(a,b):
    return np.all(Round(a)==Round(b))

def Round(x):
    return np.round(x, get_sig_figures())

def ScalarEqual(a,b):
    return Round(abs(a-b))<=get_eps()

def ScalarZero(x):
    return ScalarEqual(x,get_eps())

# Vertices 
def Vertices(x):
    return Array(x)


# 3D Line  

def LineXLine(P1,L1,P2,L2):
    '''
         Intersection of two 3D Lines decribed as (P,L) .
         It returns,  
         (1)     P     , the intersection point;
         (2) 'parallel', they are in parallel; 
         (3) 'colinear', they are one; 
         (4) 'skrew' they are skrew in 3D space.
    '''
    # Normalize them
    A,B = Array(L1), Array(L2)
    C,D = Array(P1), Array(P2)
    CD = D - C

    E = UnitVector(A)
    F = UnitVector(B)

    X = Cross(F,CD)
    Y = Cross(F, E)

    # To check if they are zeros
    if(np.linalg.norm(X) <= get_eps() and np.linalg.norm(Y)  <= get_eps()):
        return 'colinear'

    else:
        if((np.linalg.norm(Y)) <= get_eps() ):
            return 'parallel'
        else  :
            Z = Dot(X,Y)
            sign = 1 if Z>0 else -1
            M = C + sign * Length(X)/Length(Y) * E
            if PointInLine(M,P1,L1) == False or PointInLine(M,P2,L2) == False:
                return 'skrew'
            else:
                return tuple(M)

def NormalToLine(P0,P,L):
    '''
        return a line from P0 and perpendicular to (P,L) 
        a vertical plane (R0, n) to the line (P,L)
        return the direction of line from P0 to R
            R intersection point
    '''
    R0 = Array(P0)
    n  = Array(L)

    R = LineXPlane(P,L,R0,n)
    if type(R) is np.ndarray :
        dR = R - R0
        return UnitVector(dR),R
    else :
        return None,None

def PointInLine(P0,P,L):
    # To check if the point P0 is on the 3D line(P,L), Ture/False
    V0 = Array(P0)
    V  = Array(P)

    if Equal(V0,V) :
        return True

    L1 = UnitVector( V0 - V )
    Lx = UnitVector(Array(L))
    if Equal(L1, Lx) or Equal(L1, (-1)*Lx):
        return True
    else:
        return False

def PointInSegment(P,P1,P2):
    # To check if P is inside a segment(P1,P2), Ture/False

    pos = np.vstack((P1, P2))
    pos = np.array([np.min(pos[ :, :], axis=0),
                    np.max(pos[ :, :], axis=0)])

    if type(P) is not np.ndarray:
        P = Array(P)
        
    return np.all(P>=pos[0,:]) & np.all(P<=pos[1,:])

def CreateCoordinates(L1,L2):
    # Create a local coordinate system according to two directions.
    a = Array(L1)
    b = Array(L2)
    c = Cross(a, b)
    b = Cross(c, a)

    z = Round(UnitVector(c))
    x = Round(UnitVector(a))
    y = Round(UnitVector(b))
    return x,y,z

def AngleBetween(A,B):
    # Angle between two lines
    u,v = Array(A), Array(B)
    a,b = Length(u), Length(v)
    rad = math.acos( Dot(u,v)/(a*b) )%math.pi
    deg = math.degrees(rad)%180
    return rad, deg

# 3D Plane and Polygons
'''
   Core concern : intersection. 
   That is, a line of slop (L) from a point (P0) is intercepted with a Polygon.
   The process is decoupled into two steps :
        (1) the line cross a plane;
        (2) their intersection point falls in the polygon, including the border.

           P0 =np.array((x0,y0,z0))
           L  = np.array((dx,dy,dz))
           Polygon = np.array([                 # N x 3 array
                                [x1 y1 z1]
                                [x2 y2 z2]
                                ...
                                [xm ym zm]
                                ])
'''
def LineXPlane(P0,L,R0,n):
    '''
           Intersection of a 3D line with a 3D plane
           It returns
           (1)  P1       : P1 is a Python tuple
           (2) 'parallel':  the line is parallel to the plane
           (3) 'coplane' :  the line is on the plane (coplane)
    '''
    
    P0 = Array(P0)
    L  = Array(L)
    R0 = Array(R0)
    n  = Array(n)

    L = UnitVector(L) 
    n_dot_L = Dot(n,L)  
    dP = R0 - P0                         # [dx,dy,dz]

    if ScalarZero(n_dot_L):
        if ScalarZero(Dot(dP,dP)) or ScalarZero(Dot(dP,n)):
            return 'parallel'
        else:
            return 'coplane'

    x  = Dot(n,dP)/n_dot_L
    P  = P0 + x*L                         # [x,y,z]

    return tuple(P)   
    # return np.array 

def LineXPolygon(P0,L,Polygon):
    '''
    In 3D space, intersection of a line with a polygon.
    It returns the intersection point as tuple : P1 
       or 
          (1) a list of two tuples, [P1,P2],  for two intersection points;
                         plus a console warning : 
                         there are two points of intersection
          (2) string message 
               a) 'Intersection point beyond the polygon' 
               b) 'The line beyond the 2D plogon'
          
    '''
    n  = PolygonNormal(Polygon)      # [dx,dy,dz] 
    R0 = Array(Polygon[0,:])         # [x,y,z]
    R = LineXPlane(P0,L,R0,n)  # intersection of line with plane
    # print(f" In LineXPolygon() :\n R = LineXPlane(P0,L,R0,n)\n result = {R}")
    # print(f" Polygon :\n{Polygon}")

    if type(R) == str :
        if R == 'parallel':
            return 'parallel'

        if R == 'coplane':  # The line lies in the plane, so it reduces to 2D space
            PL = P0 + L
            P03D,Polygon3D,U,R0 = D3ToD2(P0,Polygon)                      ##从三维矩阵变成二维
            PL3D,Polygon3D,U,R0 = D3ToD2(PL,Polygon)
            Polygon2D = Polygon3D[:,0:2]
            L3D  = P03D-PL3D
            P02D = P03D[0:2]
            L2D  = L3D[0:2]
            P1,P2 = LineXPolygon2D(P02D,L2D,Polygon2D)

            if P1 is None : # and Points is None:
                return 'The line beyond the 2D plogon'

            elif type(P1) is tuple :  # single point
                R1 = Array(P1)
                P1 = D2toD3Point(R1,U,R0)
                return tuple(P1)

            else: # two points
                R1,R2 = P1
                P1 = D2toD3Point(Array(R1),U,R0)
                P2 = D2toD3Point(Array(R2),U,R0)
                print('intesection leaves a segment of ',
                    np.around(P1, decimals=3, out=None),
                    np.around(P2, decimals=3, out=None))
                return [tuple(P1), tuple(P2)]
    
    else :

        if PointInPolygon(R,Polygon) :
            return tuple(R)
        else :
            return 'Intersection point beyond the polygon'
 
def SegmentXPolygon(P1,P2,polygon):
    # Intersection of a segment (P1,P2) with a polygon
    L  = UnitVector(Array(P2) - Array(P1))
    P0 = P1

    Points = LineXPolygon(P0,L,polygon)

    if type(Points) is str:
        return None
    
    # single point
    elif type(Points) is tuple : 
        if PointInSegment(Array(Points),P1,P2):
           return Points
        else :
           return None

    # two points
    else :
        V1,V2 = Points
        if PointInSegment(Array(V1),P1,P2) and PointInSegment(Array(V2),P1,P2) :
            return [V1,V2]
        
        elif PointInSegment(Array(V1),P1,P2) :
            return V1

        elif PointInSegment(Array(V2),P1,P2) :
            return V2

        else :
            return None

def PolygonNormal(v):
    """
       get a unitary vector normal to the polygon 
       parameter : v
                     np.array(M,3)
    """
    #
    #   C = A x B 
    #
    A = v[1,:] - v[0,:]
    B = v[2,:] - v[1,:]
    C = Cross(A,B)
    
    return UnitVector(C)

def GetU(polygon):
    """
        Get transform matrix of a polyogn from its 3D to 2D
            U = GetU(polygon)
        Parameter :
            polygon : vertices of np.array(M,3)
    """

    v = polygon
    if type(v) != np.ndarray :
        v = Array(v) 

    a = v[1,:] - v[0,:]
    b = v[2,:] - v[1,:]
    c = Cross(a,b)

    # show("a",a)
    # show("b",b)
    # show("c",c)

    #   unitary vectors 
    i = UnitVector(a)
    k = UnitVector(c)
    j = Cross(k,i)

    # show("i",i)
    # show("j",j)
    # show("k",k)

    U = np.vstack((i,j,k))

    # show('U',U)

    return U

def LineXSegment2D(P0,L,x1,y1,x2,y2):
    '''
        Intersection of a segment (x1,y1),(x2,y2) with a 2D line.
        It returns :
        (1) True, P, intersecting point, list;
        (2) False, None, No intersection;
        (3) True, ‘colinear’, the segment if part of the line
    '''
    P1,L1,P2 = (x1,y1), (x1-x2,y1-y2), (x2,y2)
    L1  = UnitVector(Array(L1))

    if np.linalg.norm(L1) <= get_eps():
        return False, None

    else:
        P = LineXLine(P0,L,P1,L1) 

        if P == 'parallel':
            return False, None

        elif P == 'colinear':
            return True, 'colinear'

        else:
            P = Array(P)
            if PointInSegment(P, P1, P2): 
                return True, tuple(P)
            else:
                return False,'beyond segment'

def LineXPolygon2D(P0,L,Polygon):
    '''
         Intersection of line with polygon in 2D space.
         It returns a pair of values as follow,
            (1) P1，None   : one intersection point
            (2) None，None : no intersection
            (3)  P1，   P2 : two intersection points
    '''
    L = UnitVector(L) 
    n = len(Polygon)
    IS = 0
    P1 = None
    P2 = None
    for i in range(n):
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]

        ret, P = LineXSegment2D(P0,L,x1,y1,x2,y2)  
        # to check its intersection with each edge of the polygon
        if ret is False :
            pass
        
        elif P == 'colinear':           # the edge is part of line
            P1,P2 = (x1,y1),(x2,y2)
            return P1,P2
        
        else:
            if P1 is None:
                P1 = P
            elif np.linalg.norm(Array(P)-Array(P1)) <= get_eps():
                pass 

            else:
                P2 = P
                return P1,P2

    if P1 is None :
        return None, None
    else:
        return P1, None

# transformation from 3D to 2D
def D3ToD2(Point,Polygon):
    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    P  = Array(Point)
    r  = U@(R - R0).T  # @ is for vector times matrix
    p  = U@(P - R0).T
    xy = p.T
    vertices3D = r.T
    vertices2D = r.T[:,0:2]
    return xy,vertices3D,U,R0

# transformation from 2D to 3D : polygon
def D2toD3Polygon(Polygon,U,R0):
    r = Polygon.T
    A = np.mat(U)
    B = np.array(A.I)   #  inverse, .I only works for np.matrix
    R = (B@r).T + R0    # .T works for both matrxi and array
    return R            #  to let R is np.array

# transformation from 2D to 3D : Point
def D2toD3Point(Point,U,R0):
    Point3D = np.array([[Point[0]],[Point[1]],[0]])
    p = Point3D
    A = np.mat(U)
    B = np.array(A.I)
    R = (B@p).T+R0
    return R

# To check if a single point lies in a polygon, True/False
def PointInPolygon(Point,Polygon):

    # print(f" In PointInPolygon(), Polygon =\n{Polygon}")

    p,vertices3D,U,R0 = D3ToD2(Point,Polygon)
    z = p[2]
    vertices2D = vertices3D[:,0:2]

    # print(f" vertices2D =\n{vertices2D}")
    if ScalarZero(z) :
        # In local 2D coordiates, if z = 0 , the point is in the plane
        xy = p[0:2]                               # first two columns 
        return PointInPolygon2D(xy[0], xy[1], vertices2D)
    else :
        return False

# To check if many points lie in a polygon, True/False
def PointsInPolygon(Points,Polygon):
    Points = np.array(Points)

    # set it unitary
    j=0
    if Points.ndim == 1:
        return PointInPolygon(Points,Polygon)
    elif Points.ndim ==3:
        j=1
        dimen = Points.shape
        a=dimen[0]
        b=dimen[1]
        Points = Points.reshape(int(a*b),3)

    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    Ps = Array(Points)
    r  = U@(R - R0).T
    p  = U@(Ps - R0).T
    n  = len(p[0])                   # to check is z == 0
    ret = np.array(list(False for i in range(n)))

    for i in range(n):
        if ScalarZero(p[2,i]):
            ret[i] = True

    xy = (p[0:2]).T   # first two columns 
    vertices2D = r.T[:,0:2]
    if j == 1:
        ret = ret.reshape(a,b)
        xy = xy.reshape(a,b,2)
    ret = ret*PointsInPolygon2D(xy, vertices2D)
    return ret

# multiple points in a polygon : variant method 0
def PointsInPolygon0(Points,Polygon):
    Points = np.array(Points)
    ret=[]
    if Points.ndim ==2:
        for i,point in enumerate(Points):
            ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        return ret
    elif Points.ndim ==3:
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        ret = ret.reshape(i+1,j+1)
        return ret
    else:
        return None

# multiple points in a polygon : variant method 1
def PointsInPolygon1(Points,Polygon):
    Points = np.array(Points)
    if Points.ndim ==2:
        n=len(Points)
        ret = np.array(list(False for i in range(n)))
        for i,point in enumerate(Points):
            ret[i]=(PointInPolygon(point,Polygon))
        return ret
    elif Points.ndim ==3:
        n=len(Points)
        m=len(Points[0])
        ret = np.array(list(False for i in range(n*m)))
        ret = ret.reshape(n,m)
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret[i,j]=(PointInPolygon(point,Polygon))
        return ret
    else:
        return None

# multiple points in a polygon : 2D space only
def PointsInPolygon2D(Points,Polygon,Method='Custom'):
    from functools import reduce
    from operator import mul

    Vertices = Points
    if type(Points) is not np.array:
        Vertices = Array(Points)

    # Single Point
    # 1) input as np.array([7,8]), shape =(2,)
    if len(Vertices.shape) == 1 :
        x0 = Vertices[0]
        y0 = Vertices[1]
        ##print(x0,y0,Polygon)
        ret = PointInPolygon2D(x0,y0,Polygon) 
        return ret

    # 2) input as np.array([(7,8)]), shape = (1,2)
    elif (len(Vertices.shape) == 2 and Vertices.shape[0] == 1) : 
        x0 = Vertices[0][0]
        y0 = Vertices[0][1]
        ret = PointInPolygon2D(x0,y0,Polygon)
        return ret

    # Multiple Points
    shape = np.shape(Vertices)    #  0,...,n-1
    matrix_shape = shape[0:-1]  #  0,...,n-2, excluding shape[-1]
    n = reduce(mul, matrix_shape, 1)   #  how many points
    Points_array = Vertices.reshape(n,shape[-1])  # 1D array of (x,y,z).

    key_str = Method.lower()
    
    if key_str == 'custom':
        ret = _PointsInPolygon2D_Custom(Points_array,Polygon)
    elif key_str == 'matplotlib':
        ret = _PointsInPolygon2D_Matplotlib(Points_array, Polygon)

    return ret.reshape(matrix_shape)

# help functions 
def _PointsInPolygon2D_Custom(Points,Polygon):

    n = len(Points)
    ret = np.array(list(False for i in range(n)))
    for i in range(n):
        x0,y0  = Points[i]
        ret[i] = PointInPolygon2D(x0,y0,Polygon)   
    return ret

def _PointsInPolygon2D_Matplotlib(Points,Polygon):
    row = len(Polygon)   # row = N, Polygon = N x 2   
    
    # Inside
    edge = path.Path([(Polygon[i,0],Polygon[i,1]) for i in range(row)])
    ret  = edge.contains_points(Points)    
    
    # print(ret)
    # On edge
    if not all(ret) :        
        n = len(Points)
        for i in range(0,row):
            j = (i+1)%row 
            x1,y1 = Polygon[i]
            x2,y2 = Polygon[j]
            dy = y2-y1
            dx = x2-x1
           
            for k in range(n):
                if ret[k] :
                    continue          
                
                x0,y0 = Points[k]
                if not ScalarZero(dy):
                    if min(y1,y2) <= y0 and y0 <= max(y1,y2) :                        
                        x = x1 + (y0-y1)*dx/dy   # any slant line, including vertical line
                        if ScalarEqual(x,x0) :
                            ret[k] = True
                            
                elif not ScalarZero(dx):    # horizontal line
                    if min(x1,x2) <= x0 and x0 <= max(x1,x2) :
                        if ScalarEqual(y1,y0):
                            ret[k] = True
                                     
    # inside + on Edge
    return ret

# a 2D point inside a 2D polygon, it return True/False
def PointInPolygon2D(x0,y0,Polygon):
    """
       return value :
         True,  (XO,YO) IS LOCATED BOTH IN Polygon and ON EDGE
         False, (XO,YO) FAILS TO DO SO
    """
    if type(x0) is np.ndarray or type(y0) is np.ndarray :
        raise ValueError(f"PointInPolygon2D(x0,y0,Polygon)\n"
            "x0,y0 need be scalar value, but be given array.")

    n = len(Polygon)
    IS = 0
    for i in range(n):
        # print(f" Polygon[i] is of {type(Polygon[i])},\n{Polygon[i]}")
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]
        I = PointInSegment2D(x0,y0,x1,y1,x2,y2)
        # print(f" {loc[I]} of line = ({x1,y1}) - ({x2,y2})  ")
        if I == 1 :    
            IS += 1    #  x0 < x_predicted
        elif I == 2 :  # on edge
            return True
        
    ret = IS%2
    if ret == 1 :
        return True
    else:
        return False

    """
    Starting from a point P0, a ray goes to the right.
        INTERSECTION ?
            ret=O  NO  ( no any intersection with edges )
            ret=1  YES ( There is one intersection point, P0 is internal.) 
            ret=2  YES ( P0 is ON EDGE ) 
    """
    # ymin < y0 < ymax 

def PointInSegment2Dold(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ScalarEqual(min(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   
    #    if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) in the condition that all intersection occurs by the right
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            if not ScalarEqual(x1, x2) : # x1 != x2 :
                x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
                if  ScalarEqual(x0, x) :  # x0 == x :
                    return 2
                
                if x0 < x :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            
                return 0
            
            else:        # vertical line
                if ScalarEqual(x0,x1) :
                    return 2
                
                elif x0 < x1 :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            

                else :               # x0 > x1 :
                    return 0
               
        else:  # horizontal line
            if not ScalarEqual(y0 , y1) :
                return 0

            elif ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
    else:
        return 0

def PointInSegment2D(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   
    #  if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) in the condition that all intersection occurs by the right
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
            if  ScalarEqual(x0, x) :  # x0 == x :
                return 2
            if x0 < x :
                return 1 
            return 0
               
        else:  # horizontal line
            if ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
            return 0
    elif ScalarEqual(min(y1,y2) , y0):
        if ScalarEqual(min(y1,y2) , y1):
            if ScalarEqual(x1,x0):
                return 2
            else:
                return 0
        else:
            if ScalarEqual(x2,x0):
                return 2
            else:
                return 0
    else:
        return 0

# element-wise view factor
def fij(P1, P2, n1, n2, A2 ):
    '''
    P1,P2 : centers of two elements, np.array([x,y,z])
    n1,n2 : unit vectors of the two elements, np.array([x,y,z])
    A2 : the area.of receiving element
    '''
    dP = P1 - P2
    S  = np.sqrt(dP.dot(dP))
    
    V12 = P2 - P1
    V21 = P1 - P2
    d1 = V12.dot(n1)
    d2 = V21.dot(n2)
    
    f12 = d1*d2*A2/( np.pi* S*S*S*S)
    
    return f12

#
#  Demo how to use them
#
def test_PointsInPolygon2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]

    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(Points, polygon)
    print(ret)
    print(Points[ret])

def test_PointsInPath2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]
    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(P, polygon, Method = 'Matplotlib')
    print(ret)
    print(Points[ret])

def main():
    test_PointsInPolygon2D()
    test_PointsInPath2D()

if __name__ == '__main__':
    main()
