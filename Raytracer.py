import pygame
from pygame.locals import * 
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 550

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.rtClearColor(0.7, 0.5, 0.7)

#brick = Material(diffuse=(1,0.4,0.4), spec = 8,  ks = 0.01)
grass = Material(diffuse=(0.4, 1, 0.4), spec = 32,  ks = 0.1)
water = Material(diffuse=(0.4,0.4,1), spec = 256, ks = 0.2)
snow = Material(diffuse=(1,1,1), spec= 100, ks= 0.1)
rock = Material(diffuse=(0,0,0), spec=32, ks=0.2)
rock2 = Material(diffuse=(0.4, 0.3, 0.2), spec=8, ks=0.01)
carrot = Material(diffuse=(1, 0.6, 0), spec=256, ks= 0.2)

#Cuerpo
raytracer.scene.append(Sphere(position=(0,-1,-7), radius = 1, material = snow))
raytracer.scene.append(Sphere(position=(0,0.45,-7), radius = 0.8, material = snow))
raytracer.scene.append(Sphere(position=(0,1.65,-7), radius = 0.6, material = snow))

#Botones
raytracer.scene.append(Sphere(position=(0,-0.8, -6.2), radius=0.3, material= rock))
raytracer.scene.append(Sphere(position=(0,-0.1, -6.2), radius=0.2, material= rock))
raytracer.scene.append(Sphere(position=(0,0.6, -6.2), radius=0.16, material= rock))
 
#Piedras de la boca
raytracer.scene.append(Sphere(position=(-0.25   , 1.36 , -6), radius=0.05, material= rock2))
raytracer.scene.append(Sphere(position=(-0.15   , 1.25 , -6), radius=0.05, material= rock2))
raytracer.scene.append(Sphere(position=(0       , 1.18 , -6), radius=0.05, material= rock2))
raytracer.scene.append(Sphere(position=(0.15    , 1.25 , -6), radius=0.05, material= rock2))
raytracer.scene.append(Sphere(position=(0.25    , 1.36 , -6), radius=0.05, material= rock2))

#ojos
raytracer.scene.append(Sphere(position=(-0.15   , 1.8   , -6.2), radius=0.09, material= snow))
raytracer.scene.append(Sphere(position=(0.15    , 1.8   , -6.2), radius=0.09, material= snow))
raytracer.scene.append(Sphere(position=(0.15    , 1.8   , -6.1), radius=0.035, material= rock))
raytracer.scene.append(Sphere(position=(-0.15   , 1.8   , -6.1), radius=0.035, material= rock))

#Nariz
raytracer.scene.append(Sphere(position=(0   , 1.5   , -6.2), radius=0.09, material= carrot))

#iluminacion minima del ambiente
raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(1,-1,-1),intensity=0.7))

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False
    
    raytracer.rtClear()
    raytracer.rtRender()
    pygame.display.flip()
                
pygame.quit()           