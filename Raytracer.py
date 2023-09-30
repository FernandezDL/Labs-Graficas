import pygame
from pygame.locals import * 

from rt import Raytracer
from figuras import *
from lights import *
from material import *

width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rt = Raytracer(screen)
rt.envMap = pygame.image.load("images/hamiltonStage.jpg")
rt.rtClearColor(0.27,0.36,0.52)

flowTexture = pygame.image.load("images/flow.jpg")

brick = Material(diffuse=(1,0.4,0.4), spec = 8,  Ks = 0.01)
grass = Material(diffuse=(0.4,1,0.4), spec = 32,  Ks = 0.1)
water = Material(diffuse=(0.4,0.4,1), spec = 256, Ks = 0.2)

mirror = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9), spec = 32, Ks = 0.15, matType = REFLECTIVE)
colorFlow = Material(texture = flowTexture)
reflectFlow = Material(texture = flowTexture, spec = 64, Ks = 0.1, matType= REFLECTIVE)

glass = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.15, ior = 1.5, matType = TRANSPARENT)
diamond = Material(diffuse=(0.9,0.9,0.9), spec = 64, Ks = 0.2, ior = 2.417, matType = TRANSPARENT)

# rt.scene.append(Sphere(position=(-2,0,-7), radius = 1.5, material = reflectFlow))
# rt.scene.append(Sphere(position=(2,0,-7), radius = 2, material = colorFlow))
# rt.scene.append(Sphere(position=(0,-1,-5), radius = 0.5, material = mirror))
rt.scene.append(Sphere(position=(-1,0,-5), radius = 1, material = glass))
rt.scene.append(Sphere(position=(1,0,-5), radius = 0.7, material = diamond))
rt.scene.append(Sphere(position=(0,1,-8), radius = 1, material = brick))


#Luces
rt.lights.append(AmbientLight(intensity=0.1))
rt.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity=0.9))

rt.rtClear()
rt.rtRender()

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
pygame.image.save(sub, "screenshot.jpg")

pygame.quit()


