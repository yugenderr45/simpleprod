from random import random

class Answer(object):
    def __init__(self, value):
        self.value = value
        self.score = 0

    def calculate_fitness(self, fitness_func):
        self.score = fitness_func(self.value)


def gen_child(population):
    val = ""
    for bit in population:
        if random() < bit:
            val = val + "1"
        else:
            val = val + "0"
    return Answer(val)


def gen_list(size):
    return [0.5]*size


def tournament(child1, child2):
    if child1.score > child2.score:
        return child1, child2
    return child2, child1


def upd_list(population, best, worst, population_size):
    for i in range(len(population)):
        if best[i] != worst[i]:
            if best[i] == '1':
                population[i] += 1.0 / float(population_size)
            else:
                population[i] -= 1.0 / float(population_size)


def run(generations, size, population_size, fitness_function):
    population = gen_list(size)
    best = None

    for i in range(generations):
        s1 = gen_child(population)
        s2 = gen_child(population)

        s1.calculate_fitness(fitness_function)
        s2.calculate_fitness(fitness_function)

        best, worst = tournament(s1, s2)

        if best:
            if best.score > best.score:
                best = best
        else:
            best = best

        upd_list(population, best.value, worst.value, population_size)
        print(f"generation: {i+1} best value: {best.value} best score: {float(best.score)}")

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

if __name__ == '__main__':
    run(1000, 40, 10, trap4) # The score from simpleGA is less compared to compactGA