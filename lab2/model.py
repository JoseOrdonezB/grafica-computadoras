from MathLib import *
from obj import load_obj
from random import random

class Model(object):
    def __init__(self, filename):
        self.vertices = []
        self.colors = []

        raw_vertices, faces = load_obj(filename)

        for face in faces:
            for idx in face:
                self.vertices.extend(raw_vertices[idx])
            self.colors.append([random(), random(), random()])

        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.vertexShader = None

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(*self.translation)
        rotateMat = RotationMatrix(*self.rotation)
        scaleMat = ScaleMatrix(*self.scale)
        return translateMat @ rotateMat @ scaleMat