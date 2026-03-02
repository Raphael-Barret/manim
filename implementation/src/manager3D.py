from manim import *
from renderable import Renderable3D

class Graph3DManager:
    def __init__(self, scene: ThreeDScene):
        self.scene = scene
        self.axes = ThreeDAxes()
        self.objects: dict[str, Renderable3D] = {}

    def add_axes(self):
        self.scene.add(self.axes)

    def add(self, obj: Renderable3D):
        self.objects[obj.name] = obj
        obj.attach(self.scene, self.axes)

    def remove(self, name: str):
        obj = self.objects.pop(name, None)
        if obj:
            obj.detach(self.scene)

    def animate(self, name: str, run_time=2, **params):
        self.objects[name].animate_to(self.scene, run_time=run_time, **params)