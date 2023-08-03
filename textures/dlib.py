class libreria:
    def multi4x4matrix(matrix1, matrix2):
            resultado = [
                [0.0,0.0,0.0,0.0],
                [0.0,0.0,0.0,0.0],
                [0.0,0.0,0.0,0.0],
                [0.0,0.0,0.0,0.0]]
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        resultado[i][j] += matrix1[i][k] * matrix2[k][j]
            return resultado
    
    def multimatrixvec(matrix, vect):
        resultado = [0.0, 0.0, 0.0, 0.0]

        for i in range(4):
            for j in range(4):
                resultado[i] += matrix[i][j] * vect[j]

        return resultado
    
    def barycentricCoords(A,B,C, P):

        areaPBC = (B[1] -C[1]) * (P[0]-C[0]) + (C[0]-B[0]) * (P[1]-C[1])

        areaACP = (C[1] -A[1]) * (P[0]-C[0]) + (A[0]-C[0]) * (P[1]-C[1])

        areaABC = (B[1] -C[1]) * (A[0]-C[0]) + (C[0]-B[0]) * (A[1]-C[1])
        
        if areaABC == 0:
            return None

        u = areaPBC / areaABC
        v = areaACP / areaABC
        w = 1 - u -v

        return u, v, w 
