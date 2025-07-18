from MathLib import *
from obj import load_obj
from random import random

class Model(object):
    def __init__(self, filename):
        # Lista de vértices transformados en un buffer lineal
        self.vertices = []

        # Lista de colores por triángulo (uno por cara)
        self.colors = []

        # Carga vértices y caras desde el archivo .obj
        raw_vertices, faces = load_obj(filename)

        # Por cada cara (triángulo), agrega sus vértices y asigna un color aleatorio
        for face in faces:
            for idx in face:
                self.vertices.extend(raw_vertices[idx])
            self.colors.append([random(), random(), random()])

        # Transformaciones: traslación, rotación y escala
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

        # Shader que se puede aplicar a los vértices del modelo
        self.vertexShader = None

    # Devuelve la matriz de transformación combinada del modelo (Model Matrix)
    def GetModelMatrix(self):
        translateMat = TranslationMatrix(*self.translation)
        rotateMat = RotationMatrix(*self.rotation)
        scaleMat = ScaleMatrix(*self.scale)
        return translateMat @ rotateMat @ scaleMat