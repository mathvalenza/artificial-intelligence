#!/usr/bin/python
from ant import Ant
import pygame
import numpy as np

ALIVE_ANTS_NUM = 50
DEAD_ANTS_NUM = 5000
ENVIROMENT_SIZE = 100
IT_THRESHOLD = 500000

CLOCK_TICK = 100

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
running = True
grid = [[0]*ENVIROMENT_SIZE for n in range(ENVIROMENT_SIZE)]

alive_ants = []
dead_ants = []

def main():
	global grid

	set_dead_ants()
	set_alive_ants()

	pygame.init()

	while (carry_on):
		draw()

def update_alive_ants():
	global alive_ants
	global dead_ants

	count_items = 0

	for ant in alive_ants:
		ant.move()
		count_items, count_possibilities = ant.look_neighbourhood(grid, dead_ants)
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
					item = [x for x in dead_ants if (x.row == ant.row and x.col == ant.col)]
					if (len(item) > 0):
						ant.pick(item, dead_ants)
						grid[ant.row][ant.col] = status["empty"]
						# print ("PEGOU | n_items: ", count_items, "pp: ", probably_pick, "rand: ",random)

			elif (ant.status == status["carrying_ant"] and grid[ant.row][ant.col] == status["empty"]):
				random = np.random.random()
				if (random < probably_drop):
					ant.drop(dead_ants)
					grid[ant.row][ant.col] = status["dead_ant"]
					# print ("DROPOU | n_items: ", count_items, "pd: ", probably_drop, "rand: ",random)
	
	update_grid()

def reset_grid():
	global grid

	grid = [[0]*ENVIROMENT_SIZE for n in range(ENVIROMENT_SIZE)]

def update_grid():
	global alive_ants
	global dead_ants

	reset_grid()

	for ant in alive_ants:
		if (ant.row < 0 or ant.col < 0 or ant.row > ENVIROMENT_SIZE-1 or ant.col > ENVIROMENT_SIZE-1):
			print ("ant: ", ant)
		if (ant.row >= 0 and ant.row <= ENVIROMENT_SIZE-1 and ant.col >=0 and ant.col <= ENVIROMENT_SIZE-1):
			if (grid[ant.row][ant.col] == status["dead_ant"]):
				grid[ant.row][ant.col] = status["alive_overlap_dead"]
			else:
				grid[ant.row][ant.col] = ant.status

	for item in dead_ants:
		if (grid[item.row][item.col] == status["available_ant"] or grid[item.row][item.col] == status["carrying_ant"]):
			grid[item.row][item.col] = status["alive_overlap_dead"]
		else: 
			grid[item.row][item.col] = status["dead_ant"]

def set_dead_ants():
	global grid
	global dead_ants

	row = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = DEAD_ANTS_NUM)
	col = np.random.randint(low = 0, high = ENVIROMENT_SIZE-1, size = DEAD_ANTS_NUM)

	dead_ants_positions = list(zip(row, col))

	for row, col in dead_ants_positions:
		ant = Ant(status["dead_ant"], -1, row, col)
		dead_ants.append(ant)

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
	global dead_ants
	global running

	count_items = 0

	for ant in alive_ants:
		if (ant.status == status["carrying_ant"]):	
			print ("opa")
			ant.move()
			count_items, count_possibilities = ant.look_neighbourhood(grid, dead_ants)
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
						ant.drop(dead_ants)
						grid[ant.row][ant.col] = status["dead_ant"]
	
	if (len(dead_ants) < DEAD_ANTS_NUM):
		update_grid()
	else:
		del alive_ants[:]
		update_grid()

def draw():
	global carry_on
	global grid
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption("Ant Colony")
	clock = pygame.time.Clock()

	it = 0

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
				elif col == status["carrying_ant"]:
					pygame.draw.rect(screen, RED, [x, y, ANT_SIZE, ANT_SIZE], 0)
				elif col == status["alive_overlap_dead"]:
					pygame.draw.rect(screen, YELLOW, [x, y, ANT_SIZE, ANT_SIZE], 0)
				x = x + CELL_SIZE
			y = y + CELL_SIZE
			x = 0	

		if (it >= IT_THRESHOLD and len(dead_ants) < DEAD_ANTS_NUM):
			shutdown_process()
		else:
			update_alive_ants()
			it += 1

		clock.tick(CLOCK_TICK)
		pygame.display.flip()

	pygame.quit()

main()