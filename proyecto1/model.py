from MathLib import *
from obj import load_obj, first_map_kd_from_obj
from BMPTexture import BMPTexture
import os

class Model:
    def __init__(self, filename, texture=None):
        self.vertices = []
        self.colors = []
        self.uvs = []
        self.normals = []

        # Si no te pasan textura manualmente → intentar leerla del .mtl
        if texture is None:
            try:
                kd_path = first_map_kd_from_obj(filename)
                if kd_path and os.path.isfile(kd_path):
                    self.texture = BMPTexture(kd_path)
                else:
                    self.texture = None
            except Exception:
                self.texture = None
        else:
            self.texture = texture

        # Cargar datos del .obj
        raw_vertices, texcoords, raw_normals, faces = load_obj(filename)

        for face in faces:
            for v_idx, vt_idx, vn_idx in face:
                # vértices
                self.vertices.extend(raw_vertices[v_idx])

                # uvs
                if 0 <= vt_idx < len(texcoords):
                    self.uvs.append(texcoords[vt_idx])
                else:
                    self.uvs.append([0, 0])

                # normales
                if 0 <= vn_idx < len(raw_normals):
                    self.normals.append(raw_normals[vn_idx])
                else:
                    self.normals.append([0, 0, 1])

            # color por cara (por ahora blanco)
            self.colors.append([1, 1, 1])

        # transformaciones iniciales
        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

        # shaders asignables
        self.vertexShader = None 
        self.fragmentShader = None 

    def GetModelMatrix(self):
        translateMat = TranslationMatrix(*self.translation)
        rotateMat = RotationMatrix(*self.rotation)
        scaleMat = ScaleMatrix(*self.scale)
        return translateMat @ rotateMat @ scaleMat

    def SetRotationDegrees(self, pitch_deg, yaw_deg, roll_deg):
        from math import radians
        self.rotation = [radians(pitch_deg), radians(yaw_deg), radians(roll_deg)]