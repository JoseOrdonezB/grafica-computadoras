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
base_path = os.path.dirname(__file__)

width = 1512
height = 982
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption("Software Rasterizer")
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.glViewport(0, 0, width, height)

background_texture_path = os.path.join(base_path, 'textures/background.bmp')
rend.glLoadBackground(background_texture_path)

# ------------------ Carga de modelo y textura ------------------

# Mario model and texture paths
mario_model_path = os.path.join(base_path, 'models/Mario.obj')
mario_texture_path = os.path.join(base_path, 'textures/Base_Color.bmp')
mario_texture = BMPTexture(mario_texture_path)

# Steve model and texture paths
steve_model_path = os.path.join(base_path, 'models/minecraft_steve.obj')
steve_texture_path = os.path.join(base_path, 'textures/Minecraft_steve_skin.bmp')
steve_texture = BMPTexture(steve_texture_path)

# Kirby model and texture paths
kirby_model_path = os.path.join(base_path, 'models/kirby.obj')
kirby_texture_path = os.path.join(base_path, 'textures/dd489eac.bmp')
kirby_texture = BMPTexture(kirby_texture_path)

# Pikachu model and texture paths
pikachu_model_path = os.path.join(base_path, 'models/luigidoll.obj')
pikachu_texture_path = os.path.join(base_path, 'textures/7c33ed83.bmp')
pikachu_texture = BMPTexture(pikachu_texture_path)


# Asignar modelo y textura a múltiples instanacias
mario = Model(mario_model_path, texture=mario_texture)
steve = Model(steve_model_path, texture=steve_texture)
kirby = Model(kirby_model_path, texture=kirby_texture)
pikachu = Model(pikachu_model_path, texture=pikachu_texture)

# # Asignar shaders
mario.vertexShader = sway_twist_vertex_shader
mario.fragmentShader = hypno_checker_shader
steve.vertexShader = wave_vertex_shader
steve.fragmentShader = rainbow_shader
kirby.vertexShader = contraction_wave_vertex_shader
kirby.fragmentShader = vortex_spiral_shader
pikachu.vertexShader = wobble_head_vertex_shader
pikachu.fragmentShader = hypno_rings_shader

# # Transformaciones iniciales en fila horizontal
mario.translation = [-1, -0.4, 1]
mario.scale = [0.1, 0.1, 0.1]
mario.rotation = [0, math.pi/2, 0]

steve.translation = [-1, -0.2, -0.5]
steve.scale = [0.03, 0.03, 0.03]
steve.rotation = [0, -math.pi/9, 0]

kirby.translation = [1, -0.5, 1]
kirby.scale = [0.002, 0.002, 0.002]
kirby.rotation = [0, -math.pi/3, 0]

pikachu.translation = [1, -0.4, -0.5]
pikachu.scale = [0.02, 0.02, 0.02]
pikachu.rotation = [0, -math.pi/3, 0]


rend.models.append(mario)
rend.models.append(steve)
rend.models.append(kirby)
rend.models.append(pikachu)


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

    rend.glClearBackground()
    rend.glRender(viewMatrix, projectionMatrix, viewportMatrix, time=totalTime)
    pygame.display.flip()

# ------------------ Salida final ------------------

GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()