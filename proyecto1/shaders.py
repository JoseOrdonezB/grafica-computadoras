import numpy as np
import math
import random

def _clamp01(x: float) -> float:
    if not math.isfinite(x):
        return 0.0
    if x < 0.0: return 0.0
    if x > 1.0: return 1.0
    return x

def _rgb(r: float, g: float, b: float):
    return (_clamp01(r), _clamp01(g), _clamp01(b))

def _norm_tex_rgb(tex_color):
    if not tex_color or len(tex_color) < 3:
        return (1.0, 1.0, 1.0)
    r, g, b = tex_color[:3]
    if (isinstance(r, (int, float)) and r > 1) or \
       (isinstance(g, (int, float)) and g > 1) or \
       (isinstance(b, (int, float)) and b > 1):
        r, g, b = r/255.0, g/255.0, b/255.0
    return (_clamp01(float(r)), _clamp01(float(g)), _clamp01(float(b)))

def _sane_uv(u, v):
    if not math.isfinite(u): u = 0.0
    if not math.isfinite(v): v = 0.0
    return max(0.0, min(1.0, u)), max(0.0, min(1.0, v))

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

# --- Frog shaders ---
def rainbow_shader(bar, verts, texCoords, texture=None, time=0):
    # Posiciones pantalla para animación (no afectan a coordenadas reales)
    x = verts[0][0] * bar[0] + verts[1][0] * bar[1] + verts[2][0] * bar[2]
    y = verts[0][1] * bar[0] + verts[1][1] * bar[1] + verts[2][1] * bar[2]

    t = (x * 0.02 + y * 0.02 + time * 2)

    r = 0.5 + 0.5 * math.sin(t)
    g = 0.5 + 0.5 * math.sin(t + 2*math.pi/3)
    b = 0.5 + 0.5 * math.sin(t + 4*math.pi/3)

    nx = verts[0][3] * bar[0] + verts[1][3] * bar[1] + verts[2][3] * bar[2]
    ny = verts[0][4] * bar[0] + verts[1][4] * bar[1] + verts[2][4] * bar[2]
    nz = verts[0][5] * bar[0] + verts[1][5] * bar[1] + verts[2][5] * bar[2]
    nlen = math.sqrt(nx*nx + ny*ny + nz*nz) + 1e-8
    nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
    lx, ly, lz = 0.0, 0.0, -1.0
    llen = math.sqrt(lx*lx + ly*ly + lz*lz) + 1e-8
    lx, ly, lz = lx/llen, ly/llen, lz/llen
    ndotl = -(nx*lx + ny*ly + nz*lz)
    intensity = max(0.2, ndotl)

    u, v = _sane_uv(*texCoords)
    base = _norm_tex_rgb(texture.get_color(u, v)) if texture else (1.0, 1.0, 1.0)
    mix_amount = 0.45

    out_r = (base[0] * (1 - mix_amount) + r * mix_amount) * intensity
    out_g = (base[1] * (1 - mix_amount) + g * mix_amount) * intensity
    out_b = (base[2] * (1 - mix_amount) + b * mix_amount) * intensity

    return _rgb(out_r, out_g, out_b)

def wave_vertex_shader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    time = kwargs.get("time", 0)

    x, y, z = vertex[:3]

    r = math.sqrt(x**2 + y**2 + z**2)
    offset = 0.05 * math.sin(r*6 - time*3)

    pos = np.array([[x + x*offset],
                    [y + y*offset],
                    [z + z*offset],
                    [1]], dtype=np.float32)

    vt = projectionMatrix @ viewMatrix @ modelMatrix @ pos
    w = vt[3,0] if vt[3,0] != 0 else 1
    vt /= w
    vt = viewportMatrix @ vt

    return int(vt[0,0]), int(vt[1,0]), vt[2,0]

# --- Horse shaders ---
def hypno_rings_shader(bar, verts, texCoords, texture=None, time=0):
    u, v = _sane_uv(*texCoords)
    base = _norm_tex_rgb(texture.get_color(u, v)) if texture else (1.0, 1.0, 1.0)

    du, dv = u - 0.5, v - 0.5
    r = math.sqrt(du*du + dv*dv) + 1e-8
    theta = math.atan2(dv, du)

    wave = 0.5 + 0.5 * math.sin(r * 18.0 - time * 4.0 + theta * 3.0)

    r_mul = 0.9 + 0.25 * wave
    g_mul = 0.9 + 0.25 * (1.0 - wave)
    b_mul = 0.9 + 0.25 * wave

    nx = verts[0][3]*bar[0] + verts[1][3]*bar[1] + verts[2][3]*bar[2]
    ny = verts[0][4]*bar[0] + verts[1][4]*bar[1] + verts[2][4]*bar[2]
    nz = verts[0][5]*bar[0] + verts[1][5]*bar[1] + verts[2][5]*bar[2]
    nlen = math.sqrt(nx*nx + ny*ny + nz*nz) + 1e-8
    nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
    lx, ly, lz = 0.0, 0.0, -1.0
    llen = math.sqrt(lx*lx + ly*ly + lz*lz) + 1e-8
    lx, ly, lz = lx/llen, ly/llen, lz/llen
    ndotl = -(nx*lx + ny*ly + nz*lz)
    intensity = max(0.2, ndotl)

    out_r = base[0] * r_mul * intensity
    out_g = base[1] * g_mul * intensity
    out_b = base[2] * b_mul * intensity

    return _rgb(out_r, out_g, out_b)

