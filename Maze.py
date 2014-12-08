import random
import turtle

class Maze(object):
	"""docstring for Maze"""

	class Cell(object):
		"""docstring for Cell"""
		def __init__(self):
			self.edges = []
			self.visited = False

		def link(self, neighbor):
			newedge = Maze.Edge(self, neighbor)
			self.edges.append(newedge)
			neighbor.edges.append(newedge)

		def unvisitedEdges(self):
			new_edges = []
			for edge in self.edges:
				if not (edge.follow(self).visited):
					new_edges.append(edge)
			return new_edges

	class Edge(object):
		"""docstring for edge"""
		def __init__(self, vert1, vert2):
			self.walled = True
			self.v1 = vert1
			self.v2 = vert2

		def follow(self, vert):
			if vert == self.v1:
				return self.v2
			if vert == self.v2:
				return self.v1
			return None
			
			
	def __init__(self, size):
		self.size = size
		self.cells = []
		self.populate()
		self.start = None
		self.end = None

	def populate(self):
		for x in range(self.size):
			for y in range(self.size):
				index = x * self.size + y
				self.cells.append(Maze.Cell())
				if x != 0:
					self.cells[index].link(self.cells[index - self.size])
				if y != 0:
					self.cells[index].link(self.cells[index - 1])

	def numberofcells(self):
		return len(self.cells)

	def hasUnvisited(self):
		for cell in self.cells:
			if cell.visited == False:
				return True
		return False

def construct(maze):
	path = []
	current_cell = maze.cells[0]
	current_cell.visited = True
	maze.start = current_cell
	longest_path = 0
	end_cell = None
	while maze.hasUnvisited():
		walled_paths = current_cell.unvisitedEdges()
		if len(walled_paths) != 0:
			next_corridor = random.choice(walled_paths)
			path.append(current_cell)
			next_corridor.walled = False
			current_cell = next_corridor.follow(current_cell)
			current_cell.visited = True
		elif len(path) != 0:
			if len(path) > longest_path:
				longest_path = len(path)
				end_cell = current_cell
			current_cell = path.pop()
	if len(path) > longest_path:
		print("fixed")
		longest_path = len(path)
		end_cell = current_cell
	maze.end = end_cell

def displayMaze(maze, xstart, ystart, length):
	turtle.up()
	def vertical(col):
		turtle.goto(xstart + length * (col + 1), ystart)
		turtle.seth(-90)
		for x in range(0, maze.size):
			if x == maze.size - 1:
				status = maze.cells[x * maze.size + col].edges[-1].walled
			else:
				status = maze.cells[x * maze.size + col].edges[-2].walled
			if status:
				turtle.down()
			else:
				turtle.up()
			turtle.forward(length)
		turtle.up()
	def horizontal(row):
		turtle.goto(xstart, ystart - length * (row + 1))
		turtle.seth(0)
		for x in range(0, maze.size):
			status = maze.cells[row * maze.size + x].edges[-1].walled
			if status:
				turtle.down()
			else:
				turtle.up()
			turtle.forward(length)
		turtle.up()
	def drawExit(row, col):
		turtle.goto(xstart + col * length, ystart - row * length)
		turtle.down()
		turtle.begin_fill()
		for x in range(0, 4):
			turtle.forward(length)
			turtle.right(90)
		turtle.end_fill()
		turtle.up()
	for row in range(maze.size):
		for col in range(maze.size):
			if maze.cells[row * maze.size + col] == maze.end:
				turtle.color("white", "red")
				drawExit(row, col)
				turtle.color("black")
			if maze.cells[row * maze.size + col] == maze.start:
				turtle.color("white", "green")
				drawExit(row, col)
				turtle.color("black")
	turtle.goto(xstart, ystart)
	turtle.seth(0)
	turtle.down()
	for x in range(0, 4):
		turtle.forward(length * maze.size)
		turtle.right(90)
	turtle.up()
	for i in range(0, maze.size - 1):
		vertical(i)
	for j in range(0, maze.size - 1):
		horizontal(j)
	
		
	turtle.up()
	turtle.goto(xstart, ystart)
	



testmaze = Maze(10)
construct(testmaze)
testlen = 10
turtle.speed(0)
displayMaze(testmaze, testmaze.size * testlen / -2, testmaze.size * testlen / 2, testlen)
turtle.done()
		