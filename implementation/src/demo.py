
from manim import *
from manager3D import Graph3DManager


class Demo(ThreeDScene):
    def construct(self):
        mgr = Graph3DManager(self)
        mgr.add_axes()

        self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        helix = Helix()
        surf  = Paraboloid()

        mgr.add(helix)
        mgr.add(surf)

        self.wait(1)
        mgr.animate("helix", w=3.0, run_time=2)
        mgr.animate("paraboloid", a=0.4, run_time=2)

        self.wait(1)
        mgr.remove("helix")
        self.wait(1)