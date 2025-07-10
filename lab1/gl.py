class Renderer:
    def __init__ (self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)

        self.glClear()

    # se define el color de fondo.
    def glClearColor(self, r, g, b):
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.clearColor = [r, g, b]

    # función para definir el color actual.
    def glColor(self, r, g, b): 
        r = min(1, max(0, r))
        g = min(1, max(0, g))
        b = min(1, max(0, b))

        self.currColor = [r, g, b]

    # se llena el frame buffer con el color de fondo.
    def glClear(self):
        color = [int(i*255) for i in self.clearColor]
        self.screen.fill(color)

        self.frameBuffer = [[self.clearColor for i in range(self.height)]
                         for x in range(self.width)] 

    # función para dibujar un punto en pantalla.
    def glPoint(self, x, y, color = None):
        x = round(x)
        y = round(y)

        if (0 <= x < self.width) and (0 <= y < self.height):
            color = [int(i*255) for i in (color or self.currColor)]
            self.screen.set_at((x, self.height - 1 - y), color)

            self.frameBuffer[x][y] = color

    # función para dibujar líneas con el algoritmo de Bresenham.
    def glLine(self, p0, p1, color = None):
        x0 = p0[0]
        x1 = p1[0]
        y0 = p0[1]
        y1 = p1[1]

        if (x0 == x1 and y0 == y1):
            self.glPoint(x0, y0, color)
            return
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        limit = 0.75
        m = dy / dx
        y = y0

        for x in range(round(x0), round(x1) + 1):
            if steep:
                self.glPoint(y, x, color or self.currColor)
            else:
                self.glPoint(x, y, color or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                
                limit += 1

    # función para dibujar polígonos.
    def glPolygon(self, points, color = None):
        # se define la cantidad de puentos que hay en el polígono.
        n = len(points)

        # si hay menos de tres puntos, solo se dibuja una línea.
        if n < 3:
            self.glLine(points[0], points[1], color or self.currColor)

        # se recorre una lista de puntos y se dibujan las líneas para formar el polígono.
        # se usa el operador módulo para conectar el último punto con el primero.
        for i in range(n):
            p0 = points[i]
            p1 = points[(i + 1) % n]
            self.glLine(p0, p1, color or self.currColor)

    # función para rellenar polígonos.
    # algoritmo de scanline filling.
    # pequeña explicación: se dibuja una linea horizontal en cada valor de y del polígono, donde se intersecta con los bordes se dibujan puntos para llenar la figura.
    def glFillPolygon(self, points, color = None):
        color = color or self.currColor

        # se define la cantidad de puntos que hay en el polígono.
        n = len(points)

        # si hay menos de tres puntos no se rellena nada ya que no hay polígono.
        if n < 3:
            return
        
        # se obtienen los valores mínimos y máximos de y.
        y_min = min(p[1] for p in points)
        y_max = max(p[1] for p in points)
        
        # se reccore un ciclo desde el minimo de y hasta el máximo de y.
        for y in range(y_min, y_max + 1):
            # se crea una lista para guardar los valores en los que se intersecta la línea horizontal.
            intersections = []

            # se recorre cada punto del polígono y se calcula la intersección con la línea horizontal.
            for i in range(n):
                (x0, y0) = points[i]
                (x1, y1) = points[(i + 1) % n]

                # si los puntos son iguales, no se hace nada.
                if y0 == y1:
                    continue

                # si la línea horizontal intersecta con el borde del polígono, se calcula el valor de x.
                if (y >= min(y0, y1) and (y < max(y0, y1))):
                    x = int(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
                    intersections.append(x)

            intersections.sort()

            # se recorre la lista de las intersecciones.
            for i in range(0, len(intersections), 2):
                # mientras hayan pares de intersecciones, se dibujan puntos entre la x inicial y x final del par.
                if i + 1 < len(intersections):
                    x_start = intersections[i]
                    x_end = intersections[i + 1]
                    for x in range(x_start, x_end + 1):
                        self.glPoint(x, y, color)



