import numpy as np
import math

def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]

    vt = np.array([[vertex[0]], [vertex[1]], [vertex[2]], [1]])

    vt = projectionMatrix @ viewMatrix @ modelMatrix @ vt

    w = vt[3, 0]
    if w == 0:
        w = 1

    vt /= w 
    vt = viewportMatrix @ vt

    x_screen = int(vt[0, 0])
    y_screen = int(vt[1, 0])
    z_ndc = vt[2, 0]

    return x_screen, y_screen, z_ndc


# Shader solo de prueba
def lambert_shader(bar, verts, texCoords, texture=None):
    nx = verts[0][3] * bar[0] + verts[1][3] * bar[1] + verts[2][3] * bar[2]
    ny = verts[0][4] * bar[0] + verts[1][4] * bar[1] + verts[2][4] * bar[2]
    nz = verts[0][5] * bar[0] + verts[1][5] * bar[1] + verts[2][5] * bar[2]

    normal = np.array([nx, ny, nz])
    normal = normal / np.linalg.norm(normal)

    light_dir = np.array([0, 0, -1])
    light_dir = light_dir / np.linalg.norm(light_dir)

    intensity = max(0, np.dot(normal, -light_dir))

    if texture:
        base_color = texture.get_color(texCoords[0], texCoords[1])
    else:
        base_color = [1, 1, 1]

    return [channel * intensity for channel in base_color]

# Shader 1: Holograma
def hologram_shader(bar, verts, texCoords, texture=None, time=0):
    y = verts[0][1] * bar[0] + verts[1][1] * bar[1] + verts[2][1] * bar[2]
    z = verts[0][2] * bar[0] + verts[1][2] * bar[1] + verts[2][2] * bar[2]

    nx = verts[0][3] * bar[0] + verts[1][3] * bar[1] + verts[2][3] * bar[2]
    ny = verts[0][4] * bar[0] + verts[1][4] * bar[1] + verts[2][4] * bar[2]
    nz = verts[0][5] * bar[0] + verts[1][5] * bar[1] + verts[2][5] * bar[2]
    normal = np.array([nx, ny, nz])
    normal = normal / np.linalg.norm(normal)

    light_dir = np.array([0, 0, -1])
    intensity = max(0.3, np.dot(normal, -light_dir))

    scan = 0.5 + 0.5 * math.sin(y * 20 + time * 6)
    flicker = 0.9 + 0.1 * math.sin(time * 12 + z * 50)

    base_color = [0.1, 1.0, 0.8]

    final_color = [c * intensity * scan * flicker for c in base_color]
    return final_color

# Shader 2: Tv antigua
def crt_shader(bar, verts, texCoords, texture=None, time=0):
    import math

    u, v = texCoords
    x = u * 512
    y = v * 512

    scanline = 0.9 if int(y) % 2 == 0 else 0.6

    flicker = 0.95 + 0.05 * math.sin(time * 40 + y * 0.1)

    wave = 0.005 * math.sin(time * 5 + y * 0.2)
    u_distorted = u + wave

    if texture:
        base_color = texture.get_color(u_distorted, v)
    else:
        base_color = [1, 1, 1]

    gray = sum(base_color) / 3
    desaturated = [gray * 0.6 + c * 0.4 for c in base_color]

    final_color = [c * scanline * flicker for c in desaturated]
    return final_color