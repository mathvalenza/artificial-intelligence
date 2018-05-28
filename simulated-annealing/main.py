# import numpy as np

INVALID_CHARS_IN_FILE = ['c', 'p', '0', '%']

INITIAL_INSTANCE = [True, False, False, False, False, False, False, False, False, False, 
	    False, False, False, False, False, False, False, False, False, False]

ITERATIONS = 250000

def main():
	do_random_search()
	

def do_random_search():
	print ("opa")
	function = parse_file()
	# print (function)

	instance = INITIAL_INSTANCE
	best_result = ([], 0)

	i = 0

	while (i < ITERATIONS):
		function_applied = apply_function(function, instance)

		true_clausules_num = evaluate_function(function_applied)

		print (function_applied, true_clausules_num, '\n')

		if (true_clausules_num > best_result[1]):
			best_result = instance, true_clausules_num

		i += 1
		instance = perturb(instance)
		# na verdade, deve chamar generate_new_instance

	print ("----------------- BEST RESULT: ----------------------")
	print (best_result)


def generate_new_instance():
	#TODO: return a random instance

	return INSTANCE	

def perturb(instance):
	index_to_flip = 9

	# print ('instance: ', instance)

	instance[index_to_flip] = not instance[index_to_flip]

	# print ('pertuberd: ', instance)

	return instance

def parse_file():
	file = open("3_SAT_instances/uf20-01.cnf", "r")
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
main()
