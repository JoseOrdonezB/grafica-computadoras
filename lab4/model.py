from MathLib import *
from obj import load_obj

class Model:
    def __init__(self, filename, texture=None):
        self.vertices = []      # Lista lineal de x, y, z por vértice
        self.uvs = []           # Lista paralela de u, v por vértice
        self.colors = []        # Color por triángulo (usado si no hay textura)
        self.texture = texture  # Textura BMP asociada

        # Carga del archivo .obj
        raw_vertices, texcoords, faces = load_obj(filename)

        for face in faces:
            for v_idx, vt_idx in face:
                self.vertices.extend(raw_vertices[v_idx])
                if 0 <= vt_idx < len(texcoords):
                    self.uvs.append(texcoords[vt_idx])
                else:
                    self.uvs.append([0, 0])  # Coordenadas por defecto si no hay UV válida
            self.colors.append([1, 1, 1])  # Blanco por defecto si hay textura

        # Transformaciones iniciales
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]  # pitch, yaw, roll en radianes
        self.scale = [1, 1, 1]

        self.vertexShader = None  # Función para transformar vértices

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(*self.translation)
        rotateMat = RotationMatrix(*self.rotation)
        scaleMat = ScaleMatrix(*self.scale)
        return translateMat @ rotateMat @ scaleMat

    def SetRotationDegrees(self, pitch_deg, yaw_deg, roll_deg):
        from math import radians
        self.rotation = [radians(pitch_deg), radians(yaw_deg), radians(roll_deg)]