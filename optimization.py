

import pandas as pd 
import numpy as np
import random

# import location data
data = pd.read_csv('dj38.tsp', sep=' ')


def operator(state, mode='a'):
    ''' permutate 2 cities in state
    '''

    if mode == 'a':
        # select 2 random positiions
        positions = random.sample(range(1, 38), 2)
        a = state[positions[0]]
        b = state[positions[1]]
        # exchange
        state[positions[0]] = b
        state[positions[1]] = a
    elif mode == 'b':
        # select 4 random positiions
        positions = random.sample(range(1, 38), 4)
        a = state[positions[0]]; b = state[positions[1]]; c = state[positions[2]]; d = state[positions[3]]
        # exchange
        state[positions[0]] = b; state[positions[1]] = a; state[positions[2]] = d; state[positions[3]] = c

    return state



def evaluation_function(state, data):
    ''' calculate cost for state
        based on euclidian distance
        among cities
    '''
    state_cost=0
    
    for i in range(len(state)-1):
        # select nodes 
        nodea = data[data.node == state[i]]
        nodeb = data[data.node == state[(i+1)] ]
        
        # calculate euclidian distance
        cost = np.sqrt( (nodea['lat'].item() - nodeb['lat'].item())**2 + (nodea['long'].item() - nodeb['long'].item())**2 )
        state_cost += cost
    
    return state_cost





def ClimbHill(data, expansion_size = 30, mode='a'):

    
    # initialization
    state = random.sample(range(1, 39), 38)   
    state_cost = evaluation_function(state, data)
    generation = 0
    local_stuck = 0

    print('estado inicial: ', state)
    print('custo inicial: ', state_cost)

    # search looop
    found = False
    while found == False:
        # expande filhos do pai
        x=0
        sons_costs = []
        sons = []
        while x < expansion_size:
            permuted_state = operator(state, mode=mode)
            if permuted_state not in sons:
                sons = [list(permuted_state)] + sons
                sons_costs.append(evaluation_function(list(permuted_state), data))
            x+=1

        # get min cost
        min_son_cost = min(sons_costs)
        generation += 1

        # verify local minimum
        if min_son_cost == state_cost:
            local_stuck += 1
            if local_stuck >= 10:
                print('estado final: ', state, '\ncusto final: ', state_cost, '\ngeracoes: ', generation)
                break 

        # DECISION: verify father and son costs
        if min_son_cost <= state_cost:
            state = sons[sons_costs.index(min(sons_costs))]
            state_cost = min(sons_costs)
        else: 
            print('estado final: ', state, '\ncusto final: ', state_cost, '\ngeracoes: ', generation)
            break


for i in range(10):
    print('Search: ', i)
    ClimbHill(data, expansion_size = 100, mode='b')
