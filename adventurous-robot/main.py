#!/usr/bin/python
import pygame
import numpy as np
import time
from robot import Robot
import constants

grid = []

def main():
	global grid
	grid = read_file()

	robot = Robot()

	set_initial_position(robot)
	final_row, final_col = set_mark_position()

	pygame.init()

	pygame.display.set_caption("Adventurous Robot")

	# robot.move_dfs(grid)
	# robot.move_bfs(robot.node.row, robot.node.col, grid)
	# robot.move_uniform_cost(robot.node.row, robot.node.col, grid)
	robot.move_a_star(robot.node.row, robot.node.col, grid, final_row, final_col)

def read_file():
	file = open('environment.txt', 'r')

	grid = []

	for line in file:
		temp = []
		for char in line:
			if (char != '\n' and char != ' '):
				temp.append(int(char))
		grid.append(temp)

	return grid

def set_initial_position(robot):
	initial_row = -1
	initial_col = -1

	while (initial_row < 0 or initial_row > constants.LIMIT_INDEX_MATRIX):
		initial_row = int(input("Please, type the INITIAL ROW: "))

	while (initial_col < 0 or initial_col > constants.LIMIT_INDEX_MATRIX):
		initial_col = int(input("Please, type the INITIAL COLUMN: "))

	robot.node.row = initial_row
	robot.node.col = initial_col

def set_mark_position():
	final_row = -1
	final_col = -1

	while (final_row < 0 or final_row > constants.LIMIT_INDEX_MATRIX):
		final_row = int(input("Please, type the final ROW: "))

	while (final_col < 0 or final_col > constants.LIMIT_INDEX_MATRIX):
		final_col = int(input("Please, type the final COLUMN: "))

	grid[final_row][final_col] = constants.MARK_POSITION

	return final_row, final_col

def set_way_in_grid(way, grid):
	for position in way:
		if (grid[position[0]][position[1]] != constants.MARK_POSITION):
			grid[position[0]][position[1]] = constants.VISITED


main()