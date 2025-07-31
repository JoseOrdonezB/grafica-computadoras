import numpy as np

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]

    # Convertir a coordenadas homogéneas
    vt = np.array([[vertex[0]], [vertex[1]], [vertex[2]], [1]])

    # Aplicar transformación de modelo
    vt = modelMatrix @ vt

    # Evitar división por cero
    w = vt[3, 0]
    if w == 0:
        w = 1

    # Normalized Device Coordinates (NDC)
    x_ndc = vt[0, 0] / w
    y_ndc = vt[1, 0] / w
    z_ndc = vt[2, 0] / w

    # Viewport transform (de NDC [-1,1] a coordenadas de pantalla)
    width = 512
    height = 512

    x_screen = int((x_ndc + 1) * (width / 2))
    y_screen = int((y_ndc + 1) * (height / 2))

    return x_screen, y_screen, z_ndc