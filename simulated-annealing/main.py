import numpy as np
import matplotlib.pyplot as plt
import random

INVALID_CHARS_IN_FILE = ['c', 'p', '0', '%']

ITERATIONS = 25000

SAT_TYPE = "100"
INSTANCE_SIZE = int(SAT_TYPE)
FILE = "3_SAT_instances/uf" + SAT_TYPE + "-01.cnf"


def main():
	function = parse_file()
	instance = generate_first_instance(INSTANCE_SIZE)

	print ("instance: ", instance)
	print ("function: ", function, len(function))

	# history, best_result = random_search(function, instance)
	history, best_result = simulated_annealing(function, instance)

	plot(history)

	print ("----------------- BEST RESULT: ----------------------")
	print (best_result)
	print ("-------------------- HISTORY: ----------------------")
	print (history)

def random_search(function, instance):
	
	best_result = ([], 0)
	history = []

	i = 0

	while (i < ITERATIONS):
		function_applied = apply_function(function, instance)

		true_clausules_num = evaluate_function(function_applied)
		history.append(true_clausules_num)

		if (true_clausules_num > best_result[1]):
			best_result = instance, true_clausules_num

		i += 1
		instance = generate_new_instance(INSTANCE_SIZE)

	return history, best_result

def simulated_annealing(function, instance):
	best_result = ([], 0)

	instance_candidate = instance[:]

	history = []

	i = 0

	while (i < ITERATIONS):
		instance_next = perturb(instance_candidate)

		function_applied_candidate = apply_function(function, instance_candidate)
		function_applied_next = apply_function(function, instance_next)	

		energy_candidate = evaluate_function(function_applied_candidate)
		energy_next = evaluate_function(function_applied_next)

		delta_e = energy_candidate - energy_next 

		if (delta_e < 0):
			instance_candidate = instance_next
			history.append(energy_candidate)
		else:
			temperature = function_temperature(i, ITERATIONS)

			probability = np.e**(-1*delta_e / temperature)

			random = np.random.random_sample()
			if (random < probability):
				instance_candidate = instance_next
				history.append(energy_candidate)

		if (energy_candidate > best_result[1]):
			best_result = instance_candidate, energy_candidate
		i += 1

	return history, best_result

def function_temperature(i, n):
	t_0 = float(n)
	t_n = 1.0

	return t_0*(t_n / t_0)**(float(i) / float(n))


def generate_first_instance(size):
	first_instance = []
	for i in range(size):
		first_instance.append(False)

	return first_instance

def generate_new_instance(size):
	new_instance = []

	for i in range(size):
		new_instance.append(bool(random.getrandbits(1)))

	return new_instance	

def perturb(instance):
	new_instance = instance[:]

	index_to_flip = np.random.randint(len(instance))

	new_instance[index_to_flip] = not new_instance[index_to_flip]

	return new_instance

def parse_file():
	file = open(FILE, "r")
	instance = []
	for line in file:
		if(line[0] not in INVALID_CHARS_IN_FILE):
			instance.append([int(x) for x in line.split() if x != '0'])

	return instance

def apply_function(function, instance):
	function_applied = []

	for clausule in function:
		clausule_applied = []
		for variable in clausule:
			if (variable > 0):
				clausule_applied.append(instance[variable-1])
			else:
				clausule_applied.append(instance[(variable*-1)-1])
		function_applied.append(clausule_applied)

	return function_applied

def evaluate_function(function_applied):
	true_clausules_num = 0

	for clausule in function_applied:
		if (clausule[0] or clausule[1] or clausule[2]):
			true_clausules_num += 1

	return true_clausules_num

def plot(y_array):
	x_array = range(len(y_array))

	plt.plot(x_array, y_array)
	plt.show()

main()
