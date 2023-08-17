from gl import Renderer, Model
import shaders


# El tama�o del FrameBuffer
width = 560
height = 540

# Se crea el renderizador
rend = Renderer(width, height)

#Medium Shoot
# Cargamos los modelos que rederizaremos
model1= Model("models/SewingMachine.obj",
             translate = (-0.15, -0.3, -2),
             rotate = (0, 0, 0),
             scale = (3,3,3))
model1.LoadTexture("textures/wood.bmp")
model1.SetShaders(shaders.vertexShader, shaders.snakeShader)

rend.glAddModule(model1)

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("shaders/snakeShader.bmp")