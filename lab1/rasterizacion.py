import pygame
from gl import Renderer

width = 1080
height = 720

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rend = Renderer(screen)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False



    # poligono 1
    poly1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
    rend.glClear()
    rend.glPolygon(poly1)

    # poligono 2
    poly2 = [(321, 335), (288, 286), (339, 251), (374, 302)]
    
    rend.glPolygon(poly2)

    # poligono 3
    poly3 = [(377, 249), (411, 197), (436, 249)]
    
    rend.glPolygon(poly3)

    # poligono 4
    poly4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]
    
    rend.glPolygon(poly4)

    # poligono 5
    poly5 = [(682, 175), (708, 120), (735, 148), (739, 170)]
    
    rend.glPolygon(poly5)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()