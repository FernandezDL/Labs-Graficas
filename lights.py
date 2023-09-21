import numpy as np
import mathLib as ml

class Light(object):
    def __init__(self, intensity=1, color=(1,1,1), lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
        
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None
    
class AmbientLight(Light):
    def __init__(self,intensity=1,color=(1,1,1)):
        super().__init__(intensity,color, "Ambient")
        
class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0),intensity=1, color=(1, 1, 1)):
        self.direction= ml.normalize_vector(direction)
        super().__init__(intensity, color, "Directional")
        
    def getDiffuseColor(self,intercept):
        dir = [(i*-1) for i in self.direction]
        
        intensity = ml.dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        diffuseColor = [(i * intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [(i*-1) for i in self.direction]
        
        reflect = ml.reflectVector(intercept.normal,dir)
        
        viewDir = ml.vector_subtraction(viewPos, intercept.point)
        viewDir = ml.normalize_vector(viewDir)
        
        specIntensity = max(0, ml.dot_product(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity
        
        specColor = [(i * specIntensity) for i in self.color]
        
        return specColor
    
class PointLight(Light):
    def __init__(self, point=(0,0,0), intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = ml.vector_subtraction(self.point,intercept.point)
        R = ml.vector_normal(dir)

        dir = dir/R
        
        intensity = ml.dot_product(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks
        
        #Ley de cuadrados inversos
        # IF = Intensity/R^2
        #R es la distancia del punto intercepto a la luz punto
        if R!=0:
            intensity /= R**2
        
        intensity = max(0, min(1, intensity))

        diffuseColor = [(i * intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = ml.vector_subtraction(self.point,intercept.point)
        R = ml.vector_normal(dir)

        dir = dir/R
        
        reflect = ml.reflectVector(intercept.normal, dir)
        
        viewDir = ml.vector_subtraction(viewPos, intercept.point)
        viewDir = ml.normalize_vector(viewDir)
        
        specIntensity = max(0,ml.dot_product(viewDir,reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
        
        specIntensity = max(0, min(1, specIntensity))
        
        specColor = [(i * specIntensity) for i in self.color]
        
        return specColor