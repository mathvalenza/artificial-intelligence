#!/usr/bin/python
import pygame
import numpy as np
import time
from robot import Robot
from robot import Node

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

grid = []

FLOOR = 0
EXPANDED_FLOOR = 10

MOUNTAIN = 1
EXPANDED_MOUNTAIN = 11

WATER = 2
EXPANDED_WATER = 12

FIRE = 3
EXPANDED_FIRE = 13

VISITED = 99
MARK_POSITION = 5

def main():
	global grid
	grid = read_file()

	robot = Robot()

	set_initial_position(robot)
	set_mark_position()

	pygame.init()

	# screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Adventurous Robot")

	robot.move_bfs(robot.node.row, robot.node.col, grid)
	# robot.move_dfs(grid)

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

	while (initial_row < 0 or initial_row > LIMIT_INDEX_MATRIX):
		initial_row = int(input("Please, type the INITIAL ROW: "))

	while (initial_col < 0 or initial_col > LIMIT_INDEX_MATRIX):
		initial_col = int(input("Please, type the INITIAL COLUMN: "))

	robot.node.row = initial_row
	robot.node.col = initial_col
	# grid[initial_row][initial_col] = INITIAL_POSITION

def set_mark_position():
	final_row = -1
	final_col = -1

	while (final_row < 0 or final_row > LIMIT_INDEX_MATRIX):
		final_row = int(input("Please, type the final ROW: "))

	while (final_col < 0 or final_col > LIMIT_INDEX_MATRIX):
		final_col = int(input("Please, type the final COLUMN: "))

	grid[final_row][final_col] = MARK_POSITION

def set_way_in_grid(way, grid):
	for position in way:
		if (grid[position[0]][position[1]] != MARK_POSITION):
			grid[position[0]][position[1]] = VISITED


main()