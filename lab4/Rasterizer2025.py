import pygame
import os
import math
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader, hologram_shader, crt_shader 
from BMPTexture import BMPTexture
from MathLib import LookAtMatrix, ProjectionMatrix, ViewportMatrix

# ------------------ Configuración inicial ------------------

width = 512
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption("Software Rasterizer")
clock = pygame.time.Clock()

rend = Renderer(screen)

# ------------------ Carga de modelo y textura ------------------

base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "models/mimikyu.obj")
texture_path = os.path.join(base_path, "textures/Mimigma.bmp")

texture = BMPTexture(texture_path)
triangleModel = Model(model_path, texture=texture)  

# Asignar shaders
triangleModel.vertexShader = vertexShader
triangleModel.fragmentShader = crt_shader

# Transformaciones iniciales
triangleModel.translation = [0, -0.5, 0]
triangleModel.scale = [1, 1, 1]
triangleModel.rotation = [0, -math.pi / 1.5, 0]

rend.models.append(triangleModel)
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        triangleModel.translation[0] += 10 * deltaTime
    if keys[pygame.K_LEFT]:
        triangleModel.translation[0] -= 10 * deltaTime
    if keys[pygame.K_UP]:
        triangleModel.translation[1] += 10 * deltaTime
    if keys[pygame.K_DOWN]:
        triangleModel.translation[1] -= 10 * deltaTime
    if keys[pygame.K_d]:
        triangleModel.rotation[2] += 2 * deltaTime
    if keys[pygame.K_a]:
        triangleModel.rotation[2] -= 2 * deltaTime
    if keys[pygame.K_w]:
        triangleModel.scale = [s + deltaTime for s in triangleModel.scale]
    if keys[pygame.K_s]:
        triangleModel.scale = [max(0.01, s - deltaTime) for s in triangleModel.scale]

    # ------------------ Render ------------------

    rend.glClear()
    rend.glRender(viewMatrix, projectionMatrix, viewportMatrix, time=totalTime)
    pygame.display.flip()

# ------------------ Salida final ------------------

GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()