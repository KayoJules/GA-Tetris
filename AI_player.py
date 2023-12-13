"""
This controls games key and aims to get a high score
"""
from copy import copy, deepcopy
from numpy import array, mean
from random import choice
import random
from main import population_size, generations, top_percentage, mutation_rate, trials
import main

global_weights = [10.0, -2.1, 0.3, 0.15, -1.1, -2.0]
output = 'output.txt'

class AI:
    def __init__(self):
        self.direction = None

    def control(self, sqs_given, status):
        if sqs_given.curr_sq == sqs_given.st.new or self.direction is None:
            self.direction = make_choice(sqs_given)
        else:
            move(sqs_given, self.direction, status)

def move(sqs_given, direction, status):
    # rotation
    if sqs_given.rotate_curr != direction['rotate']:
        status.rotate = True
    else:
        status.rotate = False
    # horizontal left
    if sqs_given.curr_sq[1] > direction['center'][1]:
        status.left = True
    # horizontal right
    elif sqs_given.curr_sq[1] < direction['center'][1]:
        status.right = True
    # horizontal stop
    else:
        status.left = False
        status.right = False
    # vertical drop
    if sqs_given.curr_sq[0] != direction['center'][0]:
        status.down = True
    else:
        status.down = False

def make_choice(sqs_given):
    '''return one direction to go'''
    sqs = copy_sqs(sqs_given)
    pos_data = get_all_possible_pos(sqs)
    evaluate_full_situation(sqs, pos_data)
    all_highest = get_all_highest(pos_data)
    return choice(all_highest)

def get_all_highest(pos_data):
    '''highest marks might not be distinct, so return all of them'''
    # find highest mark
    highest_key = lambda dict:dict['mark']
    max_data = max(pos_data, key=highest_key)
    max_mark = max_data['mark']
    # get all data with this mark
    all_highest = []
    for data in pos_data:
        if data['mark'] == max_mark:
            all_highest.append(data)
    return all_highest


def get_all_possible_pos(sqs_given):
    # copy given sqs for safety
    sqs_origin = copy_sqs(sqs_given)

    # reset rotation
    sqs_origin.curr_shape = sqs_origin.origin_shape
    sqs_origin.rotate_curr = 1
    
    # generate pos
    pos = []
    for rotate in range(sqs_origin.rotate_limit):
        sqs = copy_sqs(sqs_origin)
        sqs_origin.rotate(sqs_origin)
        get_end_pos_with_rotate(pos, sqs)
    return pos

def get_end_pos_with_rotate(pos, sqs):
    move_sq_to_left(sqs)
    old_sq = None
    # move to right and record each position with drop to the end
    while old_sq != sqs.curr_sq:
        sqs_curr = copy_sqs(sqs)
        sqs_curr.drop_straight(sqs_curr)
        record_curr_pos(pos, sqs_curr)
        old_sq = sqs.curr_sq
        sqs.right(sqs)

def copy_sqs(sqs):
    '''this copies sqs safely'''
    sqs_copy = copy(sqs)
    sqs_copy.squares = deepcopy(sqs.squares)
    sqs_copy.curr_sq = deepcopy(sqs.curr_sq)
    sqs_copy.curr_shape = deepcopy(sqs.curr_shape)
    return sqs_copy

def move_sq_to_left(sqs):
    old_sq = None
    while old_sq != sqs.curr_sq:
        old_sq = sqs.curr_sq
        sqs.left(sqs)

def record_curr_pos(pos, sqs):
    '''record all active squares'''
    all_pos = []
    y = sqs.curr_sq[0]
    x = sqs.curr_sq[1]
    all_pos.append([y, x])
    for sq in sqs.curr_shape:
        all_pos.append([y+sq[0], x+sq[1]])
    pos.append({'all_pos':all_pos, 'center':sqs.curr_sq, 'rotate':sqs.rotate_curr})

def evaluate_full_situation(sqs, positions):
    for pos_data in positions:
        pos = pos_data['all_pos']
        sqs_curr = copy_sqs(sqs)
        map_pos_to_sqs(sqs_curr, pos)
        pos_data['mark'] = evaluate_situation(sqs_curr)

def evaluate_situation(sqs):
    full_lines = evaluate_full_lines(sqs)
    sqs.clean_full_lines(sqs)
    squares = array(sqs.squares).T  # convert rows to colomns
    hidden_squares = evaluate_hidden_squares(squares)
    lowest_column, average_column, absolute_diff = evaluate_column(squares)
    valleys = evaluate_ledges(squares)
    return evaluate_mark(full_lines, hidden_squares, lowest_column, average_column, absolute_diff, valleys)

