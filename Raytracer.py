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

cakeTexture= pygame.image.load("images/cake.jpg")

brick = Material(diffuse=(1,0.4,0.4), spec = 8,  Ks = 0.01)
cake= Material(texture=cakeTexture)
mirror = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9), spec = 32, Ks = 0.15, matType = REFLECTIVE)
marble_polished = Material(diffuse=(0.8, 0.8, 0.8), spec=128, Ks=0.5)
concrete = Material(diffuse=(0.7, 0.7, 0.7), spec=16, Ks=0.2)
concrete_dark = Material(diffuse=(0.6, 0.6, 0.6), spec=16, Ks=0.2)
drywall = Material(diffuse=(0.9, 0.9, 0.9), spec=16, Ks=0.1)

#Cilindros
rt.scene.append(Cylinder(position=(0.5,-1,-1), radius = 0.1, height=0.2, material = brick)) #Derecha
rt.scene.append(Cylinder(position=(-0.5,0.1,-1), radius = 0.1, height=0.2, material = concrete)) #Izquierda

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


