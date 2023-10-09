from math import pi, atan2, acos, sqrt
import mathLib as ml

class Intercept(object):
    def __init__(self, distance, point, normal, obj, texcoords):
        self.distance = distance
        self.point =point
        self.normal = normal
        self.texcoords = texcoords
        self.obj = obj

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def ray_intersect(self, orig, dir):
        return None
    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        self.radius = radius
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        L = ml.vector_subtraction(self.position, orig) 
        lengthL = ml.vector_normal(L)
        tca = ml.dot_product(L, dir)
        d = sqrt(lengthL ** 2 - tca ** 2)

        if d > self.radius:
            return None
        
        thc = sqrt(self.radius ** 2 - d ** 2)
        t0 = tca - thc
        t1 = tca + thc
        if t0 <= 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = ml.add_vector_scaled(orig, t0, dir)
        normal = ml.vector_subtraction(P, self.position)
        normal_length = ml.vector_normal(normal)
        normal = [normal[i] / normal_length for i in range(3)]

        u = (atan2(normal[2], normal[0]) / (2*pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance= t0,
                         point= P,
                         normal= normal,
                         texcoords= (u,v),
                         obj= self)


class Plane(Shape):
    def __init__(self, position, normal, material):
        self.normal = ml.normalize_vector(normal)
        super().__init__(position, material)
    
    def ray_intersect(self, orig, dir):
        #Distancia = (planePos - origRay) o normal) / (dirRay o normal)
        
        denom = ml.dot_product(dir, self.normal)
        
        if abs(denom) <= 0.0001:
            return None
        
        num = ml.dot_product(ml.vector_subtraction(self.position, orig), self.normal)
        t = num/denom
        
        if t<0:
            return None
        
        p = ml.vector_addition(orig, ml.multiply_scalar_array(t, dir))
        
        return Intercept(distance = t,
                         point = p,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        self.radius = radius
        super().__init__(position, normal, material)
    
    def ray_intersect(self, orig, dir):
        planeIntersect = super().ray_intersect(orig, dir)
        
        if planeIntersect is None:
            return None
        
        contactDistance = ml.vector_subtraction(planeIntersect.point, self.position)
        contactDistance = ml.vector_normal(contactDistance)
        
        if contactDistance > self.radius:
            return None
        
        return Intercept(distance = planeIntersect.distance,
                         point = planeIntersect.point,
                         normal = self.normal,
                         texcoords= None,
                         obj = self)

class AABB(Shape):
    #Axis Aligned Bounding Box

    def __init__(self, position, size, material):
        self.size = size
        super().__init__(position, material)
        
        self.planes=[]
        
        self.size= size
    
        leftPlane= Plane(ml.vector_addition(self.position, (-size[0]/ 2,0,0)), (-1,0,0), material)
        rigthPlane= Plane(ml.vector_addition(self.position, (size[0]/ 2,0,0)), (1,0,0), material)
            
        bottomPlane= Plane(ml.vector_addition(self.position, (0,-size[1]/ 2,0)), (0,-1,0), material)
        topPlane= Plane(ml.vector_addition(self.position, (0,size[1]/ 2,0)), (0,1,0), material)

        backPlane= Plane(ml.vector_addition(self.position, (0,0, -size[2]/ 2)), (0,0,-1), material)
        frontPlane= Plane(ml.vector_addition(self.position, (0,0, size[2]/ 2)), (0,0,1), material)

        self.planes.append(leftPlane)
        self.planes.append(rigthPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        #Bounds
        self.boundsMin= [0,0,0]
        self.boundsMax= [0,0,0]

        bias= 0.001

        for i in range(3):
            self.boundsMin[i]= self.position[i] - (bias + size[i] / 2)
            self.boundsMax[i]= self.position[i] + (bias + size[i] / 2)
    
    def ray_intersect(self, orig, dir):
        intersect= None
        t= float('inf')

        u= 0
        v= 0

        for plane in self.planes:
            planeIntersect= plane.ray_intersect(orig, dir)

            if planeIntersect is not None:
                planePoint= planeIntersect.point

                if self.boundsMin[0] < planePoint[0] < self.boundsMax[0]:
                    if self.boundsMin[1] < planePoint[1] < self.boundsMax[1]:
                        if self.boundsMin[2] < planePoint[2] < self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t= planeIntersect.distance
                                intersect= planeIntersect

                                #Generar las uvs
                                if abs(plane.normal[0]) > 0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u= (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v= (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)

                                elif abs(plane.normal[1]) > 0:
                                    #Estoy en Y, usamos X y Z para crear las uvs
                                    u= (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)

                                elif abs(plane.normal[2]) > 0:
                                    #Estoy en X, usamos Y y Z para crear las uvs
                                    u= (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v= (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None
        
        return Intercept(distance= t,
                         point= intersect.point,
                         normal= intersect.normal,
                         texcoords= (u, v),
                         obj= self)