import numpy as np
from math import sin, cos, tan, radians

def TranslationMatrix(x, y, z):
    return np.matrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def ScaleMatrix(x, y, z):
    return np.matrix([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])

def RotationMatrix(pitch, yaw, roll):
    # pitch (X), yaw (Y), roll (Z), en radianes
    pitchMat = np.matrix([
        [1, 0, 0, 0],
        [0, cos(pitch), -sin(pitch), 0],
        [0, sin(pitch),  cos(pitch), 0],
        [0, 0, 0, 1]
    ])

    yawMat = np.matrix([
        [ cos(yaw), 0, sin(yaw), 0],
        [       0, 1,       0, 0],
        [-sin(yaw), 0, cos(yaw), 0],
        [       0, 0,       0, 1]
    ])

    rollMat = np.matrix([
        [cos(roll), -sin(roll), 0, 0],
        [sin(roll),  cos(roll), 0, 0],
        [       0,         0, 1, 0],
        [       0,         0, 0, 1]
    ])

    return pitchMat @ yawMat @ rollMat

def LookAtMatrix(eye, target, up):
    eye = np.array(eye)
    target = np.array(target)
    up = np.array(up)

    z = eye - target
    z = z / np.linalg.norm(z)

    x = np.cross(up, z)
    x = x / np.linalg.norm(x)

    y = np.cross(z, x)
    y = y / np.linalg.norm(y)

    mat = np.matrix([
        [x[0], x[1], x[2], -np.dot(x, eye)],
        [y[0], y[1], y[2], -np.dot(y, eye)],
        [z[0], z[1], z[2], -np.dot(z, eye)],
        [   0,    0,    0,              1]
    ])

    return mat

def ProjectionMatrix(fov, aspect, near, far):
    f = 1 / tan(radians(fov) / 2)
    depth = far - near

    return np.matrix([
        [f / aspect, 0, 0,                          0],
        [0,          f, 0,                          0],
        [0,          0, -(far + near) / depth,  -2 * near * far / depth],
        [0,          0, -1,                         0]
    ])

def ViewportMatrix(x, y, width, height):
    w = width / 2
    h = height / 2
    return np.matrix([
        [w, 0, 0, x + w],
        [0, h, 0, y + h],
        [0, 0, 0.5, 0.5],  # Z en rango [0, 1]
        [0, 0, 0, 1]
    ])