def evaluate_full_lines(sqs_given):
    sqs = copy_sqs(sqs_given)
    full_lines = 0
    for line in sqs.squares:
        if line.count('none') == 0:
            full_lines += 1
    return full_lines

def evaluate_hidden_squares(squares):
    '''find the number of non-squares under squares'''
    hidden_squares = 0
    for colomn in squares:
        found_first_sq = False
        for sq in colomn:
            # find first square
            if not found_first_sq:
                if sq != 'none':
                    found_first_sq = True
                else:
                    continue
            # find hidden squares
            if sq == 'none':
                hidden_squares += 1
    return hidden_squares

def evaluate_column(squares):
    '''count lowest and average space left in every column'''
    space_left = []
    for column in squares:
        appended = False
        for index, sq in enumerate(column):
            # check every square
            if sq != 'none':
                space_left.append(index)
                appended = True
                break
        if not appended:
            space_left.append(len(column))
    return (min(space_left), mean(space_left), max(space_left)-min(space_left))

def evaluate_ledges(squares):
    space_left = []
    for column in squares:
        appended = False
        for index, sq in enumerate(column):
            # check every square
            if sq != 'none':
                space_left.append(index)
                appended = True
                break
        if not appended:
            space_left.append(len(column))
    
    num_ledges = 0

    for i in range (1, len(space_left)):
        if abs(space_left[i] - space_left[i-1]) >= 3:
            num_ledges += 1

    return num_ledges

def evaluate_mark(full_lines, hidden_squares, lowest_column, average_column, absolute_diff, ledges):

    global global_weights

    mark = 0
    mark += full_lines * global_weights[0]
    mark += hidden_squares * global_weights[1]
    mark += lowest_column * global_weights[2]
    mark += average_column * global_weights[3]
    mark += absolute_diff * global_weights[4]
    mark += ledges * global_weights[5]

    return mark

def print_weights(weights):
    print("Weights:", end=" ")
    for i in weights:
        print(i, end=" ")
    print("")

def map_pos_to_sqs(sqs, positions):
    for pos in positions:
        sqs.squares[pos[0]][pos[1]] = 'map'


def crossover(parent1, parent2):

    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]

    return child

# Generate random weights based on original weights
def generate_random_weights():
    original_values = [10.0, -2.1, 0.3, 0.15, -1.1, -2.0]
    randomized_weights = []

    for value in original_values:
        lower_bound = value * 0.5  # 50% of the original value
        upper_bound = value * 2.0  # 200% of the original value
        randomized_value = round(random.uniform(lower_bound, upper_bound),3)
        randomized_weights.append(round(randomized_value, 2))

    # print_weights(randomized_weights)
    return randomized_weights

# Generates initial population
def init_population(pop_size):
    return [(generate_random_weights(), 0) for _ in range(pop_size)]

# Sorts population by highest to lowest performing
def sort_population(population):
    return sorted(population, key=lambda x: x[1], reverse=True)

# Gather top performers from population list; returns tuple
def get_top_performers(population, top_percentage):
    sorted_population = sort_population(population)
    top_count = int(len(sorted_population) * top_percentage)

    return sorted_population[:top_count]

# Mutation
def mutate(weights, mutation_rate):
    mutated_weights = [round(w + random.uniform(-mutation_rate, mutation_rate), 3) for w in weights]
    return mutated_weights

# Hm
def run_generation(population):
    global global_weights
    with open(output, 'a') as file:     # a = append ; w = truncate & write

        for pop_index in range(population_size):

            weights, _ = population[pop_index]
            global_weights = weights
            scores = []

            print_weights(global_weights)

            for i in range(trials):

                run_score = main.run()
                scores.append(run_score)
                file.write(str(run_score) + '\n')

            run_score_avg = round(sum(scores) / len(scores), 2)
            print("Score Average: ", run_score_avg)
            file.write(str(run_score_avg) + '\n')
            population[pop_index] = (weights, run_score_avg)

        file.flush()    # live updates file
        print("------------ Generation Complete! ------------")

def genetic_main():
    population = init_population(population_size)

    for generation in range(generations):
        print("Generation: ", generation)
        run_generation(population)

        top_performers = get_top_performers(population, top_percentage)
        population = [(generate_random_weights(), 0) for _ in range(population_size)]
        
        for i in range(population_size - len(top_performers)):
            parent1, parent2 = random.sample(top_performers, 2)          
            child_weights = crossover(parent1[0], parent2[0])           
            child_weights = mutate(child_weights, mutation_rate)

            # Elitism | Directly pass on top gene to new gen
            population[0] = top_performers[0]

            # Places spliced/mutated genes into new gen, starting at end of list index-wise
            population[int(len(top_performers) + i)] = (child_weights, 0)

def export_weights(weights):
    return(weights)
    
