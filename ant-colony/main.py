#!/usr/bin/python
from ant import Ant
import pygame
import numpy as np

BACKGROUND_COLOR = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (250, 250, 250)
DARK_GREEN = (50, 100, 50)

CELL_SIZE = 12
ANT_SIZE = CELL_SIZE - 4
ENVIROMENT_SIZE = 50

SCREEN_MARGIN = 2
SCREEN_SIZE = (CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN, CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN)

ALIVE_ANTS_NUM = 50
DEAD_ANTS_NUM = 500

status = {
	"dead_ant": -1,
	"empty": 0,
	"available_ant": 1,
	"alive_overlap_dead": 2
}

carry_on = True
grid = [[0]*ENVIROMENT_SIZE for n in range(ENVIROMENT_SIZE)]

alive_ants = []
dead_ants = []

def main():
	global grid

	set_dead_ants()
	set_alive_ants()
	# print ("alive_ants: ", list(alive_ants), len(alive_ants))

	pygame.init()

	draw()

def update_alive_ants():
	global alive_ants
	for ant in alive_ants:
		if (ant.row < ENVIROMENT_SIZE-1 and ant.col < ENVIROMENT_SIZE-1):
			ant.move()

	update_grid()

# C = current position
# each number represents a future direction in the grid, like above:
# | 1 | 2 | 3 |
# | 4 | C | 5 |
# | 6 | 7 | 8 |

def reset_grid():
	global grid

	grid = [[0]*ENVIROMENT_SIZE for n in range(ENVIROMENT_SIZE)]

def update_grid():
	global grid
	global alive_ants
	global dead_ants

	reset_grid()

	for ant in alive_ants:
		# print ("ant: ", ant.x, ant.y)
		if (grid[ant.row][ant.col] == status["dead_ant"]):
			grid[ant.row][ant.col] = status["alive_overlap_dead"]
		else:
			grid[ant.row][ant.col] = status["available_ant"]

	for ant in dead_ants:
		if (grid[ant.row][ant.col] == status["available_ant"]):
			grid[ant.row][ant.col] = status["alive_overlap_dead"]
		else: 
			grid[ant.row][ant.col] = status["dead_ant"]

def set_dead_ants():
	global grid
	global dead_ants

	row = np.random.randint(low = 0, high = ENVIROMENT_SIZE, size = DEAD_ANTS_NUM)
	col = np.random.randint(low = 0, high = ENVIROMENT_SIZE, size = DEAD_ANTS_NUM)

	dead_ants_positions = list(zip(row, col))

	for row, col in dead_ants_positions:
		ant = Ant(status["dead_ant"], -1, -1, row, col)
		dead_ants.append(ant)

def set_alive_ants():
	global grid
	global alive_ants

	row = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = ALIVE_ANTS_NUM)
	col = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = ALIVE_ANTS_NUM)

	alive_ants_positions = list(zip(row, col))

	for row, col in alive_ants_positions:
		ant = Ant(status["available_ant"], -1, -1, row, col)
		alive_ants.append(ant)

def draw():
	global carry_on
	global grid
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("The first one")
	clock = pygame.time.Clock()

	screen.fill(BACKGROUND_COLOR)

	while (carry_on):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				carry_on = False

		x, y = 0, 0
		for row in grid:
			for col in row:
				if col == status["empty"]:
					pygame.draw.rect(screen, BACKGROUND_COLOR, [x, y, ANT_SIZE, ANT_SIZE], 0)
				elif col == status["dead_ant"]:
					pygame.draw.rect(screen, BLACK, [x, y, ANT_SIZE, ANT_SIZE], 0)
				elif col == status["available_ant"]:
					pygame.draw.rect(screen, GREEN, [x, y, ANT_SIZE, ANT_SIZE], 0)
				elif col == status["alive_overlap_dead"]:
					pygame.draw.rect(screen, DARK_GREEN, [x, y, ANT_SIZE, ANT_SIZE], 0)
				x = x + CELL_SIZE
			y = y + CELL_SIZE
			x = 0

		update_alive_ants()
		clock.tick(4)
		pygame.display.flip()

	pygame.quit()

main()