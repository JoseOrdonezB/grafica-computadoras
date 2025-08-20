from barycentric import barycentricCoords
from BMPTexture import BMPTexture

POINTS = 0
LINES = 1
TRIANGLES = 2

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = self.screen.get_rect()

        self.glColor(1, 1, 1)
        self.glClearColor(0, 0, 0)
        self.glClear()

        self.primitiveType = TRIANGLES
        self.models = []

        self.activeModelMatrix = None
        self.activeViewMatrix = None
        self.activeProjectionMatrix = None
        self.activeViewportMatrix = None
        self.activeVertexShader = None
        self.activeFragmentShader = None
        self.activeTexture = None

        self.background = None

        self.vpX = 0
        self.vpY = 0
        self.vpWidth = self.width
        self.vpHeight = self.height

        self.zBuffer = [[float('inf') for _ in range(self.height)] for _ in range(self.width)]

    def glLoadBackground(self, filename):
        self.background = BMPTexture(filename)

    def glClearColor(self, r, g, b):
        self.clearColor = [min(1, max(0, r)),
                           min(1, max(0, g)),
                           min(1, max(0, b))]

    def glClearBackground(self):
    # Limpia color + zbuffer
        self.glClear()

        if self.background is None:
            return

        eps = 1e-6
        w = max(1, self.vpWidth)
        h = max(1, self.vpHeight)

        for y in range(self.vpY, self.vpY + h):
        # Centro de píxel y eje V invertido (imagen tiene origen arriba)
            v = 1.0 - (((y - self.vpY) + 0.5) / h)
            if v >= 1.0: v = 1.0 - eps
            if v < 0.0:  v = 0.0

            for x in range(self.vpX, self.vpX + w):
                u = ((x - self.vpX) + 0.5) / w
                if u >= 1.0: u = 1.0 - eps
                if u < 0.0:  u = 0.0

                # Nota: usa el mismo nombre de método que tu clase BMPTexture
                texColor = self.background.get_color(u, v)   # o get_color(u, v) si ese es el tuyo
                if not texColor:
                    continue

                # aceptar 0..1 o 0..255
                r, g, b = texColor[:3]
                if r > 1 or g > 1 or b > 1:
                    R, G, B = int(r), int(g), int(b)
                else:
                    R, G, B = int(r*255), int(g*255), int(b*255)

            # clamp
                R = 0 if R < 0 else 255 if R > 255 else R
                G = 0 if G < 0 else 255 if G > 255 else G
                B = 0 if B < 0 else 255 if B > 255 else B

            # Escribir SIN prueba de profundidad
                self.screen.set_at((x, self.height - 1 - y), (R, G, B))
                self.frameBuffer[x][y] = [R, G, B]


    def glColor(self, r, g, b):
        self.currColor = [min(1, max(0, r)),
                          min(1, max(0, g)),
                          min(1, max(0, b))]
        
    def glViewport(self, x, y, width, height):
        self.vpX = int(x)
        self.vpY = int(y)
        self.vpWidth = max(1, int(width))
        self.vpHeight = max(1, int(height))

    def glClear(self):
        color = [int(i * 255) for i in self.clearColor]
        self.screen.fill(color)
        self.frameBuffer = [[color[:] for _ in range(self.height)] for _ in range(self.width)]
        self.zBuffer = [[float('inf') for _ in range(self.height)] for _ in range(self.width)]

    def glPoint(self, x, y, color=None, z=0):
        x = round(x)
        y = round(y)
        if 0 <= x < self.width and 0 <= y < self.height:
            if z < self.zBuffer[x][y]:
                self.zBuffer[x][y] = z
                color = [int(i * 255) for i in (color or self.currColor)]
                self.screen.set_at((x, self.height - 1 - y), color)
                self.frameBuffer[x][y] = color

    def glLine(self, p0, p1, color=None):
        x0, y0 = p0
        x1, y1 = p1

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        offset = 0
        limit = 0.5
        m = dy / dx if dx != 0 else 0
        y = y0

        for x in range(round(x0), round(x1) + 1):
            point = (y, x) if steep else (x, y)
            self.glPoint(*point, color or self.currColor)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glTriangleTextured(self, A, B, C, texture, time=0):
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                bCoords = barycentricCoords(A, B, C, (x, y))
                if bCoords is None:
                    continue
                u, v, w = bCoords

                zA, zB, zC = A[2], B[2], C[2]
                z = zA * u + zB * v + zC * w

                w_recip = (u / zA) + (v / zB) + (w / zC)
                if w_recip == 0:
                    continue

                tx = ((A[3] / zA) * u + (B[3] / zB) * v + (C[3] / zC) * w) / w_recip
                ty = ((A[4] / zA) * u + (B[4] / zB) * v + (C[4] / zC) * w) / w_recip

                nx = A[5] * u + B[5] * v + C[5] * w
                ny = A[6] * u + B[6] * v + C[6] * w
                nz = A[7] * u + B[7] * v + C[7] * w

                interpolatedVerts = [
                    [A[0], A[1], A[2], A[5], A[6], A[7]],
                    [B[0], B[1], B[2], B[5], B[6], B[7]],
                    [C[0], C[1], C[2], C[5], C[6], C[7]]
                ]

                if self.activeFragmentShader:
                    color = self.activeFragmentShader(
                        bar=(u, v, w),
                        verts=interpolatedVerts,
                        texCoords=(tx, ty),
                        texture=texture,
                        time=time
                    )
                elif texture:
                    color = texture.get_color(tx, ty)
                else:
                    color = self.currColor

                self.glPoint(x, y, color, z)

    def glRender(self, viewMatrix, projectionMatrix, viewportMatrix, time=0):
        self.activeViewMatrix = viewMatrix
        self.activeProjectionMatrix = projectionMatrix
        self.activeViewportMatrix = viewportMatrix

        for model in self.models:
            self.activeModelMatrix = model.GetModelMatrix()
            self.activeVertexShader = model.vertexShader
            self.activeFragmentShader = getattr(model, 'fragmentShader', None)
            self.activeTexture = getattr(model, 'texture', None)

            vertexBuffer = []

            for i in range(0, len(model.vertices), 3):
                x = model.vertices[i]
                y = model.vertices[i + 1]
                z = model.vertices[i + 2]

                if self.activeVertexShader:
                    x, y, z = self.activeVertexShader(
                        [x, y, z],
                        modelMatrix=self.activeModelMatrix,
                        viewMatrix=self.activeViewMatrix,
                        projectionMatrix=self.activeProjectionMatrix,
                        viewportMatrix=self.activeViewportMatrix,
                        time=time
                    )

                u = model.uvs[i // 3][0] if model.uvs else 0
                v = model.uvs[i // 3][1] if model.uvs else 0

                nx, ny, nz = model.normals[i // 3] if model.normals else [0, 0, 1]

                vertexBuffer.extend([x, y, z, u, v, nx, ny, nz])

            self.glDrawPrimitives(vertexBuffer, 8, model.colors, time)

    def glDrawPrimitives(self, buffer, vertexOffset, colors=None, time=0):
        if self.primitiveType == POINTS:
            for i in range(0, len(buffer), vertexOffset):
                x = buffer[i]
                y = buffer[i + 1]
                z = buffer[i + 2]
                self.glPoint(x, y, z=z)

        elif self.primitiveType == LINES:
            for i in range(0, len(buffer), vertexOffset * 3):
                for j in range(3):
                    x0 = buffer[i + vertexOffset * j]
                    y0 = buffer[i + vertexOffset * j + 1]
                    x1 = buffer[i + vertexOffset * ((j + 1) % 3)]
                    y1 = buffer[i + vertexOffset * ((j + 1) % 3) + 1]
                    self.glLine((x0, y0), (x1, y1))

        elif self.primitiveType == TRIANGLES:
            for i in range(0, len(buffer), vertexOffset * 3):
                A = buffer[i                     : i + vertexOffset]
                B = buffer[i + vertexOffset      : i + vertexOffset * 2]
                C = buffer[i + vertexOffset * 2  : i + vertexOffset * 3]

                if colors:
                    color_index = i // (vertexOffset * 3)
                    self.glColor(*colors[color_index])

                self.glTriangleTextured(A, B, C, self.activeTexture, time)