POINTS = 0
LINES = 1
TRIANGLES = 2

class Renderer(object):
	def __init__(self, screen):
		self.screen = screen
		_, _, self.width, self.height = self.screen.get_rect()

		self.glColor(1,1,1)
		self.glClearColor(0,0,0)

		self.glClear()

		self.primitiveType = TRIANGLES

		self.models = []

		self.activeModelMatrix = None
		self.activeVertexShader = None


	def glClearColor(self, r, g, b):
		r = min(1, max(0,r))
		g = min(1, max(0,g))
		b = min(1, max(0,b))
		self.clearColor = [r,g,b]


	def glColor(self, r, g, b):
		r = min(1, max(0,r))
		g = min(1, max(0,g))
		b = min(1, max(0,b))
		self.currColor = [r,g,b]

	def glClear(self):
		color = [int(i * 255) for i in self.clearColor]
		self.screen.fill(color)
		self.frameBuffer = [[color for y in range(self.height)]
							for x in range(self.width)]


	def glPoint(self, x, y, color = None):
		x = round(x)
		y = round(y)
		if (0 <= x < self.width) and (0 <= y < self.height):
			color = [int(i * 255) for i in (color or self.currColor) ]
			self.screen.set_at((x,self.height - 1 - y ), color)
			self.frameBuffer[x][y] = color


	def glLine(self, p0, p1, color = None):
		x0 = p0[0]
		x1 = p1[0]
		y0 = p0[1]
		y1 = p1[1]

		if x0 == x1 and y0 == y1:
			self.glPoint(x0, y0)
			return

		dy = abs(y1 - y0)
		dx = abs(x1 - x0)
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
				y += 1 if y0 < y1 else -1
				limit += 1


	def glTriangle(self, A, B, C):
		if A[1] < B[1]: A, B = B, A
		if A[1] < C[1]: A, C = C, A
		if B[1] < C[1]: B, C = C, B

		def flatBottom(vA, vB, vC):
			try:
				mBA = (vB[0] - vA[0]) / (vB[1] - vA[1])
				mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
			except:
				return
			if vB[0] > vC[0]:
				vB, vC = vC, vB
				mBA, mCA = mCA, mBA
			x0 = vB[0]
			x1 = vC[0]
			for y in range(round(vB[1]), round(vA[1] + 1)):
				for x in range(round(x0), round(x1 + 1)):
					self.glPoint(x,y)
				x0 += mBA
				x1 += mCA

		def flatTop(vA, vB, vC):
			try:
				mCA = (vC[0] - vA[0]) / (vC[1] - vA[1])
				mCB = (vC[0] - vB[0]) / (vC[1] - vB[1])
			except:
				return
			if vA[0] > vB[0]:
				vA, vB = vB, vA
				mCA, mCB = mCB, mCA
			x0 = vA[0]
			x1 = vB[0]
			for y in range(round(vA[1]), round(vC[1] - 1), -1):
				for x in range(round(x0), round(x1 + 1)):
					self.glPoint(x,y)
				x0 -= mCA
				x1 -= mCB

		if B[1] == C[1]:
			flatBottom(A,B,C)
		elif A[1] == B[1]:
			flatTop(A,B,C)
		else:
			D = [ A[0] + ((B[1] - A[1]) / (C[1] - A[1])) * (C[0] - A[0]), B[1] ]
			flatBottom(A, B, D)
			flatTop(B, D, C)


	def glRender(self):
		for model in self.models:
			self.activeModelMatrix = model.GetModelMatrix()
			self.activeVertexShader = model.vertexShader

			vertexBuffer = []
			for i in range(0, len(model.vertices), 3):
				x = model.vertices[i]
				y = model.vertices[i + 1]
				z = model.vertices[i + 2]

				if self.activeVertexShader:
					x, y, z = self.activeVertexShader([x,y,z],
													  modelMatrix = self.activeModelMatrix)

				vertexBuffer.append(x)
				vertexBuffer.append(y)
				vertexBuffer.append(z)

			self.glDrawPrimitives(vertexBuffer, 3, model.colors)


	def glDrawPrimitives(self, buffer, vertexOffset, colors=None):
		if self.primitiveType == POINTS:
			for i in range(0, len(buffer), vertexOffset):
				x = buffer[i]
				y = buffer[i + 1]
				self.glPoint(x,y)

		elif self.primitiveType == LINES:
			for i in range(0, len(buffer), vertexOffset * 3):
				for j in range(3):
					x0 = buffer[i + vertexOffset * j + 0]
					y0 = buffer[i + vertexOffset * j + 1]
					x1 = buffer[i + vertexOffset * ((j + 1) % 3) + 0]
					y1 = buffer[i + vertexOffset * ((j + 1) % 3) + 1]
					self.glLine((x0,y0), (x1,y1))

		elif self.primitiveType == TRIANGLES:
			for i in range(0, len(buffer), vertexOffset * 3):
				A = [ buffer[i + j + vertexOffset * 0] for j in range(vertexOffset) ]
				B = [ buffer[i + j + vertexOffset * 1] for j in range(vertexOffset) ]
				C = [ buffer[i + j + vertexOffset * 2] for j in range(vertexOffset) ]

				if colors:
					color_index = i // (vertexOffset * 3)
					self.glColor(*colors[color_index])

				self.glTriangle(A,B,C)