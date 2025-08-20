import pygame
import os
import math
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader, rainbow_shader, wave_vertex_shader, hypno_rings_shader, sway_twist_vertex_shader, wobble_head_vertex_shader, hypno_checker_shader, contraction_wave_vertex_shader, vortex_spiral_shader
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

# Horse model and texture paths
horse_model_path = os.path.join(base_path, "models/10026_Horse_v01-it2.obj")
horse_texture_path = os.path.join(base_path, "textures/Horse_v01.bmp")
horse_texture = BMPTexture(horse_texture_path)

# Frog model and texture paths
frog_model_path = os.path.join(base_path, 'models/20436_Frog_v1 textured.obj')
frog_texture_path = os.path.join(base_path, 'textures/20436_Frog_diff.bmp')
frog_texture = BMPTexture(frog_texture_path)

# Sealion model and texture paths
sealion_model_path = os.path.join(base_path, 'models/10041_sealion_v1_L3.obj')
sealion_texture_path = os.path.join(base_path, 'textures/10041_sealion_v1_Diffuse.bmp')
sealion_texture = BMPTexture(sealion_texture_path)

# Duck model and texture paths
duck_model_path = os.path.join(base_path, 'models/12248_Bird_v1_L2.obj')
duck_texture_path = os.path.join(base_path, 'textures/12248_Bird_v1_diff.bmp')
duck_texture = BMPTexture(duck_texture_path)

# Asignar modelo y textura a múltiples instanacias
horse = Model(horse_model_path, texture=horse_texture)
frog = Model(frog_model_path, texture=frog_texture)
sealion = Model(sealion_model_path, texture=sealion_texture)
duck = Model(duck_model_path, texture=duck_texture)




# Asignar shaders
horse.vertexShader = sway_twist_vertex_shader
horse.fragmentShader = hypno_rings_shader
frog.vertexShader = wave_vertex_shader
frog.fragmentShader = rainbow_shader
sealion.vertexShader = contraction_wave_vertex_shader
sealion.fragmentShader = vortex_spiral_shader
duck.vertexShader = wobble_head_vertex_shader
duck.fragmentShader = hypno_checker_shader

# Transformaciones iniciales en fila horizontal
horse.translation = [-2, -0.5, 1]
horse.scale = [0.0003, 0.0003, 0.0003]
horse.rotation = [math.pi/2, math.pi, 0]

frog.translation = [0, -0.5, -2]
frog.scale = [0.2, 0.2, 0.2]
frog.rotation = [math.pi/2, math.pi, 0]

sealion.translation = [0, -0.5, 1]
sealion.scale = [0.007, 0.007, 0.007]
sealion.rotation = [math.pi/2, math.pi, 0]

duck.translation = [2, -0.5, 1]
duck.scale = [0.008, 0.008, 0.008]
duck.rotation = [math.pi/2, math.pi, 0]


rend.models.append(horse)
rend.models.append(frog)
rend.models.append(sealion)
rend.models.append(duck)

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