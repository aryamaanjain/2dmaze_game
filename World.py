"""
	Method from youtube video series by The Coding Train:
	https://www.youtube.com/watch?v=HyK_Q5rrcr4&t=1s
	which was taken from wikipedia:
	https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import randint
from math import floor


class World:
	"""docstring for World"""


	def __init__(self, rows, cols, w):
		self.rows = rows  # number of cells along rows
		self.cols = cols  # number of cells along column
		self.w = w  # width and height of each cell
		self.grid = []  # to hold all the cells

		for i in range(rows):
			for j in range(cols):
				self.grid.append(Cell(i, j))

		stack = []
		current = self.grid[0]
		current.visited = True
		neighbour = current.checkNeighbour(self)  # contains unvisited neighbours

		while neighbour is not None or len(stack) > 0:
			if neighbour is not None:
				neighbour.visited = True
				stack.append(current)
				self.removeWall(current, neighbour)
				current = neighbour
			elif len(stack) > 0:
				current = stack.pop()

			neighbour = current.checkNeighbour(self)


	def display(self):
		# walls
		for cell in self.grid:
			cell.display(self.w)


	def removeWall(self, c, n):
		"""removes wall between 2 given cells, current and neighbour"""
		dr =  c.i - n.i  # difference of rows
		if dr > 0:  # then current is above neighbour
			c.walls[0] = False  # remove bottom wall of current
			n.walls[2] = False  # remove top wall of neighbour
		elif dr < 0:
			c.walls[2] = False
			n.walls[0] = False

		dc = c.j - n.j 
		if dc > 0:  # then current is right of neighbour
			c.walls[3] = False
			n.walls[1] = False
		elif dc < 0:
			c.walls[1] = False
			n.walls[3] = False


	def index(self, i, j):
		"""returns location in 1D array given 2D points"""
		if i < 0 or j < 0 or i > self.rows-1 or j > self.cols-1:  # out of grid
			return None
		else:
			return i * self.cols + j


	def shadow(self, p):
		"""prevents light from going through walls"""
		prow = floor(p.y / self.w)
		pcol = floor(p.x / self.w)

		pindex = self.index(prow, pcol)
		pcur = self.grid[pindex]

		# immidiate neighbours
		if self.index(prow-1, pcol) is not None:
			pbot = self.grid[self.index(prow-1, pcol  )]  # bottom
		else:
			pbot = None
		if self.index(prow  , pcol+1) is not None:
			prig = self.grid[self.index(prow  , pcol+1)]
		else:
			prig = None
		if self.index(prow+1, pcol  ) is not None:
			ptop = self.grid[self.index(prow+1, pcol  )]
		else:
			ptop = None
		if self.index(prow  , pcol-1) is not None:
			plef = self.grid[self.index(prow  , pcol-1)]
		else:
			plef = None

		# diagonal neighbours
		if self.index(prow+1, pcol+1) is not None:
			ptr = self.grid[self.index(prow+1, pcol+1)]
		else:
			ptr = None
		if self.index(prow-1, pcol+1) is not None:
			pbr = self.grid[self.index(prow-1, pcol+1)]
		else:
			pbr = None
		if self.index(prow-1, pcol-1) is not None:
			pbl = self.grid[self.index(prow-1, pcol-1)]
		else:
			pbl = None
		if self.index(prow+1, pcol-1) is not None:
			ptl = self.grid[self.index(prow+1, pcol-1)]
		else:
			ptl = None

		for i in self.grid:
			# same cell
			condition = (i == pcur)
			# immidiate neighbours
			condition = condition or (i == pbot and pcur.walls[0] == False)  # bottom cell
			condition = condition or (i == prig and pcur.walls[1] == False)  # right cell
			condition = condition or (i == ptop and pcur.walls[2] == False)  # top cell
			condition = condition or (i == plef and pcur.walls[3] == False)  # left cell
			# diagonal neighbours
			# top right
			condition1 = (i == ptr)
			if ptop is not None:
				condition2 = ptop.walls[0] == False and ptop.walls[1] == False
			else:
				condition2 = False
			if prig is not None:
				condition3 = prig.walls[3] == False and prig.walls[2] == False
			else:
				condition3 = False
			condition  = condition or (condition1 and (condition2 or condition3))

			# bottom right
			condition1 = (i == pbr)
			if pbot is not None:
				condition2 = pbot.walls[2] == False and pbot.walls[1] == False
			else:
				condition2 = False
			if prig is not None:
				condition3 = prig.walls[3] == False and prig.walls[0] == False
			else:
				condition3 = False
			condition  = condition or (condition1 and (condition2 or condition3))

			# bottom left
			condition1 = (i == pbl)
			if pbot is not None:
				condition2 = pbot.walls[2] == False and pbot.walls[3] == False
			else:
				condition2 = False
			if plef is not None:
				condition3 = plef.walls[1] == False and plef.walls[0] == False
			else:
				condition3 = False
			condition  = condition or (condition1 and (condition2 or condition3))

			# top left
			condition1 = (i == ptl)
			if ptop is not None:
				condition2 = ptop.walls[0] == False and ptop.walls[3] == False
			else:
				condition2 = False
			if plef is not None:
				condition3 = plef.walls[1] == False and plef.walls[2] == False
			else:
				condition3 = False
			condition  = condition or (condition1 and (condition2 or condition3))

			if not condition:
				i.putshadow(self.w)


class Cell:
	"""docstring for Cell"""


	def __init__(self, i, j):
		self.i = i  # row number
		self.j = j  # col number
		self.walls = [True, True, True, True]  # whether walls exist in order bottom, right, top, left
		self.visited = False


	def checkNeighbour(self, w):
		"""takes in world w and checks whether neighbours visited"""
		neighbours = []  # will contain neighbours not visited
		i = self.i
		j = self.j

		if w.index(i-1, j) is not None:
			bottom = w.grid[w.index(i-1, j)]
			if not bottom.visited:
				neighbours.append(bottom)

		if w.index(i, j+1) is not None:
			right = w.grid[w.index(i, j+1)]
			if not right.visited:
				neighbours.append(right)

		if w.index(i+1, j) is not None:
			top = w.grid[w.index(i+1, j)]
			if not top.visited:
				neighbours.append(top)

		if w.index(i, j-1) is not None:
			left = w.grid[w.index(i, j-1)]
			if not left.visited:
				neighbours.append(left)

		if len(neighbours) > 0:
			return neighbours[randint(0, len(neighbours)-1)]
		else:
			return None


	def display(self, w):
		"""takes in width and displays cell"""		
		r = self.i * w
		c = self.j * w

		# glColor3f(0.2, 0.2, 0.2)
		
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.2, 0.2, 0.2, 1.0)
		mspecular = (0.2, 0.2, 0.2, 1.0)
		mshininess = 10.0

		glMaterialfv(GL_FRONT, GL_AMBIENT, mambient)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mdiffuse)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mspecular)
		glMaterialfv(GL_FRONT, GL_SHININESS, mshininess)

		gap = 0.001  # to remove overlap of walls for proper lighting
		glBegin(GL_QUADS)
		if self.walls[0]:  # bottom wall
			glNormal3f(0.0, 1.0, 0.0)
			r += gap
			glVertex3f(c  , r  , -0.01)
			glVertex3f(c  , r  , w)
			glVertex3f(c+w, r  , w)
			glVertex3f(c+w, r  , -0.01)
			r -= gap
		if self.walls[1]:  # right wall
			glNormal3f(-1.0, 0.0, 0.0)
			c -= gap
			glVertex3f(c+w, r  , -0.01)
			glVertex3f(c+w, r  , w)
			glVertex3f(c+w, r+w, w)
			glVertex3f(c+w, r+w, -0.01)
			c += gap
		if self.walls[2]:  # top wall
			glNormal3f(0.0, -1.0, 0.0)
			glVertex3f(c+w, r+w, -0.01)
			glVertex3f(c+w, r+w, w)
			glVertex3f(c  , r+w, w)
			glVertex3f(c  , r+w, -0.01)
		if self.walls[3]:  # left wall
			glNormal3f(1.0, 0.0, 0.0)
			glVertex3f(c  , r+w, -0.01)
			glVertex3f(c  , r+w, w)
			glVertex3f(c  , r  , w)
			glVertex3f(c  , r  , -0.01)
		glEnd()
		
		# floor
		# glColor3f(0.5, 0.5, 0.5)
		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.5, 0.5, 0.5, 1.0)
		mspecular = (0.2, 0.2, 0.2, 1.0)
		mshininess = 10.0

		glMaterialfv(GL_FRONT, GL_AMBIENT, mambient)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mdiffuse)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mspecular)
		glMaterialfv(GL_FRONT, GL_SHININESS, mshininess)

		glBegin(GL_QUADS)  # do tessellation for better lighting
		glNormal3f(0.0, 0.0, 1.0)
		glVertex3f(c  , r  , -0.01)
		glVertex3f(c+w, r  , -0.01)
		glVertex3f(c+w, r+w, -0.01)
		glVertex3f(c  , r+w, -0.01)
		glEnd()
		# glColor3f(1.0, 1.0, 1.0)


	def putshadow(self, w):
		"""puts black roof on top of cell to give appearance of shadow"""
		r = self.i * w
		c = self.j * w

		mambient  = (0.0, 0.0, 0.0, 1.0)
		mdiffuse  = (0.0, 0.0, 0.0, 1.0)
		mspecular = (0.0, 0.0, 0.0, 1.0)
		mshininess = 0.0

		glMaterialfv(GL_FRONT, GL_AMBIENT, mambient)
		glMaterialfv(GL_FRONT, GL_DIFFUSE, mdiffuse)
		glMaterialfv(GL_FRONT, GL_SPECULAR, mspecular)
		glMaterialfv(GL_FRONT, GL_SHININESS, mshininess)

		glBegin(GL_QUADS)  # do tessellation for better lighting
		glNormal3f(0.0, 0.0, -1.0)
		glVertex3f(c  , r  , w)
		glVertex3f(c+w, r  , w)
		glVertex3f(c+w, r+w, w)
		glVertex3f(c  , r+w, w)
		glEnd()