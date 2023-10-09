import pygame
from pygame.locals import * 

from rt import Raytracer
from figuras import *
from lights import *
from material import *

width = 250
height =250
depth= 600

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rt = Raytracer(screen)
rt.rtClearColor(0.7,0.5,0.7)

cakeTexture= pygame.image.load("images/cake.jpg")

brick = Material(diffuse=(1,0.4,0.4), spec = 8,  Ks = 0.01)
cake= Material(texture=cakeTexture)

marble_polished = Material(diffuse=(0.8, 0.8, 0.8), spec=128, Ks=0.5)
concrete = Material(diffuse=(0.7, 0.7, 0.7), spec=16, Ks=0.2)
concrete_dark = Material(diffuse=(0.6, 0.6, 0.6), spec=16, Ks=0.2)
drywall = Material(diffuse=(0.9, 0.9, 0.9), spec=16, Ks=0.1)
blueMirror = Material(diffuse=(0.4,0.4,0.9), spec = 32, Ks = 0.15, matType = REFLECTIVE)

#Paredes
rt.scene.append(Plane(position=(-100, 50, 0), normal=(1,0,0), material= concrete)) #Izquierda
rt.scene.append(Plane(position=(100, 50, 0), normal=(-1,0,0), material= concrete)) #Derecha
rt.scene.append(Plane(position=(0, 50, -depth/2), normal=(0,0,1), material= concrete_dark)) #Fondo

#Techo
rt.scene.append(Plane(position=(0, 100, 0), normal=(0,-1,0), material= drywall))

#Piso
rt.scene.append(Plane(position=(0, -50, 0), normal=(0,1,0), material= marble_polished))

#Cubos
rt.scene.append(AABB(position=(-1.5, 1.5, -5), size=(1,1,1), material=brick))
rt.scene.append(AABB(position=(-0.9, -1.5, -5), size=(1,1,1), material= cake))

#Disco
rt.scene.append(Disk(position=(1, 0.5, -4), normal=(0, -0.8, 0.3), radius=1, material= blueMirror))

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


