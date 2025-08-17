import numpy as np
from math import sin, cos, tan, radians

def TranslationMatrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def ScaleMatrix(x, y, z):
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def RotationMatrix(pitch, yaw, roll):
    pitchMat = np.array([
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch),  cos(pitch), 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    yawMat = np.array([
        [ cos(yaw), 0, sin(yaw), 0],
        [       0, 1,       0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [       0, 0,       0, 1]
    ], dtype=np.float32)

    rollMat = np.array([
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll),  cos(roll), 0, 0],
        [       0,         0, 1, 0],
        [       0,         0, 0, 1]
    ], dtype=np.float32)

    return pitchMat @ yawMat @ rollMat

def LookAtMatrix(eye, target, up):
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    z = eye - target
    z /= np.linalg.norm(z)

    x = np.cross(up, z)
    x /= np.linalg.norm(x)

    y = np.cross(z, x)

    mat = np.array([
        [x[0], x[1], x[2], -np.dot(x, eye)],
        [y[0], y[1], y[2], -np.dot(y, eye)],
        [z[0], z[1], z[2], -np.dot(z, eye)],
        [   0,    0,    0,              1]
    ], dtype=np.float32)

    return mat

def ProjectionMatrix(fov, aspect, near, far):
    f = 1 / tan(radians(fov) / 2)
    depth = far - near

    return np.array([
        [f / aspect, 0, 0,                          0],
        [0,          f, 0,                          0],
        [0,          0, -(far + near) / depth,  -2 * near * far / depth],
        [0,          0, -1,                         0]
    ], dtype=np.float32)

def ViewportMatrix(x, y, width, height):
    w = width / 2
    h = height / 2
    return np.array([
        [w, 0, 0, x + w],
        [0, h, 0, y + h],
        [0, 0, 0.5, 0.5],
        [0, 0, 0, 1]
    ], dtype=np.float32)