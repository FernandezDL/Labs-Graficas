
import libreria as lb

class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType

    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intercept, viewPos):
        return None

class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,1,1)):
        super().__init__(intensity, color, "Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0, -1, 0),intensity=1, color=(1, 1, 1)):
        self.direction = lb.normalize_vector(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):

        dir = [(i * -1) for i in self.direction]

        intensity = lb.dot_product(intercept.normal, dir) * self.intensity
        intensity = max(0, min(1,intensity))
        intensity *= 1 - intercept.obj.material.Ks

        diffuseColor = [(i * intensity) for i in self.color]

        return diffuseColor

    def getSpecularColor(self, intercept, viewPos):
        
        dir = [(i * -1) for i in self.direction]
        reflect = lb.reflect_vector(intercept.normal, dir)

        viewDir = [viewPos[i] - intercept.point[i] for i in range(3)]
        viewDir = lb.normalize_vector(viewDir)

        specIntensity = max(0, lb.dot_product(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity

        specColor = [(i * specIntensity) for i in self.color]

        return specColor
        
class PointLight(Light):
    def __init__(self, point = (0,0,0), intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")

    def getDiffuseColor(self, intercept):
        dir = lb.subtract_vectors(self.point, intercept.point)
        R = lb.vector_norm(dir)
        dir = lb.normalize_vector(dir)

        intensity = lb.dot_product(intercept.normal, dir) * self.intensity
        intensity *= 1 - intercept.obj.material.Ks

        if R != 0:
            intensity /= R ** 2

        intensity = max(0, min(1,intensity))

        return [(i * intensity) for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = lb.subtract_vectors(self.point, intercept.point)
        R = lb.vector_norm(dir)
        dir = lb.normalize_vector(dir)

        reflect = lb.reflect_vector(intercept.normal, dir)

        viewDir = lb.subtract_vectors(viewPos, intercept.point)
        viewDir = lb.normalize_vector(viewDir)

        specIntensity = max(0, lb.dot_product(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity

        if R != 0:
            specIntensity /= R ** 2
        specIntensity = max(0, min(1,specIntensity))


        specColor = [(i * specIntensity) for i in self.color]

        return specColor