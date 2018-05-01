import time
import pygame

MARK_POSITION = 5
VISITED = 20

ENVIROMENT_SIZE = 42
LIMIT_INDEX_MATRIX = ENVIROMENT_SIZE-1

BLACK = (0, 0, 0)
GREEN = (93, 191, 0)
DARK_GREEN = (43, 100, 0)
RED = (255, 63, 0)
DARK_RED = (200, 0, 0)
BLUE = (48, 157, 229)
DARK_BLUE = (0, 80, 120)
BROWN = (120, 79, 49)
DARK_BROWN = (70, 29, 0)
GRAY = (30, 30, 30)
WHITE = (255, 255, 255)

CELL_SIZE = 15
MARGIN_CELL = 0.1

ENVIROMENT_SIZE = 42
LIMIT_INDEX_MATRIX = ENVIROMENT_SIZE-1
SCREEN_MARGIN = 2
SCREEN_SIZE = (CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN, CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN)

# grid = []
screen = pygame.display.set_mode(SCREEN_SIZE)

FLOOR = 0
EXPANDED_FLOOR = 10

MOUNTAIN = 1
EXPANDED_MOUNTAIN = 11

WATER = 2
EXPANDED_WATER = 12

FIRE = 3
EXPANDED_FIRE = 13

VISITED = 20
MARK_POSITION = 5

border_bfs = []
visited_bfs = []

class Node:
	row = -1
	col = -1
	precedent = -1
	cost = -1

	def __init__(self, row, col, precedent, cost):
		self.row = row
		self.col = col
		self.precedent = precedent
		self.cost = cost

	def __str__(self):
		if (self.precedent != -1):
			return "Node: (%d, %d) old: (%d, %d) | %d" % (self.row, self.col,
				self.precedent.row, self.precedent.col, self.cost)
		return "Node: (%d, %d) | old: RAIZ" % (self.row, self.col)


class Robot:
	node = Node(-1, -1, -1, -1)
	way = []

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Adventurous Robot")

	def move_dfs(self, grid):
		if (self.can_move('up', self.node, grid) and self.is_not_expanded(grid, self.node.row-1, self.node.col, None)):
			self.node.row -= 1
		elif (self.can_move('right', self.node, grid) and self.is_not_expanded(grid, self.node.row, self.node.col+1, None)):
			self.node.col += 1
		elif (self.can_move('down', self.node, grid) and self.is_not_expanded(grid, self.node.row+1, self.node.col, None)):
			self.node.row += 1
		elif (self.can_move('left', self.node, grid) and self.is_not_expanded(grid, self.node.row, self.node.col-1, None)):
			self.node.col -= 1

		self.apply_expand_function_in_grid(self.node.row, self.node.col, grid)
		self.way.append((self.node.row, self.node.col))

		self.draw(screen, grid)
		pygame.display.flip()
		# time.sleep(1)

		if (self.is_in_mark_position(grid, self.node)):
			while (True):
				print ("I got the way")

		self.move_dfs(grid)

	def move_bfs(self, root_row, root_col, grid):
		# global border_bfs
		global visited_bfs
		to_visit_bfs = []
		root = Node(root_row, root_col, -1, 1)

		# visited_bfs.append(root)
		to_visit_bfs.append(root)

		while(to_visit_bfs):
			node = to_visit_bfs.pop(0)
			visited_bfs.append(node)
			border_bfs = self.expand(node, grid)

			for b_node in border_bfs:
				if (self.is_in_mark_position(grid, b_node)):				
					to_visit_bfs = []
					self.get_the_way(visited_bfs, root, b_node)
					while(True):
						print ("I got the way")
				elif (self.is_not_expanded(grid, b_node.row, b_node.col, None) and self.is_not_in_to_visited(b_node, to_visit_bfs)):
					print (b_node)
					self.apply_expand_function_in_grid(node.row, node.col, grid)
					to_visit_bfs.append(b_node)
				
				self.draw(screen, grid)
				pygame.display.flip()



	def expand(self, node, grid):
		row, col = node.row, node.col
		cost = 1

		border_bfs = []

		future_node = Node(row-1, col, node, cost)
		if (self.can_move('up', node, grid)):
			border_bfs.append(future_node)

		future_node = Node(row, col+1, node, cost)
		if (self.can_move('right', node, grid)):
			border_bfs.append(future_node)
		
		future_node = Node(row+1, col, node, cost)
		if (self.can_move('down', node, grid)):
			border_bfs.append(future_node)
		
		future_node = Node(row, col-1, node, cost)
		if (self.can_move('left', node, grid)):
			border_bfs.append(future_node)

		return border_bfs

	def is_in_mark_position(self, grid, node):
		return (grid[node.row][node.col] == MARK_POSITION)

	def can_move(self, direction, node, grid):
		return (direction == 'up' and node.row > 0
				or direction == 'right' and node.col < LIMIT_INDEX_MATRIX
				or direction == 'down' and node.row < LIMIT_INDEX_MATRIX
				or direction == 'left' and node.col > 0)

	def is_not_expanded(self, grid, last_row, last_col, node):
		global visited_bfs

		if (node == None):
			return (grid[last_row][last_col] < 10)
		return (node not in visited_bfs or grid[last_row][last_col] < 10)

	def is_not_in_to_visited(self, node, to_visit_bfs):
		global visited_bfs

		for aux in to_visit_bfs:
			if (aux.row == node.row and aux.col == node.col):
				return False

		return True

	def apply_expand_function_in_grid(self, row, col, grid):
		if (grid[row][col] != MARK_POSITION):
			grid[row][col] += 10

	def get_the_way(self, visited_nodes, root, final_node):
		aux = final_node

		temp_way = []

		while(aux != -1):
			print ("aux: ", aux)
			temp_way.append(aux)
			aux = aux.precedent

		way = list(reversed(temp_way))

		for node in way:
			print ("FINAL WAY: ", node)

	def draw(self, screen, grid):
		x, y = 0, 0
		for row in grid:
			for col in row:
				if col == FLOOR:
					pygame.draw.rect(screen, GREEN, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == MOUNTAIN:
					pygame.draw.rect(screen, BROWN, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == WATER:
					pygame.draw.rect(screen, BLUE, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == FIRE:
					pygame.draw.rect(screen, RED, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				# elif col == ROBOT:
				# 	pygame.draw.rect(screen, BLACK, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == MARK_POSITION:
					pygame.draw.rect(screen, WHITE, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == VISITED:
					pygame.draw.rect(screen, GRAY, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				if col == EXPANDED_FLOOR:
					pygame.draw.rect(screen, DARK_GREEN, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == EXPANDED_MOUNTAIN:
					pygame.draw.rect(screen, DARK_BROWN, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == EXPANDED_WATER:
					pygame.draw.rect(screen, DARK_BLUE, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				elif col == EXPANDED_FIRE:
					pygame.draw.rect(screen, DARK_RED, [x, y, CELL_SIZE - MARGIN_CELL, CELL_SIZE - MARGIN_CELL], 0)
				x = x + CELL_SIZE
			y = y + CELL_SIZE
			x = 0	