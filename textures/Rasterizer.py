from gl import Renderer
import shadedrs
from obj import Obj

width = 2048
height = 2048

rend = Renderer(width,height)

rend.vertexShader = shadedrs.vertexShader
rend.fragmentShader = shadedrs.fragmentShader


rend.glLoadModel(filename = "SewingMachine.obj", 
                  textureName= "wood.bmp", 
                  translate=(700, 1500, 0), 
                  rotate=(-1.5, 180, 0.5), 
                  scale=(1270, 1270, 1270))

rend.glLoadModel(filename = "SewingMachine.obj", 
                  textureName= "wood.bmp", 
                  translate=(600, 200, 0), 
                  rotate=(-1.5, 0, 0.5), 
                  scale=(1570, 1570, 1570))

rend.glLoadModel(filename = "SewingMachine.obj", 
                  textureName= "wood.bmp", 
                  translate=(1500, 1500, 0), 
                  rotate=(80, 70, 90), 
                  scale=(1170, 1170, 1170))

rend.glLoadModel(filename = "SewingMachine.obj", 
                  textureName= "wood.bmp", 
                  translate=(1800, 600, 0), 
                  rotate=(270, 90, 0), 
                  scale=(1270, 1270, 1270)) 

rend.glRender()

rend.glFinish("R2-textures.bmp")