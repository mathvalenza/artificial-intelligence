import time
import pygame
import constants
import numpy as np

screen = pygame.display.set_mode(constants.SCREEN_SIZE)

steps = 0

class Node:
	row = -1
	col = -1
	precedent = -1
	cost = -1
	cost_a_star = -1

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
		global steps
		steps += 1 

		self.apply_expand_function_in_grid(self.node.row, self.node.col, grid)
		self.way.append((self.node.row, self.node.col))

		if (self.can_move('up', self.node, grid) and self.is_not_expanded(grid, self.node.row-1, self.node.col)):
			self.node.row -= 1
		elif (self.can_move('right', self.node, grid) and self.is_not_expanded(grid, self.node.row, self.node.col+1)):
			self.node.col += 1
		elif (self.can_move('down', self.node, grid) and self.is_not_expanded(grid, self.node.row+1, self.node.col)):
			self.node.row += 1
		elif (self.can_move('left', self.node, grid) and self.is_not_expanded(grid, self.node.row, self.node.col-1)):
			self.node.col -= 1

		self.draw(screen, grid)
		pygame.display.flip()

		if (self.is_in_mark_position(grid, self.node)):
			while (True):
				print ("I've got the way in %d steps" % steps)

		self.move_dfs(grid)

	def move_bfs(self, root_row, root_col, grid):
		global steps
		visited_bfs = []
		to_visit_bfs = []
		root = Node(root_row, root_col, -1, 1)
		cost = 1

		to_visit_bfs.append(root)

		while(to_visit_bfs):
			steps += 1 
			node = to_visit_bfs.pop(0)
			visited_bfs.append(node)
			border_bfs = self.expand(node, cost, grid)

			for b_node in border_bfs:
				if (self.is_in_mark_position(grid, b_node)):				
					to_visit_bfs = []
					self.get_the_way(visited_bfs, root, b_node, grid)
					break
				elif (self.is_not_expanded(grid, b_node.row, b_node.col) and self.is_not_in_to_visit(b_node, to_visit_bfs)):
					print (b_node)
					self.apply_expand_function_in_grid(node.row, node.col, grid)
					to_visit_bfs.append(b_node)
				
				self.draw(screen, grid)
				pygame.display.flip()


		while(True):
			self.draw(screen, grid)
			pygame.display.flip()
			time.sleep(2)
			print ("I've got the way in %d steps" % steps)

	def move_uniform_cost(self, root_row, root_col, grid):
		global steps
		visited_uniform_cost = []
		to_visit_uniform_cost = []
		root = Node(root_row, root_col, -1, self.get_cost(root_row, root_col, grid))

		to_visit_uniform_cost.append(root)

		while(to_visit_uniform_cost):
			steps += 1
			node = to_visit_uniform_cost.pop(0)
			visited_uniform_cost.append(node)
			border_uniform_cost = self.expand(node, node.cost, grid)

			for b_node in border_uniform_cost:
				if (self.is_in_mark_position(grid, b_node)):				
					to_visit_uniform_cost = []
					self.get_the_way(visited_uniform_cost, root, b_node, grid)
					break
				elif (self.is_not_expanded(grid, b_node.row, b_node.col) and self.is_not_in_to_visit(b_node, to_visit_uniform_cost)):
					print (b_node)
					self.apply_expand_function_in_grid(node.row, node.col, grid)
					to_visit_uniform_cost.append(b_node)
					to_visit_uniform_cost.sort(key=lambda x: x.cost)
				
				self.draw(screen, grid)
				pygame.display.flip()
				
			self.draw(screen, grid)
			pygame.display.flip()

		while(True):
			self.draw(screen, grid)
			pygame.display.flip()
			time.sleep(2)
			print ("I've got the way in %d steps" % steps)

	def move_a_star(self, root_row, root_col, grid, final_row, final_col):
		global steps
		visited_a_star = []
		to_visit_a_star = []
		root = Node(root_row, root_col, -1, self.get_cost(root_row, root_col, grid))

		to_visit_a_star.append(root)

		while(to_visit_a_star):
			steps += 1
			node = to_visit_a_star.pop(0)
			# node.cost += self.get_estimate_cost(node, grid, final_row, final_col)

			visited_a_star.append(node)

			border_a_star = self.expand(node, node.cost, grid)
			print ("--------------")
			print ('atual: ', node)

			for b_node in border_a_star:
				origin_to_here_cost = b_node.cost
				# origin_to_here_cost = b_node.cost
				here_to_destiny_cost = self.get_estimate_cost(b_node, grid, final_row, final_col)

				b_node.cost_a_star = origin_to_here_cost + here_to_destiny_cost

				# if (b_node.cost < node.cost):
				# 	b_node.cost = node.cost

				print ("origin_to_here_cost + here_to_destiny_cost: ", origin_to_here_cost, here_to_destiny_cost)

				if (self.is_in_mark_position(grid, b_node)):				
					to_visit_a_star = []
					self.get_the_way(visited_a_star, root, b_node, grid)
					break
				elif (self.is_not_expanded(grid, b_node.row, b_node.col) and self.is_not_in_to_visit(b_node, to_visit_a_star)):
					self.apply_expand_function_in_grid(node.row, node.col, grid)
					to_visit_a_star.append(b_node)
					to_visit_a_star.sort(key=lambda x: x.cost_a_star)

					
					for n in to_visit_a_star:
						print (n)
					print ("--------------")
				
				self.draw(screen, grid)
				pygame.display.flip()
				
			self.draw(screen, grid)
			pygame.display.flip()

		while(True):
			self.draw(screen, grid)
			pygame.display.flip()
			time.sleep(2)
			print ("I've got the way in %d" % steps)

	def expand(self, node, cost, grid):
		row, col = node.row, node.col

		border = []

		if (self.can_move('up', node, grid)):
			future_node = Node(row-1, col, node, cost + self.get_cost(row-1, col, grid))
			border.append(future_node)

		if (self.can_move('right', node, grid)):
			future_node = Node(row, col+1, node, cost + self.get_cost(row, col+1, grid))
			border.append(future_node)
		
		if (self.can_move('down', node, grid)):
			future_node = Node(row+1, col, node, cost + self.get_cost(row+1, col, grid))
			border.append(future_node)
		
		if (self.can_move('left', node, grid)):
			future_node = Node(row, col-1, node, cost + self.get_cost(row, col-1, grid))
			border.append(future_node)

		return border

	def is_in_mark_position(self, grid, node):
		return (grid[node.row][node.col] == constants.MARK_POSITION)

	def can_move(self, direction, node, grid):
		return (direction == 'up' and node.row > 0
				or direction == 'right' and node.col < constants.LIMIT_INDEX_MATRIX
				or direction == 'down' and node.row < constants.LIMIT_INDEX_MATRIX
				or direction == 'left' and node.col > 0)

	def is_not_expanded(self, grid, last_row, last_col):
		return (grid[last_row][last_col] < 10)

	def is_not_in_to_visit(self, node, to_visit):
		for aux in to_visit:
			if (aux.row == node.row and aux.col == node.col):
				return False

		return True

	def apply_expand_function_in_grid(self, row, col, grid):
		if (grid[row][col] != constants.MARK_POSITION):
			grid[row][col] += 10

	def get_cost(self, row, col, grid):
		print ("row, col, grid", row, col, grid[row][col])

		if (self.is_not_expanded(grid, row, col)):
			if (grid[row][col] == constants.FLOOR):
				return constants.FLOOR_COST
			elif (grid[row][col] == constants.MOUNTAIN or grid[row][col]):
				return constants.MOUNTAIN_COST
			elif (grid[row][col] == constants.WATER or grid[row][col]):
				return constants.WATER_COST
			elif (grid[row][col] == constants.FIRE or grid[row][col]):
				return constants.FIRE_COST

		for i in range(10):
			if (grid[row][col] == constants.FLOOR*i):
				return constants.FLOOR_COST
			elif (grid[row][col] == constants.MOUNTAIN or grid[row][col]*i):
				return constants.MOUNTAIN_COST
			elif (grid[row][col] == constants.WATER or grid[row][col]*i):
				return constants.WATER_COST
			elif (grid[row][col] == constants.FIRE or grid[row][col]*i):
				return constants.FIRE_COST

	def get_estimate_cost(self, node, grid, final_row, final_col):
		row_distance = np.abs(final_row - node.row)
		col_distance = np.abs(final_col - node.col)

		return row_distance + col_distance

	def get_the_way(self, visited_nodes, root, final_node, grid):
		aux = final_node

		temp_way = []

		while(aux != -1):
			temp_way.append(aux)
			aux = aux.precedent

		way = list(reversed(temp_way))

		for node in way:
			print ("FINAL WAY: ", node)
			grid[node.row][node.col] = constants.VISITED

	def draw(self, screen, grid):
		x, y = 0, 0
		for row in grid:
			for col in row:
				if col == constants.FLOOR:
					pygame.draw.rect(screen, constants.GREEN, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.MOUNTAIN:
					pygame.draw.rect(screen, constants.BROWN, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.WATER:
					pygame.draw.rect(screen, constants.BLUE, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.FIRE:
					pygame.draw.rect(screen, constants.RED, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.MARK_POSITION:
					pygame.draw.rect(screen, constants.WHITE, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.VISITED:
					pygame.draw.rect(screen, constants.BLACK, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				if col == constants.EXPANDED_FLOOR:
					pygame.draw.rect(screen, constants.DARK_GREEN, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.EXPANDED_MOUNTAIN:
					pygame.draw.rect(screen, constants.DARK_BROWN, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.EXPANDED_WATER:
					pygame.draw.rect(screen, constants.DARK_BLUE, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				elif col == constants.EXPANDED_FIRE:
					pygame.draw.rect(screen, constants.DARK_RED, [x, y, constants.CELL_SIZE - constants.MARGIN_CELL, constants.CELL_SIZE - constants.MARGIN_CELL], 0)
				x = x + constants.CELL_SIZE
			y = y + constants.CELL_SIZE
			x = 0	