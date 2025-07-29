import numpy as np

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]

    vt = np.array([[vertex[0]], [vertex[1]], [vertex[2]], [1]])

    vt = modelMatrix @ vt

    x_ndc = vt[0, 0] / vt[3, 0]
    y_ndc = vt[1, 0] / vt[3, 0]
    z_ndc = vt[2, 0] / vt[3, 0]

    width = 512
    height = 512

    x_screen = int((x_ndc + 1) * (width / 2))
    y_screen = int((y_ndc + 1) * (height / 2))

    return x_screen, y_screen, z_ndc