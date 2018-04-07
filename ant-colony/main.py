#!/usr/bin/python
from ant import Ant
import pygame
import numpy as np

ALIVE_ANTS_NUM = 50
DEAD_ANTS_NUM = 5000
ENVIROMENT_SIZE = 100
IT_THRESHOLD = 500000

CLOCK_TICK = 300

BACKGROUND_COLOR = (50, 50, 50)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (250, 250, 250)
RED = (255, 0, 0)
YELLOW = (255, 207, 16)

CELL_SIZE = 7
ANT_SIZE = CELL_SIZE - 0.1

SCREEN_MARGIN = 2
SCREEN_SIZE = (CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN, CELL_SIZE*ENVIROMENT_SIZE + SCREEN_MARGIN)

status = {
	"dead_ant": -1,
	"empty": 0,
	"available_ant": 1,
	"carrying_ant": 2,
	"alive_overlap_dead": 3
}

carry_on = True
grid = [[0]*ENVIROMENT_SIZE for n in range(ENVIROMENT_SIZE)]

alive_ants = []
dead_ants = []

def main():
	global grid
	global carry_on

	set_dead_ants()
	set_alive_ants()

	pygame.init()

	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Ant Colony")

	screen.fill(BACKGROUND_COLOR)

	it = 0
	while (carry_on):
		if (it >= IT_THRESHOLD and len(dead_ants) < DEAD_ANTS_NUM):
			shutdown_process()
		else:
			if (it == 0 or it == 100000 or it == 300000 or it == 499999):
				print ("it: ", it)
				draw(screen)
			update_alive_ants()
			it += 1
			pygame.display.flip()

def update_alive_ants():
	global alive_ants
	global grid
	count_items = 0

	for ant in alive_ants:
		ant.move()

		count_items, count_possibilities = ant.look_neighbourhood(grid)
		probably_pick, probably_drop = 0, 0

		if (count_items > 0):	
			if (ant.status == status["available_ant"]):
				probably_pick = 1 - (count_items / count_possibilities)
			if (ant.status == status["carrying_ant"]):
				probably_drop = (count_items / count_possibilities)
		else:
			probably_pick = 1
			probably_drop = 0

		if (ant.row < ENVIROMENT_SIZE-1  and ant.col < ENVIROMENT_SIZE-1):			
			if (ant.status == status["available_ant"] and grid[ant.row][ant.col] == status["dead_ant"]):
				random = np.random.random()
				if (random < probably_pick):
						ant.pick()
						grid[ant.row][ant.col] = status["empty"]
					
			elif (ant.status == status["carrying_ant"] and grid[ant.row][ant.col] == status["empty"]):
				random = np.random.random()
				if (random < probably_drop):
					ant.drop()
					grid[ant.row][ant.col] = status["dead_ant"]

def set_dead_ants():
	global grid

	row = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = DEAD_ANTS_NUM)
	col = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = DEAD_ANTS_NUM)

	dead_ants_positions = list(zip(row, col))

	for row, col in dead_ants_positions:
		ant = Ant(status["dead_ant"], -1, row, col)
		grid[row][col] = status["dead_ant"]
			

def set_alive_ants():
	global grid
	global alive_ants

	row = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = ALIVE_ANTS_NUM)
	col = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = ALIVE_ANTS_NUM)

	alive_ants_positions = list(zip(row, col))

	for row, col in alive_ants_positions:
		ant = Ant(status["available_ant"], -1, row, col)
		alive_ants.append(ant)

def shutdown_process():
	global alive_ants

	count_items = 0

	for ant in alive_ants:
		if (ant.status == status["carrying_ant"]):
			ant.move()
			count_items, count_possibilities = ant.look_neighbourhood(grid)
			probably_pick, probably_drop = 0, 0

			if (count_items > 0):	
				if (ant.status == status["available_ant"]):
					probably_pick = 1 - (count_items / count_possibilities)
				if (ant.status == status["carrying_ant"]):
					probably_drop = (count_items / count_possibilities)
			else:
				probably_pick = 1
				probably_drop = 0

			if (ant.row < ENVIROMENT_SIZE-1  and ant.col < ENVIROMENT_SIZE-1):
				if (ant.status == status["carrying_ant"] and grid[ant.row][ant.col] == status["empty"]):
					random = np.random.random()
					if (random < probably_drop):
						ant.drop()
						grid[ant.row][ant.col] = status["dead_ant"]


def draw(screen):
	global carry_on
	global grid

	x, y = 0, 0
	for row in grid:
		for col in row:
			if col == status["empty"]:
				pygame.draw.rect(screen, BACKGROUND_COLOR, [x, y, ANT_SIZE, ANT_SIZE], 0)
			elif col == status["dead_ant"]:
				pygame.draw.rect(screen, BLACK, [x, y, ANT_SIZE, ANT_SIZE], 0)
			elif col == status["available_ant"]:
				pygame.draw.rect(screen, GREEN, [x, y, ANT_SIZE, ANT_SIZE], 0)
			elif col == status["carrying_ant"]:
				pygame.draw.rect(screen, RED, [x, y, ANT_SIZE, ANT_SIZE], 0)
			elif col == status["alive_overlap_dead"]:
				pygame.draw.rect(screen, YELLOW, [x, y, ANT_SIZE, ANT_SIZE], 0)
			x = x + CELL_SIZE
		y = y + CELL_SIZE
		x = 0	

main()