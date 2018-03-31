#!/usr/bin/python
import numpy as np

NEW_POSITIONS_POSSIBILITIES = 8
ENVIROMENT_SIZE = 100
RADIUS_VISION = 1

status = {
	"dead_ant": -1,
	"empty": 0,
	"available_ant": 1,
	"carrying_ant": 2,
	"alive_overlap_dead": 3
}

class Ant:
	status = 0
	last_direction = 0
	row = 0
	col = 0

	def __init__(self, status, old_direction, row, col):
		self.status = status
		self.last_direction = old_direction
		self.row = row
		self.col = col

	def __str__(self):
		return "status: %s, row: %s, col: %s, old_direction: %s" % (self.status, self.row, self.col, self.last_direction)

	def __repr__(self):
		return str(self)

	def set_status(self, status):
		self.status = status

	def move(self):
		direction = self.get_new_direction()
		

		if (self.to_the_other_side(direction)):
			self.set_in_the_other_side(self.row, self.col, direction)
		else:
			self.set_new_position_by_direction(direction)

		self.last_direction = direction

	def get_new_direction(self):
		new_direction = np.random.randint(low = 1, high = NEW_POSITIONS_POSSIBILITIES+1, size = 1)
		new_direction = new_direction[0]

		if (new_direction == self.get_oposite_direction(self.last_direction)):
			return self.get_oposite_direction(new_direction)

		return new_direction

	def set_new_position_by_direction(self, new_direction):
		if new_direction == 1:
			self.row -= 1
			self.col -= 1
		elif new_direction == 2:
			self.row -= 1
		elif new_direction == 3:
			self.row -= 1
			self.col += 1 
		elif new_direction == 4:
			self.col -= 1
		elif new_direction == 5:
			self.col += 1
		elif new_direction == 6:
			self.row += 1
			self.col -= 1
		elif new_direction == 7:
			self.row += 1
		elif new_direction == 8:
			self.row += 1
			self.col += 1

	# C = current position
	# each number represents a future direction in the grid:
	# | 1 | 2 | 3 |
	# | 4 | C | 5 |
	# | 6 | 7 | 8 |
	def can_move(self, direction):
		if (direction == 1 or direction == 2 or direction == 3):
			if (self.row == 0):
				return False
		
		if (direction == 1 or direction == 4 or direction == 6):
			if (self.col == 0):
				return False
		
		if (direction == 6 or direction == 7 or direction == 8):
			if (self.row == ENVIROMENT_SIZE-1):
				return False
		
		if (direction == 3 or direction == 5 or direction == 8):
			if (self.col == ENVIROMENT_SIZE-1):
				return False

		return True

	def get_oposite_direction(self, direction):
		if direction == 1:
			return 8
		elif direction == 2:
			return 7
		elif direction == 3:
			return 6
		elif direction == 4:
			return 5
		elif direction == 5:
			return 4
		elif direction == 6:
			return 3
		elif direction == 7:
			return 2
		elif direction == 8:
			return 1

		return 0

	def to_the_other_side(self, direction):
		if (self.row == 0):
			if (direction == 1 or direction == 2 or direction == 3):
				return True
		elif (self.row == ENVIROMENT_SIZE-1):
			if (direction == 6 or direction == 7 or direction == 8):
				return True
		
		if (self.col == 0):
			if (direction == 1 or direction == 4 or direction == 6):
				return True
		elif (self.col == ENVIROMENT_SIZE-1):
			if (direction == 3 or direction == 5 or direction == 8):
				return True
		
		return False

	def set_in_the_other_side(self, row, col, direction):
		if (row == 0):
			if (direction == 1 or direction == 2 or direction == 3):
				self.row = ENVIROMENT_SIZE-1
		elif (row == ENVIROMENT_SIZE-1):
			if (direction == 6 or direction == 7 or direction == 8):
				self.row = 0

		if (col == ENVIROMENT_SIZE-1):
			if (direction == 3 or direction == 5 or direction == 8):
				self.col = 0
		elif (col == 0):
			if (direction == 1 or direction == 4 or direction == 6):
				self.col = ENVIROMENT_SIZE-1

	def look_neighbourhood(self, grid, dead_ants):
		count_items = 0
		count_possibilites = NEW_POSITIONS_POSSIBILITIES*RADIUS_VISION

		for i in range(-RADIUS_VISION, RADIUS_VISION+1, 1):
			for j in range(-RADIUS_VISION, RADIUS_VISION+1, 1):
				if (self.row+i < ENVIROMENT_SIZE and self.col+j < ENVIROMENT_SIZE-1):
					if (i != 0 or j != 0):
						if (grid[self.row+i][self.col+j] == status["dead_ant"] or grid[self.row+i][self.col+j] == status["alive_overlap_dead"]):
							count_items += 1

		return count_items, count_possibilites

	def pick(self, item, dead_ants):
		dead_ants.remove(item[0])
		self.status = 2

	def drop(self, dead_ants):
		item = Ant(-1, -1, self.row, self.col)
		self.status = 1

		dead_ants.append(item)