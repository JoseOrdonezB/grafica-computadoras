import pygame
from gl import *
from BMP_Writer import GenerateBMP
from model import Model
from shaders import vertexShader
import os

width = 512
height = 512

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "models/sheep.obj")
triangleModel = Model(model_path)
triangleModel.vertexShader = vertexShader
triangleModel.translation = [0, 0, 0]
triangleModel.scale = [0.5, 0.5, 0.5]

rend.models.append(triangleModel)

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
        triangleModel.rotation[2] += 20 * deltaTime
    if keys[pygame.K_a]:
        triangleModel.rotation[2] -= 20 * deltaTime

    if keys[pygame.K_w]:
        triangleModel.scale = [s + deltaTime for s in triangleModel.scale]
    if keys[pygame.K_s]:
        triangleModel.scale = [s - deltaTime for s in triangleModel.scale]

    rend.glClear()
    rend.glRender()
    pygame.display.flip()

GenerateBMP("output.bmp", width, height, 3, rend.frameBuffer)
pygame.quit()