def barycentricCoords(A, B, C, P):
    # Calcula áreas usando el Shoelace Theorem para obtener coordenadas baricéntricas

    def area(v0, v1, v2):
        return abs((v0[0] * v1[1] + v1[0] * v2[1] + v2[0] * v0[1]) -
                   (v0[1] * v1[0] + v1[1] * v2[0] + v2[1] * v0[0]))

    areaABC = area(A, B, C)
    if areaABC == 0:
        return None  # Triángulo degenerado

    areaPBC = area(P, B, C)
    areaPCA = area(P, C, A)
    areaPAB = area(P, A, B)

    u = areaPBC / areaABC
    v = areaPCA / areaABC
    w = areaPAB / areaABC

    # Valida que el punto esté dentro del triángulo
    if 0 <= u <= 1 and 0 <= v <= 1 and 0 <= w <= 1:
        return u, v, w
    else:
        return None