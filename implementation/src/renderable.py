from abc import ABC, abstractmethod
from dataclasses import dataclass
from manim import *

class Renderable3D(ABC):
    def __init__(self, name: str):
        self.name = name
        self.trackers: dict[str, ValueTracker] = {}
        self.mobj: Mobject | None = None

    def add_param(self, key: str, value: float):
        self.trackers[key] = ValueTracker(value)
        return self

    def get(self, key: str) -> float:
        return self.trackers[key].get_value()

    @abstractmethod
    def build(self, axes: Mobject) -> Mobject:
        """Construit le mobject manim (courbe/surface/...) à partir des trackers."""

    def attach(self, scene: Scene, axes: Mobject):
        # always_redraw : le mobject est recalculé automatiquement
        self.mobj = always_redraw(lambda: self.build(axes))
        scene.add(self.mobj)

    def detach(self, scene: Scene):
        if self.mobj is not None:
            scene.remove(self.mobj)
            self.mobj = None

    def animate_to(self, scene: Scene, run_time: float = 2, **params):
        anims = []
        for k, v in params.items():
            if k not in self.trackers:
                self.add_param(k, float(v))
            anims.append(self.trackers[k].animate.set_value(float(v)))
        scene.play(*anims, run_time=run_time)