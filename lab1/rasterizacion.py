import pygame
from gl import Renderer

width = 640
height = 480

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    # poligono 1
    # (165, 380) (185, 360) (180, 330) (207, 345) (233, 330) (230, 360) (250, 380) (220, 385) (205, 410) (193, 383)
    rend.glClear()
    rend.glLine((165, 380), (185, 360))
    rend.glLine((185, 360), (180, 330))
    rend.glLine((180, 330), (207, 345))
    rend.glLine((207, 345), (233, 330))
    rend.glLine((233, 330), (230, 360))
    rend.glLine((230, 360), (250, 380))
    rend.glLine((250, 380), (220, 385))
    rend.glLine((220, 385), (205, 410))
    rend.glLine((205, 410), (193, 383))
    rend.glLine((193, 383), (165, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()