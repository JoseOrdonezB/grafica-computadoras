import pygame
import os
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader
from BMPTexture import BMPTexture
import math

# Configuración de ventana
width = 512
height = 512
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption("Software Rasterizer")
clock = pygame.time.Clock()

rend = Renderer(screen)

# Rutas del modelo y textura
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "models/13463_Australian_Cattle_Dog_v3.obj")
texture_path = os.path.join(base_path, "textures/Australian_Cattle_Dog_dif.bmp")

# Cargar textura BMP
texture = BMPTexture(texture_path)

# Cargar modelo con textura
triangleModel = Model(model_path, texture=texture)
triangleModel.vertexShader = vertexShader

# Transformaciones iniciales (ajustar según el modelo)
triangleModel.translation = [0, -0.5, 0]               # mover un poco abajo
triangleModel.scale = [0.05, 0.05, 0.05]
triangleModel.rotation = [-math.pi / 2, 0, -math.pi]          # rotar -90° en eje X

# Agregar modelo a la lista
rend.models.append(triangleModel)
rend.primitiveType = TRIANGLES

# Loop principal
isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0

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

    # Controles de movimiento y rotación
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

    # Renderizar escena
    rend.glClear()
    rend.glRender()
    pygame.display.flip()

# Guardar imagen final
GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()