def sway_twist_vertex_shader(vertex, **kwargs):
    import numpy as np, math
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    time = kwargs.get("time", 0)

    x, y, z = vertex[:3]

    angle = 0.15 * math.sin(time * 1.5 + y * 2.0)
    bob   = 0.02 * math.sin(time * 1.2)

    ca, sa = math.cos(angle), math.sin(angle)
    x2 = x * ca - z * sa
    z2 = x * sa + z * ca
    y2 = y + bob

    pos = np.array([[x2], [y2], [z2], [1.0]], dtype=np.float32)

    vt = projectionMatrix @ viewMatrix @ modelMatrix @ pos
    w = vt[3, 0] if vt[3, 0] != 0 else 1.0
    vt /= w
    vt = viewportMatrix @ vt

    return int(vt[0, 0]), int(vt[1, 0]), vt[2, 0]

# --- Duck shaders ---
def hypno_checker_shader(bar, verts, texCoords, texture=None, time=0):
    u, v = _sane_uv(*texCoords)
    base = _norm_tex_rgb(texture.get_color(u, v)) if texture else (1.0, 1.0, 1.0)

    freq = 8.0
    wave = math.sin(time*2.0)
    check = (int((u*freq + wave) % 2) ^ int((v*freq + wave) % 2))

    c0 = (0.9, 0.3, 0.9)
    c1 = (0.3, 0.9, 0.9)
    tint = c1 if check else c0

    out_r = base[0]*0.6 + tint[0]*0.4
    out_g = base[1]*0.6 + tint[1]*0.4
    out_b = base[2]*0.6 + tint[2]*0.4

    return _rgb(out_r, out_g, out_b)

def wobble_head_vertex_shader(vertex, **kwargs):
    import numpy as np, math
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    time = kwargs.get("time", 0)

    x, y, z = vertex[:3]

    sway = 0.05 * math.sin(time*2.0 + y*3.0)
    x2 = x + sway
    z2 = z + 0.5*sway

    pos = np.array([[x2],[y],[z2],[1.0]], dtype=np.float32)

    vt = projectionMatrix @ viewMatrix @ modelMatrix @ pos
    w = vt[3,0] if vt[3,0] != 0 else 1.0
    vt /= w
    vt = viewportMatrix @ vt

    return int(vt[0,0]), int(vt[1,0]), vt[2,0]

# --- Sealion shaders ---
def vortex_spiral_shader(bar, verts, texCoords, texture=None, time=0):
    u, v = _sane_uv(*texCoords)
    base = _norm_tex_rgb(texture.get_color(u, v)) if texture else (1.0, 1.0, 1.0)

    du, dv = u - 0.5, v - 0.5
    r = math.sqrt(du*du + dv*dv) + 1e-8
    theta = math.atan2(dv, du)

    phase  = 6.0*theta - 10.0*r + time*2.0
    spiral = 0.5 + 0.5*math.sin(phase)
    glow   = spiral * spiral

    r_t = 0.6 + 0.4*math.sin(phase + 0.0)
    g_t = 0.6 + 0.4*math.sin(phase + 2*math.pi/3)
    b_t = 0.6 + 0.4*math.sin(phase + 4*math.pi/3)

    nx = verts[0][3]*bar[0] + verts[1][3]*bar[1] + verts[2][3]*bar[2]
    ny = verts[0][4]*bar[0] + verts[1][4]*bar[1] + verts[2][4]*bar[2]
    nz = verts[0][5]*bar[0] + verts[1][5]*bar[1] + verts[2][5]*bar[2]
    nlen = math.sqrt(nx*nx + ny*ny + nz*nz) + 1e-8
    nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
    lx, ly, lz = 0.0, 0.0, -1.0
    llen = math.sqrt(lx*lx + ly*ly + lz*lz) + 1e-8
    lx, ly, lz = lx/llen, ly/llen, lz/llen
    ndotl = -(nx*lx + ny*ly + nz*lz)
    if ndotl < 0.0: ndotl = 0.0
    intensity = 0.2 + 0.8*ndotl

    emissive = 0.35 * glow
    out_r = base[0]*intensity + r_t*emissive
    out_g = base[1]*intensity + g_t*emissive
    out_b = base[2]*intensity + b_t*emissive

    return _rgb(out_r, out_g, out_b)

def contraction_wave_vertex_shader(vertex, **kwargs):
    import numpy as np, math
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    time = kwargs.get("time", 0)

    x, y, z = vertex[:3]
    r = math.sqrt(x*x + y*y + z*z) + 1e-6
    dirx, diry, dirz = x/r, y/r, z/r

    amp   = 0.05
    speed = 2.0
    freq  = 6.0
    fall  = 1.0 / (1.0 + 1.5*r)

    disp = -amp * math.sin(time*speed - r*freq) * fall

    x2 = x + dirx * disp
    y2 = y + diry * disp
    z2 = z + dirz * disp

    vt = projectionMatrix @ viewMatrix @ modelMatrix @ np.array([[x2],[y2],[z2],[1.0]], dtype=np.float32)
    w = vt[3,0] if vt[3,0] != 0 else 1.0
    vt /= w
    vt = viewportMatrix @ vt

    return int(vt[0,0]), int(vt[1,0]), vt[2,0]