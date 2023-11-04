from OpenGL.GL import * 
import glm
from numpy import array, float32
import pygame

class Model(object):
    def __init__(self, data):
        self.vertBuffer= array(data, dtype= float32)

        #Vertex Buffer Object
        self.VBO= glGenBuffers(1)

        #Vertex Array Object
        self.VAO= glGenVertexArrays(1)

        self.position = glm.vec3(0,0,0)
        self.rotation= glm.vec3(0,0,0)
        self.scale= glm.vec3(1,1,1)

    def loadTexture(self, textureName):
        self.textureSurface= pygame.image.load(textureName)
        self.textureData= pygame.image.tostring(self.textureSurface, "RGB", True)
        self.textureBuffer= glGenTextures(1)

    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.position)

        #Rotacion X - Pitch
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))

        #Rotacion Y - Yaw
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))

        #Rotacion Z - Roll
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMat= pitch * yaw * roll

        scaleMat= glm.scale(identity, self.scale)

        return translateMat * rotationMat * scaleMat

    def render(self):
        #Atar los buffers a la GPU
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        #Especificar información de vertices
        glBufferData(GL_ARRAY_BUFFER,           #Buffer ID
                     self.vertBuffer.nbytes,    #Buffer Size in Bytes
                     self.vertBuffer,           #Buffer Data
                     GL_STATIC_DRAW)            #Usage

        #Atributos vertices
        glVertexAttribPointer(0,                    #Attribute Number
                              3,                    #Size
                              GL_FLOAT,             #Type
                              GL_FALSE,             #Is it normalized
                              4 * 8,                #Stride
                              ctypes.c_void_p(0))   #Offset

        glEnableVertexAttribArray(0)

        #Atributos coordenadas de textura
        glVertexAttribPointer(1,                         #Attribute Number
                              2,                         #Size
                              GL_FLOAT,                  #Type
                              GL_FALSE,                  #Is it normalized
                              4 * 8,                     #Stride
                              ctypes.c_void_p(4 * 3))    #Offset

        glEnableVertexAttribArray(1)

        #Atributos normales
        glVertexAttribPointer(2,                         #Attribute Number
                              3,                         #Size
                              GL_FLOAT,                  #Type
                              GL_FALSE,                  #Is it normalized
                              4 * 8,                     #Stride
                              ctypes.c_void_p(4 * 5))    #Offset

        glEnableVertexAttribArray(2)

        #Activar la textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
        glTexImage2D(GL_TEXTURE_2D,                       #Texture Type
                     0,                                   #Positions
                     GL_RGB,                              #Internal format
                     self.textureSurface.get_width(),     #Width
                     self.textureSurface.get_height(),    #Height
                     0,                                   #Border
                     GL_RGB,                              #Format
                     GL_UNSIGNED_BYTE,                    #Type
                     self.textureData)                    #Data

        glGenerateTextureMipmap(self.textureBuffer)
         
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 8))