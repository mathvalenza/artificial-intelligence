#!/usr/bin/python
import numpy as np

NEW_POSITIONS_POSSIBILITIES = 8
ENVIROMENT_SIZE = 50

class Ant:
	status = 0
	row_old = 0
	col_old = 0
	row = 0
	col = 0

	def __init__(self, status, row_old, col_old, row, col):
		self.status = status
		self.row_old = row_old
		self.col_old = col_old
		self.row = row
		self.col = col

	def __str__(self):
		return "status: %s, row: %s, col: %s" % (self.status, self.row, self.col)

	def __repr__(self):
		return str(self)

	def set_status(status):
		self.status = status

	def move(self):
		direction = np.random.randint(low = 1, high = NEW_POSITIONS_POSSIBILITIES+1, size = 1)
		direction = direction[0]

		if (self.is_in_margin()):
			if (self.can_move(direction) == False):
				oposite_direction = self.get_oposite_direction(direction)
				# print ("not can move ", self.row, self.col, oposite_direction)
				self.set_new_position_by_direction(oposite_direction)
			else:
				# print ("in margin but can move ", self.row, self.col, direction)
				self.set_new_position_by_direction(direction)
		else:
			# print ("it is not in the margin ", self.row, self.col, direction)
			self.set_new_position_by_direction(direction)

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
		# print ("new_position: ", row, col)

	# C = current position
	# each number represents a future direction in the grid, like above:
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

	def is_in_margin(self):
		if (self.row == 0 or self.col == 0 or self.row == ENVIROMENT_SIZE-1 or self.col == ENVIROMENT_SIZE-1):
			return True
		return False