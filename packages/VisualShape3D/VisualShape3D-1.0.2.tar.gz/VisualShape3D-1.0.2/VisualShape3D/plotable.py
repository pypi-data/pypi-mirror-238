import math
import numpy as np
import matplotlib._color_data as mcd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
import matplotlib.pylab as plt
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d

class Plotable(object):
### Initialization
    _fig = None
    _ax  = None

    @staticmethod
    def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
        """我。
        Plots the string *s* on the axes *ax*, with position *xyz*, size *size*,
        and rotation angle *angle*. *zdir* gives the axis which is to be treated as
        the third dimension. *usetex* is a boolean indicating whether the string
        should be run through a LaTeX subprocess or not.  Any additional keyword
        arguments are forwarded to `.transform_path`.
    
        Note: zdir affects the interpretation of xyz.
        """
        x, y, z = xyz
        if zdir == "y":
            xy1, z1 = (x, z), y
        elif zdir == "x":
            xy1, z1 = (y, z), x
        else:
            xy1, z1 = (x, y), z
    
        text_path = TextPath((0, 0), s, size=size, usetex=usetex)
        trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])
    
        p1 = PathPatch(trans.transform_path(text_path), **kwargs)
        ax.add_patch(p1)
        art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)
    """
    It's a base class for plotable geometries.    
    Universal methods :
        `plot()`
        `get_centroid()`

        `copy()`
        `save()`
        `restore()`
    
    Specific methods as defined in geometry classes:
        `get_instance()`      returns the specific instance to be plotted
        `iplot()`             specific action in plot()
        `set_view_domain()`   adjusting viewport to hold all geometries.
        
    """
    def __init__(self):
        self.backup = None
        self.facecolor  ='xkcd:beige'
        self.edgecolor  ='olive'
        self.color      ='darkgreen'  # for Point/Segement/Line/Polyline
        self.linewidth  = 1
        self.linestyles ="solid"
        self.alpha      = 1
        self.marker     ='o'
        self.label = None

    def set_ax(self, ax):
        Plotable._ax = ax

    def get_ax(self):
        return Plotable._ax

    def clear_ax(self):
        self.set_ax(None)

    def close(self):
        plt.close()

