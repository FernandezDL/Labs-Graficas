import pygame
from pygame.locals import * 

from rt import Raytracer
from figuras import *
from lights import *
from material import *

width = 512
height =315

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rt = Raytracer(screen)
rt.rtClearColor(0.7,0.5,0.7)
rt.envMap = pygame.image.load("images/bikiniBottom.jpg")

jellyFishTexture= pygame.image.load("images/jellyFish.jpg")

jellyFish= Material(texture=jellyFishTexture)
greenMirror = Material(diffuse=(0.4,0.9,0.4), spec = 32, Ks = 0.15, matType = REFLECTIVE)
dirtyGlass = Material(diffuse=(0.7, 0.7, 0.7), spec=32, Ks=0.05, ior=1.5, matType=TRANSPARENT)


#Triangulos
#Superficie transparente
rt.scene.append(Triangle(vertices= [(0,-1,-3), (0,1,-3), (-2,2,-4)], material=dirtyGlass)) #Izquierda
rt.scene.append(Triangle(vertices=[(0,-1,-3), (0,1,-3), (2,2,-4)], material=dirtyGlass)) #Derecha
rt.scene.append(Triangle(vertices=[(0,1,-3), (2,2,-4), (-2,2,-4)], material=dirtyGlass)) #Tope

#Superficie opaca
rt.scene.append(Triangle(vertices=[(-4, -2, -5), (-3, 0, -5), (-1.5, -1, -5)], material= jellyFish)) 

#Superficie reflectiva
rt.scene.append(Triangle(vertices= [(4.2, -2.5, -5.7), (3, -2, -6), (4, 1, -6)], material=greenMirror)) #Izquierda
rt.scene.append(Triangle(vertices=[(4.2, -2.5, -5.7), (5.1, -2, -6), (4, 1, -6)], material=greenMirror)) #Derecha

#Luces
rt.lights.append(AmbientLight(intensity=1))

rt.rtClear()
rt.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

rect = pygame.Rect(0,0, width, height)
sub= screen.subsurface(rect)
pygame.image.save(sub, "images/screenshot.jpg")

pygame.quit()


