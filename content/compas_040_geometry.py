# https://github.com/compas-Workshops/BFH24/blob/main/040_geometry.py

from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import NurbsCurve
from compas.geometry import Point
from compas.geometry import Polyline
from compas.geometry import Transformation
from compas.itertools import linspace
from compas_viewer import Viewer

points = [
    Point(0, 0, 0),
    Point(3, 3, 0),
    Point(6, -6, 3),
    Point(9, 0, 0),
]
curve: NurbsCurve = NurbsCurve.from_points(points)

frames: list[Frame] = []
for t in linspace(curve.domain[0], curve.domain[1], 100):
    frames.append(curve.frame_at(t))

box = Box(0.8, 0.5, 0.3)

# =============================================================================
# Viz
# =============================================================================

viewer = Viewer()
viewer.renderer.camera.target = [0, 0, 3]
viewer.renderer.camera.position = [-5, 0, 7]

viewer.scene.add(curve)
viewer.scene.add(Polyline(curve.points), show_points=True)

for frame in frames[::2]:
    viewer.scene.add(frame)

boxobj = viewer.scene.add(box)


@viewer.on(interval=100, frames=len(frames))
def slide(f):
    frame = frames[f]
    transformation = Transformation.from_frame_to_frame(box.frame, frame)
    box.transform(transformation)
    boxobj.init()  # this is a temp hack
    boxobj.update()


viewer.show()