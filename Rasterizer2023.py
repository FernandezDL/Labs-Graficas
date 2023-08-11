from gl import Renderer, Model
import shaders

# El tama�o del FrameBuffer
width = 560
height = 540

# Se crea el renderizador
rend = Renderer(width, height)

# Le damos los shaders que se utilizar�s
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.emissionShader

#Medium Shoot
# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "models/SewingMachine.obj",
                 textureName = "textures/wood.bmp",
                 translate = (-0.15, -0.3, -2),
                 rotate = (0, 0, 0),
                 scale = (3,3,3)) 

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("photoshoot/mediumAngle.bmp")