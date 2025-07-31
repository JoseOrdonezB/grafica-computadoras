import numpy as np

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    # Paso 1: convertir a coordenadas homogéneas
    vt = np.array([[vertex[0]], [vertex[1]], [vertex[2]], [1]])

    # Paso 2: aplicar Model, View y Projection
    vt = projectionMatrix @ viewMatrix @ modelMatrix @ vt

    # Paso 3: perspectiva (división por W)
    w = vt[3, 0]
    if w == 0:
        w = 1

    vt /= w  # Normalized Device Coordinates (NDC)

    # Paso 4: aplicar viewport (de NDC a pantalla)
    vt = viewportMatrix @ vt

    x_screen = int(vt[0, 0])
    y_screen = int(vt[1, 0])
    z_ndc = vt[2, 0]

    return x_screen, y_screen, z_ndc