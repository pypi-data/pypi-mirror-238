# VisualShape3D

## About VisualShape3D

VisualShape3D intends to plot 3D points, lines and polygons more easily in matplotlib. That is, one needs not create a plotting figure by plt.figure and plt.subplot() as usual.


## Core Features
- Three shapes : Point, Segment and Polygon.
- Its logic for 3D definition : creating a 2D shape first in working plane and then moving its referene point to a desired 3D position and rotating its normal vector of facet to a designated orientation.
- It can check whether or not a point is inside a segment or polygon, by their magic functions `__contains__` as overloaded for Segment and Polygon.
- `__hash__` and `__eq__`, also overloaded for Point, Segment and Polygon.
- `__neg__` overloaded for polygon when one wants to know the list of vertices on its other side.


## Requirements

* [Python](http://www.python.org) 3 
* Matplotlib is installed.

## Documentation

To be continued.

## Installation
```bash
pip install VisualShape3D
```

## Usage
```Python
import VisualShape3D.Rendering as rd
import VisualShape3D.VisualShapes as vs

view = rd.OpenView()

W,H = 2.0,1.5
shape = vs.Shape('rectangle',W,H)
shape = shape.move(to = (2,0,0), by = (45,30))

line = vs.Polyline((0,0,0),(3,1.,2))
P = shape.intersect(line)
line.broken_at(P)

view.add_plot(shape,style = {'facecolor':'cornflowerblue', 'edgecolor':'navy'})
view.add_plot(line,style={'color':'k','linewidth':2,'node':'visible'})

view.show(azim=-20, elev=13, hideAxes=True,origin=True)
```
<img src="./html/_images/logo_drawn.png"/>

## Change Log

[changelog.md](changelog.md)

## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact
heliqun@ustc.edu.cn

