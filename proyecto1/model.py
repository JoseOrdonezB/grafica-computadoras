from MathLib import *
from obj import load_obj

class Model:
    def __init__(self, filename, texture=None):
        self.vertices = []
        self.colors = []
        self.uvs = []
        self.normals = []
        self.texture = texture

        raw_vertices, texcoords, raw_normals, faces = load_obj(filename)

        for face in faces:
            for v_idx, vt_idx, vn_idx in face:

                self.vertices.extend(raw_vertices[v_idx])

                if 0 <= vt_idx < len(texcoords):
                    self.uvs.append(texcoords[vt_idx])
                else:
                    self.uvs.append([0, 0])

                if 0 <= vn_idx < len(raw_normals):
                    self.normals.append(raw_normals[vn_idx])
                else:
                    self.normals.append([0, 0, 1])

            self.colors.append([1, 1, 1])

        self.translation = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]

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