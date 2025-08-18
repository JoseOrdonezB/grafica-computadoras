import pygame
import os
import math
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader, hologram_shader, old_tv_shader, wave_shader, pulsating_vertex_shader
from BMPTexture import BMPTexture
from MathLib import LookAtMatrix, ProjectionMatrix, ViewportMatrix

# ------------------ Configuración inicial ------------------

width = 1200
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption("Software Rasterizer")
clock = pygame.time.Clock()

rend = Renderer(screen)

# ------------------ Carga de modelo y textura ------------------

base_path = os.path.dirname(__file__)

# Mimikiy model and texture paths
mimikyu_model_path = os.path.join(base_path, "models/mimikyu.obj")
mimikyu_texture_path = os.path.join(base_path, "textures/Mimigma.bmp")
mimikyu_texture = BMPTexture(mimikyu_texture_path)

# Poliwhirl model and texture paths
poliwhirl_mode_path = os.path.join(base_path, 'models/poliwhirl.obj')
poliwhirl_texture_path = os.path.join(base_path, 'textures/poliwhirl.bmp')
poliwhirl_texture = BMPTexture(poliwhirl_texture_path)

# Asignar modelo y textura a múltiples instanacias
mimikyu = Model(mimikyu_model_path, texture=mimikyu_texture)
poliwhirl = Model(poliwhirl_mode_path, texture=poliwhirl_texture)



# Asignar shaders
mimikyu.vertexShader = vertexShader
mimikyu.fragmentShader = None
poliwhirl.vertexShader = vertexShader
poliwhirl.fragmentShader = None

# Transformaciones iniciales en fila horizontal
mimikyu.translation = [-3, -0.5, 0]
mimikyu.scale = [1, 1, 1]
mimikyu.rotation = [0, -math.pi / 1.5, 0]

poliwhirl.translation = [-1, -0.5, 0]
poliwhirl.scale = [0.5, 0.5, 0.5]
poliwhirl.rotation = [-math.pi/2, 0, math.pi]

# mimikyu2.translation = [1, -0.5, 0]
# mimikyu2.scale = [1, 1, 1]
# mimikyu2.rotation = [0, -math.pi / 1.5, 0]

# mimikyu3.translation = [3, -0.5, 0]
# mimikyu3.scale = [1, 1, 1]
# mimikyu3.rotation = [0, -math.pi / 1.5, 0]


rend.models.append(mimikyu)
rend.models.append(poliwhirl)

rend.primitiveType = TRIANGLES

# ------------------ Cámaras ------------------

def get_camera_matrices(shot):
    eye = [0, 0, 3]
    target = [0, 0, 0]
    up = [0, 1, 0]

    if shot == "medium":
        eye = [0, 0, 3]
        up = [0, 1, 0]
    elif shot == "low":
        eye = [0, -1, 2]
        up = [0, 1, 0]
    elif shot == "high":
        eye = [0, 1, 2]
        up = [0, 1, 0]
    elif shot == "dutch":
        eye = [0, 0, 3]
        up = [1, 0.3, 0]

    view = LookAtMatrix(eye, target, up)
    projection = ProjectionMatrix(60, width / height, 0.1, 100)
    viewport = ViewportMatrix(0, 0, width, height)
    return view, projection, viewport

shot_type = "medium"
viewMatrix, projectionMatrix, viewportMatrix = get_camera_matrices(shot_type)

# ------------------ Bucle principal ------------------

isRunning = True
totalTime = 0 

while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    totalTime += deltaTime 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                rend.primitiveType = POINTS
            elif event.key == pygame.K_2:
                rend.primitiveType = LINES
            elif event.key == pygame.K_3:
                rend.primitiveType = TRIANGLES

            elif event.key == pygame.K_z:
                shot_type = "medium"
                print("Medium shot")
            elif event.key == pygame.K_x:
                shot_type = "low"
                print("Low angle")
            elif event.key == pygame.K_c:
                shot_type = "high"
                print("High angle")
            elif event.key == pygame.K_v:
                shot_type = "dutch"
                print("Dutch angle")

            viewMatrix, projectionMatrix, viewportMatrix = get_camera_matrices(shot_type)

    # ------------------ Transformaciones interactivas ------------------

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT]:
    #     triangleModel.translation[0] += 10 * deltaTime
    # if keys[pygame.K_LEFT]:
    #     triangleModel.translation[0] -= 10 * deltaTime
    # if keys[pygame.K_UP]:
    #     triangleModel.translation[1] += 10 * deltaTime
    # if keys[pygame.K_DOWN]:
    #     triangleModel.translation[1] -= 10 * deltaTime
    # if keys[pygame.K_d]:
    #     triangleModel.rotation[2] += 2 * deltaTime
    # if keys[pygame.K_a]:
    #     triangleModel.rotation[2] -= 2 * deltaTime
    # if keys[pygame.K_w]:
    #     triangleModel.scale = [s + deltaTime for s in triangleModel.scale]
    # if keys[pygame.K_s]:
    #     triangleModel.scale = [max(0.01, s - deltaTime) for s in triangleModel.scale]

    # ------------------ Render ------------------

    rend.glClear()
    rend.glRender(viewMatrix, projectionMatrix, viewportMatrix, time=totalTime)
    pygame.display.flip()

# ------------------ Salida final ------------------

GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()