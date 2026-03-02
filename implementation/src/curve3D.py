import numpy as np
from renderable import Renderable3D
from abc import ABC, abstractmethod
from manim import *


class Curve3D(Renderable3D, ABC):
    def __init__(self, name: str, t_range=(-TAU, TAU)):
        super().__init__(name)
        self.t_range = list(t_range)

    @abstractmethod
    def pos(self, t: float, axes: ThreeDAxes) -> np.ndarray:
        """Retourne axes.c2p(x,y,z)."""

    def build(self, axes: ThreeDAxes) -> Mobject:
        return ParametricFunction(
            lambda t: self.pos(t, axes),
            t_range=self.t_range,
        )