import pygame
import glm
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *

width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock= pygame.time.Clock()

rend= Renderer(screen)
rend.setShader(vertex_shader, fragment_shader)

obj= rend.loadModel(filename= "models/turtle.obj", 
                    texture="textures/turtle.jpg", 
                    position = (0,0, -6),
                    rotation = (-90, 0, 75),
                    scale = (0.3,0.3,0.3))

isRunning= True

while isRunning:
    deltaTime = clock.tick(60)/ 1000
    keys= pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    if keys[K_d]:
        rend.camPosition.x -= 5 * deltaTime

    elif keys[K_a]:
        rend.camPosition.x += 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.y -= 5 * deltaTime
        
    elif keys[K_s]:
        rend.camPosition.y += 5 * deltaTime

    if keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime
         
    elif keys[K_q]:
        rend.camPosition.z += 5 * deltaTime

    if keys[K_1]:
        rend.setShader(vertex_shader, fragment_shader)

    elif keys[K_2]:
        rend.setShader(vertex_shader, pie_shader)
    
    elif keys[K_3]:
        rend.setShader(vertex_shader, siren_shader)

    elif keys[K_4]:
        rend.setShader(vertex_shader, glitch_shader)

    elif keys[K_5]:
        rend.setShader(vertex_shader, mixColors_shader)

    obj.rotation.x += 45 * deltaTime

    rend.elapsedTime += deltaTime
    rend.render()

    pygame.display.flip()

pygame.quit()