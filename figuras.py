from math import pi, atan2, acos, sqrt, cos, sin 
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

class OvalSphere(Sphere):
    def __init__(self, position, radius_x, radius_y, material):
        self.radius_x = radius_x
        self.radius_y = radius_y
        super().__init__(position, (radius_x + radius_y) / 2, material)
    
    def ray_intersect(self, orig, dir):
        L = ml.vector_subtraction(self.position, orig) 
        lengthL = ml.vector_normal(L)
        tca = ml.dot_product(L, dir)
        d = sqrt(lengthL ** 2 - tca ** 2)

        if d > max(self.radius_x, self.radius_y):
            return None
        
        thc_x = sqrt(self.radius_x ** 2 - d ** 2)
        thc_y = sqrt(self.radius_y ** 2 - d ** 2)

        t0_x = tca - thc_x
        t1_x = tca + thc_x
        t0_y = tca - thc_y
        t1_y = tca + thc_y

        # Encuentra la intersección más cercana en cada eje
        t0 = min(t0_x, t1_x, t0_y, t1_y)
        t1 = max(t0_x, t1_x, t0_y, t1_y)

        if t0 <= 0:
            t0 = t1
        if t0 < 0:
            return None
        
        P = ml.add_vector_scaled(orig, t0, dir)

        # Calcula la normal en función de las coordenadas de la esfera ovalada
        normal = [
            (P[0] - self.position[0]) / self.radius_x ** 2,
            (P[1] - self.position[1]) / self.radius_y ** 2,
            (P[2] - self.position[2]) / self.radius_x ** 2  # Puedes ajustar según la forma deseada
        ]

        normal_length = ml.vector_normal(normal)
        normal = [normal[i] / normal_length for i in range(3)]

        u = (atan2(normal[2], normal[0]) / (2*pi)) + 0.5
        v = acos(normal[1]) / pi

        return Intercept(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=(u, v),
                         obj=self)


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

class Cylinder(Sphere):
    def __init__(self, position, radius, height, material):
        super().__init__(position, radius, material)
        self.height = height
    
    def ray_intersect(self, orig, dir):
        # Calcula la intersección con el cilindro
        L = ml.vector_subtraction(orig, self.position)

        a = dir[0] ** 2 + dir[2] ** 2
        b = 2 * (L[0] * dir[0] + L[2] * dir[2])
        c = L[0] ** 2 + L[2] ** 2 - self.radius ** 2

        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            # No hay intersección con el cilindro
            return None

        # Encuentra las soluciones de la ecuación cuadrática
        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        # Verifica si las soluciones están dentro de la altura del cilindro
        y0 = orig[1] + t0 * dir[1]
        y1 = orig[1] + t1 * dir[1]

        if 0 <= y0 <= self.height or 0 <= y1 <= self.height:
            # Al menos una solución está dentro de la altura del cilindro
            t = min(t0, t1)
            intersection_point = ml.add_vector_scaled(orig, t, dir)

            # Ajusta la posición del punto de intersección considerando la posición inicial del cilindro
            intersection_point[1] = self.position[1] + t * dir[1]

            # Calcula la normal en la intersección
            normal = [intersection_point[0] - self.position[0], 
                      0, 
                      intersection_point[2] - self.position[2]]
            normal_length = ml.vector_normal(normal)
            normal = [normal[i] / normal_length for i in range(3)]

            u = (atan2(normal[2], normal[0]) / (2 * pi)) + 0.5
            v = intersection_point[1] / self.height

            return Intercept(distance=t,
                             point=intersection_point,
                             normal=normal,
                             texcoords=(u, v),
                             obj=self)
        else:
            # Ambas soluciones están fuera de la altura del cilindro
            return None


class Triangle(Shape):
    def __init__(self, vertices, material):
        self.vertices = vertices
        #super().__init__(position, material)
        v0 = ml.vector_subtraction(self.vertices[1], self.vertices[0])
        v1 = ml.vector_subtraction(self.vertices[2],self.vertices[0])
        self.normal = ml.normalize_vector(ml.cross_product(v0,v1))

        x = (vertices[0][0] + vertices[1][0]+vertices[2][0])/3
        y = (vertices[0][1] + vertices[1][1]+vertices[2][1])/3
        z = (vertices[0][2] + vertices[1][2]+vertices[2][2])/3

        super().__init__((x,y,z), material)

    def ray_intersect(self, orig, dir):
        denom = ml.dot_product(dir, self.normal)
                
        if abs(denom)<=0.0001:
            return None
        
        d = -1 * ml.dot_product(self.normal, self.vertices[0])
        num = -1 * (ml.dot_product(self.normal, orig) + d)

        t = num/denom 

        if t < 0:
            return None
        
        P = ml.vector_addition(orig, ml.multiply_scalar_array(t,dir))

        #edge 0
        edge0 = ml.vector_subtraction(self.vertices[1],self.vertices[0]) #v1 - v0; 
        vp0 = ml.vector_subtraction(P,self.vertices[0]) #Vec3f vp0 = P - v0;
        C = ml.cross_product(edge0,vp0)
        
        if ml.dot_product(self.normal,C)<0: 
            return None
        
        #edge 1
        edge1 = ml.vector_subtraction(self.vertices[2], self.vertices[1])    #Vec3f edge1 = v2 - v1; 
        vp1 = ml.vector_subtraction(P, self.vertices[1])    #Vec3f vp1 = P - v1;
        C = ml.cross_product(edge1,vp1);
        
        if ml.dot_product(self.normal, C) < 0:    
            return None
    
        #edge 2
        edge2 = ml.vector_subtraction(self.vertices[0],self.vertices[2]) #v0 - v2; 
        vp2 = ml.vector_subtraction(P,self.vertices[2]) #Vec3f vp2 = P - v2;
        C = ml.cross_product(edge2,vp2);
        
        if ml.dot_product(self.normal, C) < 0:   
            return None 
        
        u,v,w = ml.barycentricCoords(self.vertices[0], self.vertices[1], self.vertices[2], P)

        
        return Intercept(distance=t,
                         point=P,
                         normal=self.normal,
                         texcoords=(u,v),
                         obj=self)  