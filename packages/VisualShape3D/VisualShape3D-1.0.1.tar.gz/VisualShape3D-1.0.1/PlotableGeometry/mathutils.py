import numpy as np
from math import pi,log10

SIG_FIGURES = 10
FLOAT_EPS = 1 / (10 ** SIG_FIGURES)
def set_eps(eps = 1e-10):
    global FLOAT_EPS,SIG_FIGURES
    FLOAT_EPS = eps
    SIG_FIGURES = round(log10(1 / eps))

def get_eps():
    global FLOAT_EPS
    return FLOAT_EPS

def get_sig_figures():
    global SIG_FIGURES
    return SIG_FIGURES

def set_sig_figures(sig_figures = 10):
    global FLOAT_EPS,SIG_FIGURES
    SIG_FIGURES = sig_figures
    FLOAT_EPS = 1 / (10 ** SIG_FIGURES)


class Vector():
    def __init__(self,*args):
        super().__init__()
        self.x, self.y, self.z = 0,0,0
        self._set_vector(*args)

    def _set_vector(self, *args):
        m = len(args) 
        _class_ = self.__class__

        if m == 0 :
            return

        if m == 1:
            P = args[0]
            if isinstance(P,_class_) :
                self.x, self.y, self.z = P.x, P.y, P.z

            else :
                if len(P)==3 :
                    self.x, self.y, self.z = P[0],P[1],P[2]
                
                elif len(P)==2 :
                    self.x, self.y, self.z = P[0],P[1],0.0
                
                else:
                    name = self.__class__.__name__
                    raise ValueError("{name} needs 2 or 3 values")
        
        else : # 2 or 3 scalar numbers
            self.x,self.y = args[0],args[1]

            if len(args) == 3 :
                self.z = args[2]
            else :
                self.z = 0
        
        
        
    def __str__(self):
        name = self.__class__.__name__
        return f"{name}{self.x,self.y,self.z}"    
    

    # operators 
    def __add__(self, v):
        return self.__class__(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return self.__class__(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rmul__(self, c):
        return self.__class__(c * self.x, c * self.y, c * self.z)

    def __mul__(self, c):
        return self.__rmul__(c)

    def __getitem__(self, item):
        """return one of x,y,z"""
        return (self.x, self.y, self.z)[item]

    def __setitem__(self, item, value):
        """set one of x,y,z of a Point"""
        setattr(self, "xyz"[item], value)

    def dot(self,v):
        u = self
        return u.x * v.x + u.y * v.y + u.z * v.z
      
    def cross(self, v):
        u = self
        return self.__class__(u.y * v.z - u.z * v.y, u.z * v.x - u.x * v.z, u.x * v.y - u.y * v.x)

    def rotated_by(self,M):  # Matrix * vector
        u = self 
        x = u.x * M[0][0] + u.y * M[0][1] + u.z * M[0][2] 
        y = u.x * M[1][0] + u.y * M[1][1] + u.z * M[1][2] 
        z = u.x * M[2][0] + u.y * M[2][1] + u.z * M[2][2] 
        return self.__class__(x,y,z)
    
    def length(self):
        x,y,z = self.x, self.y, self.z
        return np.sqrt(x * x + y * y + z * z)

    def unit(self):
        L = self.length()
        x,y,z = self.x, self.y, self.z
        if L > 0 :
            inv_L = 1/L
            x, y, z = x*inv_L,y*inv_L,z*inv_L
        return Vector(x,y,z) 
    
    def as_list(self):
        return [self.x,self.y,self.z]

    def as_tuple(self):
        return (self.x,self.y,self.z)

    def as_dict(self):
        return {"x":self.x, "y":self.y, "z":self.z}

    def as_array(self):
        return np.array([self.x,self.y,self.z])
    
    #  logical operant : == 
    def __eq__(self, v):
        #return self.x == v.x and self.y == v.y and self.z == v.z
        return isinstance(v, type(self)) and self.equal_to(v)
    
    def equal_to(self, v):
        return self.deviation_from(v) < get_eps()

    def deviation_from(self, v):
        dx = self.x - v.x
        dy = self.y - v.y
        dz = self.z - v.z
        return np.sqrt(dx * dx + dy * dy + dz * dz)

class Matrix3():
    '''
      https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry/matrices
    '''
    def __init__(self, *args):
        # initialize with the identity matrix of 4x4 
        self.m = np.array([[1,0,0],[0,1,0],[0,0,1]])
        if len(args) > 0 :
            self._set_matrix(*args)

    def __str__(self):
        name = self.__class__.__name__
        return f"{name}({self.m})"

    def __rmul__(self, c):
        if type(c) is int or type(c) is float:
            return Matrix3(c * self.m)

        elif isinstance(c,Vector):
            return Vector(self.m @ c.as_array())

        elif type(c) is np.ndarray and len(c) >= 3 :
            v = c[0:3]
            return Vector(self.m @ v)

        elif type(c) is type(self):
            A = c.get_m()
            B = self.get_m()
            return self.__class__(A @ B)

    def __mul__(self, c):
        return self.__rmul__(c)

    # two help functions
    def _set_matrix(self, *args):
        import copy
        if len(args) == 1:   #   Matrix(M)
            
            first_input= args[0]
            if type(first_input) is self.__class__ :
                self.m = copy.deepcopy(first_input.m)

            else :  #  Matrix([[1,2,3],[5,6,7],[9,10,11]])  
                self._set_m(*first_input)
        
        else : #  Matrix([1,2,3],[5,6,7],[9,10,11])
            self._set_m(*args)

    def _set_m(self,*args):
        m = len(args) 
        for i in range(m) :
            n = len(args[i])
            for j in range(n):
                x = args[i][j]
                if type(x) is not str:
                    self.m[i,j] = x 
    
    # three functions to manipulate the matrix
    def get_m(self):
        m,n = np.shape(self.m)
        M = np.eye(m)
        for i in range(m):
            for j in range(m):
                M[i,j] = self.m[i,j]
        return M

    def transpose(self):
        return np.transpose(self.m)

    def inverse(self):
        return np.linalg.inv(self.m)

# validation function for intersection
'''
     https://math.stackexchange.com/questions/27388/intersection-of-2-lines-in-2d-via-general-form-linear-equations?noredirect=1
''' 
# ----------------------
# generic math functions

def add_v3v3(v0, v1):
    return (
        v0[0] + v1[0],
        v0[1] + v1[1],
        v0[2] + v1[2],
        )

def sub_v3v3(v0, v1):
    return (
        v0[0] - v1[0],
        v0[1] - v1[1],
        v0[2] - v1[2],
        )

def dot_v3v3(v0, v1):
    return (
        (v0[0] * v1[0]) +
        (v0[1] * v1[1]) +
        (v0[2] * v1[2])
        )

def len_squared_v3(v0):
    return dot_v3v3(v0, v0)

def mul_v3_fl(v0, f):
    return (
        v0[0] * f,
        v0[1] * f,
        v0[2] * f,
        )

def isect_line_plane_v3(p0, p1, p_co, p_no, epsilon=1e-6):
    """
    p0, p1     : a line from p0 to p1.
    p_co, p_no : a plane 
                p_co, a point on the plane (plane coordinate).
                p_no, a normal vector defining the plane direction;
                      (does not need to be normalized).

    Return a Vector or None (when the intersection can't be found).
    """

    u = sub_v3v3(p1, p0)
    dot = dot_v3v3(p_no, u)

    if abs(dot) > epsilon:
        # The factor of the point between p0 -> p1 (0 - 1)
        # if 'fac' is between (0 - 1) the point intersects with the segment.
        # Otherwise:
        #  < 0.0: behind p0.
        #  > 1.0: in front of p1.
        w = sub_v3v3(p0, p_co)
        fac = -dot_v3v3(p_no, w) / dot
        u = mul_v3_fl(u, fac)
        return add_v3v3(p0, u)
    else:
        # The segment is parallel to plane.
        return None

# ----------------------

def main():
    v1 = Vector(1,2,3)
    print(f" v = {v1}")
    print(f" v = {v1.as_array()}")
    print(f" v = {v1.as_list()}")
    print(v1.cross(v1))
    v2 = Vector(v1)
    print(type(v2))

    m = Matrix3([1,2,3],[5,6,7],[9,10,11])

    print(f" m = {m}")
    print(m.transpose())

    v2 = m * v1
    print(f" m * v = {v2}")
    v3 = v1 * m
    print(f" v * m = {v3}")

    m2 = m * m 
    print(f" m * m = {m2}")

if __name__ == '__main__':
    main()