### Functions
    def show(self, elev= 20.0, azim = -80.0, hideAxes = False, origin = False):
        ax = self.get_ax()

        if ax is None :
            return
      
        ax.view_init(elev, azim)

        if hideAxes :
            ax.set_axis_off()

        if origin :
            R0 = Origin()
            self.add_plot(R0)

        plt.show()

        return ax


    def plot(self, style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'}, ax = None, 
                   hideAxes = False, **kwargs):
        """
        it will plot geometry in the settings as follow 
  
         1) style :
              style = {'facecolor','edgecolor','linewidth','alpha','node','nodemarker','nodecolor'}
              It matters differently for line and polygon 
                = (edge color, line width, alpha) for segement, line, polyline and Ray
                = (face color, edge color, alpha) for polygon
                = ( node, node color, node marker) for point
         2) ax: 
              None : to plot in a new figure
              ax :   to plot in the current "ax" (mplot3d.Axes3D) 

         3) hideAxes : hide axes or not

        return  plt, ax
              
        Note :
            plt.show() activates all plots.
        """

        bAdjustViewport = True     # to hold new geometries
        if ax is None:
            if self.get_ax() is None : 
                
                # it is the very first plot of one alone application
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                self.set_ax(ax)
                bAdjustViewport = False
                
            else :          # or it plot in the ax of an GUI app
                pass        

        # fetch the instance of a geometry
        # instance = self.__class__(**self.get_seed())
        instance = self.get_instance()

        if instance is None : # in the case for an instance of Plotable itself.
            return  

        # print(f" instance = {type(instance)}")
        # print(f" self = {type(self)}")
        # print(f" ax = {type(ax)}")

        # adjust viewport to hold the instance 
        domain = instance.get_domain()

        bound = np.max(domain[1]-domain[0])
        centroid = instance.get_centroid()
        pos = np.vstack((centroid-bound/2, centroid+bound/2))
        pos[0,2] = domain[0,2]
        pos[1,2] = pos[0,2] + bound
        
        # Overlap the existing plots 
        if bAdjustViewport :
            old_pos = np.array([ax.get_xbound(),
                                ax.get_ybound(),
                                ax.get_zbound()]).T
            pos = np.dstack((pos, old_pos))
            pos = np.array([np.min(pos[0, :, :], axis=1),
                            np.max(pos[1, :, :], axis=1)])


        # Plot instance
        if 'facecolor' not in style : style['facecolor'] = 'default' 
        if 'edgecolor' not in style : style['edgecolor'] = 'default' 
        if 'linewidth' not in style : style['linewidth'] = 'default' 
        if 'alpha'     not in style : style['alpha']     = 'default' 

        if style['facecolor'] == 'default' : style['facecolor'] = self.facecolor
        if style['edgecolor'] == 'default' : style['edgecolor'] = self.edgecolor
        if style['linewidth'] == 'default' : style['linewidth'] = self.linewidth
        if style['alpha']     == 'default' : style['alpha']     = self.alpha    

        instance.iplot(style = style, ax = ax, **kwargs)

        # Axis limits
        ax.set_xlim3d(left   = pos[0,0], right = pos[1,0])
        ax.set_ylim3d(bottom = pos[0,1], top   = pos[1,1])
        ax.set_zlim3d(bottom = pos[0,2], top   = pos[1,2])

        if hideAxes :
            ax.set_axis_off()
            # self.draw_origin()

        else :
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        return ax


    def add_plot(self, shape, 
                 style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'},
                 hideAxes = False, **kwargs):

        if not isinstance(shape, Plotable):
            return None

        return shape.plot(style = style, ax = self.get_ax(), hideAxes=hideAxes,**kwargs)

 
    def get_centroid(self):
        """
        The centroid refers to the center of the circumscribed
        paralellepiped, not its mass center.
        
        it returns a ndarray of (x, y, z).
        
        """
        return self.get_domain().mean(axis=0)

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): 
        return self

    def iplot(self, style, ax, **kwargs):
        if ax is None:
            ax = self.get_ax()

        R0 = Origin()
        R0.iplot(style, ax, **kwargs)

    def get_domain(self) :

        ax = self.get_ax()
        domain = np.array([ax.get_xbound(), 
                           ax.get_ybound(),
                           ax.get_zbound()])
        return domain.T
 
class OpenView(Plotable):
### Initialization
    def __init__(self, ax=None):
        super().__init__()
        if self.get_ax() is not None:
            self.clear_ax()

        if ax is None :
            # it is the very first plot of the application
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
        self.set_ax(ax)


class Origin(Plotable):
    def __init__(self):
        super().__init__()    

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):
        if ax is None:
            ax = self.get_ax()

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        zmin, zmax = ax.get_zlim()

        # set the grid
        x = [xmin, xmin, xmin]
        y = [ymin, ymin, ymin]
        z = [zmin, zmin, zmin]
        
        dx = 0.15*(xmax - xmin)
        dy = 0.15*(ymax - ymin)
        dz = 0.15*(zmax - zmin)

        # set the directiona and sizea of three arrows
        u = [dx,0 ,0 ]
        v = [0 ,dy,0 ]
        w = [0 ,0 ,dz]
        
        ax.quiver(x, y, z, u, v, w)
        
        # Manually label the axes
        
        Plotable.text3d(ax, (xmin + 1.1*dx, ymin - 0.2*dy, zmin), "X-axis", zdir="z", size=.1, usetex=False,
               ec="none", fc="k", **kwargs)
        
        Plotable.text3d(ax, (xmin, ymin + 1.1*dy ,zmin), "Y-axis", zdir="z", size=.1, usetex=False,
               angle=np.pi / 2, ec="none", fc="k",**kwargs)
        
        Plotable.text3d(ax, (xmin - 0.1* dx, ymin, zmin + dz ), "Z-axis", zdir="y", size=.1, usetex=False,
               angle=np.pi / 2, ec="none", fc="k", **kwargs)


def main():
    view = OpenView()
    print(view.get_ax())
    view.show()

if __name__ == '__main__':
    main()
