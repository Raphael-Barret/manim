from renderable import Renderable3D
from abc import ABC, abstractmethod
from manim import *

class Surface3D(Renderable3D, ABC):
    def __init__(self, name: str, u_range=(-2, 2), v_range=(-2, 2), resolution=(32, 32)):
        super().__init__(name)
        self.u_range = list(u_range)
        self.v_range = list(v_range)
        self.resolution = resolution

    @abstractmethod
    def pos(self, u: float, v: float, axes: ThreeDAxes):
        ...

    def build(self, axes: ThreeDAxes) -> Mobject:
        return Surface(
            lambda u, v: self.pos(u, v, axes),
            u_range=self.u_range,
            v_range=self.v_range,
            resolution=self.resolution,
        )

