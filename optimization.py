

import pandas as pd 
import numpy as np
import random

# import location data
data = pd.read_csv('dj38.tsp', sep=' ')


def operator(state):
    ''' permutate 2 cities in state
    '''

    # select 2 random positiions
    positions = random.sample(range(1, 38), 2)
    a = state[positions[0]]
    b = state[positions[1]]

    # exchange
    state[positions[0]] = b
    state[positions[1]] = a

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





def ClimbHill(data, expansion_size = 10):

    ## random initialization of state
    state = random.sample(range(1, 39), 38)

    # init variables
    state_cost = evaluation_function(state, data)
    generation = 0
    sons = []
    sons_costs = []

    print('initial state: ', state)
    print('initial cost: ', state_cost)

    found = False
    while found == False:
        # expande filhos do pai
        x=0
        while x < expansion_size:
            permuted_state = operator(state)
            if permuted_state not in sons:
                sons = [list(permuted_state)] + sons
                sons_costs.append(evaluation_function(list(permuted_state), data))
            x+=1

        # verificar se filho de menor custo
        # tem custo menor que pai, se sim, filho vira pai,
        # se nao, retorna o pai
        min_son_cost = min(sons_costs)
        print(min_son_cost)
        if min_son_cost < state_cost:
            state = sons[sons_costs.index(min(sons_costs))]
            state_cost = min(sons_costs)
            generation += 1
            print('geracao: ', generation, '\n')
        else: 
            print('estado final: ', state)
            print('custo final: ', state_cost)
            print('geracoes: ', generation)
            return state, state_cost, generation


ClimbHill(data, expansion_size = 300)