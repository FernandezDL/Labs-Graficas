import glm
from obj import Obj
from model import Model
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self, screen):
        self.screen= screen
        _, _, self.width, self.height= screen.get_rect()

        self.clearColor= [0,0,0]

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.elapsedTime = 0.0
        self.scene =[]
        self.activeShader= None
        self.dirLight= glm.vec3(1,0,0)

        #View matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)

        #Projection Matrix
        self.projectionMatrix= glm.perspective(glm.radians(60),             #FOV
                                               self.width / self.height,    #Aspect Ratio
                                               0.1,                         #Near Plane
                                               1000)                        #Far Plane

    def getViewMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.camPosition)

        pitch = glm.rotate(identity, glm.radians(self.camPosition.x), glm.vec3(1,0,0))
        yaw = glm.rotate(identity, glm.radians(self.camPosition.y), glm.vec3(0,1,0))
        roll = glm.rotate(identity, glm.radians(self.camPosition.z), glm.vec3(0,0,1))

        rotationMat= pitch * yaw * roll

        camMatrix= translateMat * rotationMat 

        return glm.inverse(camMatrix)
    
    def setShader(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                               compileShader(fragmentShader, GL_FRAGMENT_SHADER))

        else:
            self.activeShader= None

    def loadModel(self, filename, texture, position = (0,0,-5), rotation = (0,0,0), scale = (1,1,1)):
        model = Obj(filename)

        objectData = []

        for face in model.faces:
            # Revisamos cuantos vertices tiene esta cara. Si tiene cuatro
            # vertices, hay que crear un segundo triangulo por cara
            vertCount = len(face)

            # Obtenemos los vertices de la cara actual.
            v0 = model.vertices[ face[0][0] - 1]
            v1 = model.vertices[ face[1][0] - 1]
            v2 = model.vertices[ face[2][0] - 1]
            if vertCount == 4:
                v3 = model.vertices[ face[3][0] - 1]

            # Obtenemos las coordenadas de textura de la cara actual
            vt0 = model.texcoords[face[0][1] - 1]
            vt1 = model.texcoords[face[1][1] - 1]
            vt2 = model.texcoords[face[2][1] - 1]
            if vertCount == 4:
                vt3 = model.texcoords[face[3][1] - 1]

            #Obtenemos las normales de la cara actual.
            vn0 = model.normals[face[0][2] - 1]
            vn1 = model.normals[face[1][2] - 1]
            vn2 = model.normals[face[2][2] - 1]
            if vertCount == 4:
                vn3 = model.normals[face[3][2] - 1]

            [objectData.append(i) for i in v0]
            [objectData.append(vt0[i]) for i in range (2)]
            [objectData.append(i) for i in vn0]

            [objectData.append(i) for i in v1]
            [objectData.append(vt1[i]) for i in range (2)]
            [objectData.append(i) for i in vn1]

            [objectData.append(i) for i in v2]
            [objectData.append(vt2[i]) for i in range (2)]
            [objectData.append(i) for i in vn2]

            if vertCount == 4:
                [objectData.append(i) for i in v0]
                [objectData.append(vt0[i]) for i in range (2)]
                [objectData.append(i) for i in vn0]

                [objectData.append(i) for i in v2]
                [objectData.append(vt2[i]) for i in range (2)]
                [objectData.append(i) for i in vn2]

                [objectData.append(i) for i in v3]
                [objectData.append(vt3[i]) for i in range (2)]
                [objectData.append(i) for i in vn3]

        newModel = Model(objectData)
        newModel.loadTexture(texture)
        newModel.position = glm.vec3(position)
        newModel.rotation = glm.vec3(rotation)
        newModel.scale = glm.vec3(scale)

        self.scene.append(newModel)

        return newModel

    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.activeShader is not None:
            glUseProgram(self.activeShader)

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.getViewMatrix()))

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"),
                               1,
                               GL_FALSE,
                               glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.activeShader, "time"),
                                             self.elapsedTime)

            """ glUniform3fv(glGetUniformLocation(self.activeShader, "dirLight"),
                                              1, glm.value_ptr(self.dirLight)) """

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"),
                               1,
                               GL_FALSE,
                               glm.value_ptr(obj.getModelMatrix()))

            obj.render()