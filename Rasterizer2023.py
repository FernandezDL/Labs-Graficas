from gl import Renderer
import shaders

# El tama�o del FrameBuffer
width = 560
height = 540

# Se crea el renderizador
rend = Renderer(width, height)

# Le damos los shaders que se utilizar�s
rend.vertexShader = shaders.vertexShader
rend.fragmentShader = shaders.gouradShader

#Medium Shoot
# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "models/SewingMachine.obj",
                 textureName = "textures/wood.bmp",
                 translate = (0, -0.3, -2),
                 rotate = (0, 90, 0),
                 scale = (3,3,3)) 

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("photoshoot/mediumAngle.bmp")

#---------------------------------------------------------

#Low Angle Shoot
""" rend.glLookAt(camPos=(0, -1.5, 0),
              eyePos=(0,2,-5))

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "models/SewingMachine.obj",
                 textureName = "textures/wood.bmp",
                 translate = (-0.1, -0.5, -2),
                 rotate = (0, 0, 0),
                 scale = (3,3,3))  
                 
# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("photoshoot/lowAngle.bmp")

#---------------------------------------------------------
"""

#High Angle Shoot
""" rend.glLookAt(camPos=(0, 1.5, 0),
              eyePos=(0,-2,-5))

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "models/SewingMachine.obj",
                 textureName = "textures/wood.bmp",
                 translate = (-0.1, -0.5, -2),
                 rotate = (0, 0, 0),
                 scale = (3,3,3)) 
                 
# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("photoshoot/highAngle.bmp")

#---------------------------------------------------------
"""

#Dutch Angle Shoot
""" rend.glLookAt(camPos=(0, 1.5, 0),
              eyePos=(0,-2,-5))

# Cargamos los modelos que rederizaremos
rend.glLoadModel(filename = "models/SewingMachine.obj",
                 textureName = "textures/wood.bmp",
                 translate = (0, -0.2, -2),
                 rotate = (-20, 20, 25),
                 scale = (3,3,3)) 
                 
# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("photoshoot/dutchAngle.bmp")

#---------------------------------------------------------
"""
