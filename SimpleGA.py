import sys
import logging
import json
import random
from statistics import mean
from Levenshtein import distance as lev

def onemax(bit_string):
	val = 0;
	for bit in bit_string:
		val += int(bit)
	return val

def trap4(bit_string):
	divisions = len(bit_string)%4
	val = 0
	if divisions == 0:
		for i in range(0, len(bit_string), 4):
			sub_str = bit_string[i:i+4]
			fitness = sub_str.count('1')
			if fitness == 4:
				val += 4
			else:
				val += 3-fitness
	else:
		logger.error("Please enter bit string length which is divisible by 4")
	return val


def interleaved_trap(bit_string):
	divisions = len(bit_string)%4
	val = 0
	if divisions == 0:
		for i in range(len(bit_string)//4):
			for j in range(divisions):
				val += int(bit_string[i+j])
	else:
		logger.error("Please enter bit string length which is divisible by 4")
	return val


def calculate_output(parents, fitness_func):
	scores = [fitness_func(score) for score in parents]
	print("{B:"+str(max(scores))+", A:"+str(mean(scores))+", W:"+str(min(scores))+"}")

def rts(parents, fitness_func, W):
	generation = []
	for parent in parents:
		subset = random.sample(parents, W)

		mostSimilar = subset[0]
		lowestDistance = lev(parent, mostSimilar)

		for i in range(1,len(subset)):
			distancia=	lev(parent, subset[i])

			if distancia < lowestDistance:
				lowestDistance = distancia
				mostSimilar = subset[i]

		if fitness_func(mostSimilar) < fitness_func(parent):
			generation.append(parent)
		else:
			generation.append(mostSimilar)

def tournament(parents, fitness_func):
	random1 = random.randint(0, len(parents)-1)
	random2 = 0
	while(random1 == random2):
		random2 = random.randint(0, len(parents)-1)
	val1 = fitness_func(parents[random1])
	val2 = fitness_func(parents[random2])
	if val1 > val2:
		return random1
	return random2

def mutate(bit_string):
	new_bit_string = ""
	for bit_ind in range(len(bit_string)):
		if bit_string[bit_ind] == "0":
			new_bit_string += "1"
		else:
			new_bit_string += "0"
	return new_bit_string

def cross_over(parent1, parent2, N):
	child1 = list(parent1)
	child2 = list(parent2)
	for k in range(N):
		idx = random.randint(0, N-1)
		temp = child1[idx]
		child1[idx] = child2[idx]
		child2[idx] = temp
	return "".join(child1), "".join(child2)

def one_point_cross_over(parent1, parent2, N):
	split = random.randint(1, N-1)
	child1 = parent1[split:] + parent2[:split]
	child2 = parent2[split:] + parent1[:split]
	child1 = mutate(child1)
	child2 = mutate(child2)
	logging.info("Mutated Child is:")
	logging.info(child1)
	logging.info(child2)
	return child1, child2

def two_point_cross_over(parent1, parent2, N):
	child1, child2 = parent1, parent2
	for k in range(2):
		child1, child2 = one_point_cross_over(child1, child2, N)
	return child1, child2

def create_children(parents, N, n, cross_over_flg):
	children = [""]*N
	if cross_over_flg == 0:
		for i in range(N-1):
			child1, child2 = cross_over(parents[i], parents[i+1], N)
			children[i] = child1
			children[i+1] = child2
		child1, child2 = cross_over(parents[0], parents[N-1], N)
	elif cross_over_flg == 1:
		for i in range(N-1):
			child1, child2 = one_point_cross_over(parents[i], parents[i+1], N)
			children[i] = child1
			children[i+1] = child2
		child1, child2 = one_point_cross_over(parents[0], parents[N-1], N)
	else:
		for i in range(N-1):
			child1, child2 = two_point_cross_over(parents[i], parents[i+1], N)
			children[i] = child1
			children[i+1] = child2
		child1, child2 = two_point_cross_over(parents[0], parents[N-1], N)

	children[0] = child1
	children[N-1] = child2
	return children

def create_generation(n, N):
	parents = []
	for iters in range(N):
		bit_string = [str(random.randint(0,1)) for i in range(n)]
		bit_string = "".join(bit_string)
		parents.append(bit_string)
	return parents

def run_simplega(filename, logger):
	file = open(filename)
	data = json.load(file)
	parents = []
	N = data["N"]
	n = data["n"]
	gen = data["gen"]
	cross_over_flg = data["crossoverOperator"]
	fitness_func_flag = data["fitnessFunction"]
	bisection_flg = data["bisection"]
	rts_flg = data["rts"]
	W = data["W"]
	best = "0"*n

	winner = ""

	logger.info("Initializing the random parent bit strings")
	parents = create_generation(n , N)

	if bisection_flg == 0:
		logger.info("Running the Simple GA algorithm")
		for generation in range(gen):
			logger.warning("generation : "+str(generation+1))
			logger.warning(parents)
			worst = "1"*n
	    
			for select in range(len(parents)):
				if fitness_func_flag == 1:
					winner = tournament(parents, trap4)
					if trap4(parents[winner]) > trap4(best):
						best = parents[winner]
					if trap4(parents[winner]) < trap4(worst):
						worst = parents[winner]
				else:
					winner = tournament(parents, onemax)
					if onemax(parents[winner]) > onemax(best):
						best = parents[winner]
					if onemax(parents[winner]) < onemax(worst):
						worst = parents[winner]
			logger.warning("Worst: "+worst)
			if fitness_func_flag == 1:
				calculate_output(parents, trap4)
			else:
				calculate_output(parents, onemax)
			best_score = n
	    
			for i in range(len(parents)):
				if fitness_func_flag == 1:
					if trap4(parents[i]) == best_score:
						print("Global Fitness Acheived")
						print("Solution : ", parents[i])
						print("Location of solution with global fitness : ", i+1)
				else:
					if onemax(parents[i]) == best_score:
						print("Global Fitness Acheived")
						print("Solution : ", parents[i])
						print("Location of solution with global fitness : ", i+1)
			parents = create_children(parents, N, n, cross_over_flg)
			if rts_flg:
				print("Restricted Tournament Replacement Initialized")
				rts(parents, onemax, W)
			logger.warning("Best : "+best)
	else:
		logger.info("Running the Bisection GA algorithm")
		N_first = 10
		old_convergence = 0
		new_convergence = 0
		while(True):
			for generation in range(gen):
				logger.warning("generation : "+str(generation+1))
				logger.warning(parents)
				worst = "1"*n
		    
				for select in range(len(parents)):
					if fitness_func_flag == 1:
						winner = tournament(parents, trap4)
						if trap4(parents[winner]) > trap4(best):
							best = parents[winner]
						if trap4(parents[winner]) < trap4(worst):
							worst = parents[winner]
					else:
						winner = tournament(parents, onemax)
						if onemax(parents[winner]) > onemax(best):
							best = parents[winner]
						if onemax(parents[winner]) < onemax(worst):
							worst = parents[winner]
				logger.warning("Worst: "+worst)
				if fitness_func_flag == 1:
					calculate_output(parents, trap4)
				else:
					calculate_output(parents, onemax)
				best_score = n
		    
				for i in range(len(parents)):
					if fitness_func_flag == 1:
						if trap4(parents[i]) == best_score:
							print("Global Fitness Acheived")
							print("Solution : ", parents[i])
							print("Location of solution with global fitness : ", i+1)
					else:
						if onemax(parents[i]) == best_score:
							print("Global Fitness Acheived")
							print("Solution : ", parents[i])
							print("Location of solution with global fitness : ", i+1)
				parents = create_children(parents, N, n, cross_over_flg)
				if rts_flg:
					print("Restricted Tournament Replacement Initialized")
					rts(parents, onemax, W)
				logger.warning("Best : "+best)
				old_convergence = new_convergence
				new_convergence = worst
			if old_convergence < new_convergence:
				N_first = (N + N_first)//2
			else:
				N_first = (N - N_first)//2
			if abs(float(worst) - float(old_convergence)) < float(worst)*0.10:
				print("The value of N is : ", N_first)
				break




logger = logging.getLogger()
logger.setLevel(logging.ERROR)
if len(sys.argv) == 1:
	run_simplega("gasettings.dat", logger)
elif len(sys.argv) == 2:
	if sys.argv[1] == "-h":
		logger.warning("This program imitates the Simple GA algorithm")
		logger.warning("The program can be run using the following command")
		logger.warning("sga [-h] [-g] [-G] [filename]")
		logger.warning("-h : option to describe other options")
		logger.warning("-g : option to show limited debugging messages")
		logger.warning("-G : option to show full debugging messages")
		logger.warning("filename: option to enter settings file name. gasettings.dat is selected by default if no name is specified")
	elif sys.argv[1] == "-g":
		logging.basicConfig(level=logging.DEBUG)
		logger.setLevel(logging.DEBUG)
	elif sys.argv[1] == "-G":
		logger.setLevel(logging.WARNING)
	run_simplega("gasettings.dat", logger)
elif len(sys.argv) == 3:
	run_simplega(argv[2], logger)