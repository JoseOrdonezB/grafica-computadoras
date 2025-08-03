import numpy as np
from MathLib import LookAtMatrix, ProjectionMatrix, ViewportMatrix

class Camera:
    def __init__(self, eye, target, up, fov, aspect, near, far, screen_width, screen_height):
        self.eye = eye
        self.target = target
        self.up = up
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.viewMatrix = LookAtMatrix(eye, target, up)
        self.projectionMatrix = ProjectionMatrix(fov, aspect, near, far)
        self.viewportMatrix = ViewportMatrix(0, 0, screen_width, screen_height)

    def getCombinedMatrix(self, modelMatrix):
        return self.viewportMatrix @ self.projectionMatrix @ self.viewMatrix @ modelMatrix