import pyibl
import random
import csv
from datetime import date

PAIRINGS = {
    "disconnected": [(0, 1), (2, 3), (4, 5)], #3 edge for disconnected
    "ring": [(0, 1), (2, 3), (4,5), #6 edges for ring
             (1, 2), (3, 4), (0, 5)],
    "fully-connected": [(0, 1), (2, 3), (4,5),
                        (1, 2), (3, 4), (0, 5),
                        (0,2),(3,5),(4,1),
                        (2,4),(5,1),(0,3),
                        (2,5),(0,4),(1,3) ]} #15 C(6,2) for fully connected graph
# the list are shuffled randomly to make sure 

GROUPS = 100
ROUNDS = 100
NODES = 6
MISMATCH_PENALTY = 0.1

GAME = {('cooperate', 'cooperate'): (5, 5),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (0, 0)} 

PREPOPULATED_VALUE = 1.05 * max(max(pair) for pair in GAME.values())


def main():

    #prep file
    logfile=f"log-{date.today()}.csv"
    file = open(logfile, 'w')
    writer = csv.writer(file)
    writer.writerow(("network,participant cluster,round,"
                            "player 1,player 2,"
                        "player 1 choice,player 2 choice,"
                        "player 1 rep,player 2 rep," #new code
                        "player 1 payoff,player 2 payoff").split(","))   


    #first assign group number (
    # e.g. 10 groups means 10 different group of agents assigned to each condition) 
    for group_number in range(GROUPS):
        #condition = PAIRINGS.keys()
        
        #then assign condition as in network layout
        #the condition are keys of PAIRING, i.e. disconnected, fully connected, ring
        
        for condition in PAIRINGS.keys():
            random.shuffle(PAIRINGS[condition])   
            #create agents
            # adding partial matching
            agents = [pyibl.Agent(str(name),["button", "reputation"],default_utility=PREPOPULATED_VALUE, mismatch_penalty=MISMATCH_PENALTY ) for name in range(NODES) ]
         

            #initialize buttons
            cooperate_CC = { "button": "cooperate", "reputation": 'CC' }
            cooperate_CD = { "button": "cooperate", "reputation": 'CD' }
            cooperate_DC = { "button": "cooperate", "reputation": 'DC' }
            cooperate_DD = { "button": "cooperate", "reputation": 'DD' }
            defect_CC = { "button": "defect", "reputation": 'CC' }
            defect_CD = { "button": "defect", "reputation": 'CD' }
            defect_DC = { "button": "defect", "reputation": 'DC' }
            defect_DD = { "button": "defect", "reputation": 'DD' }

            #initialize first move 
            last_move_list = ['o'] *NODES 
            for i in range(NODES):
                last_move_list[i] = random.choice('CD') 

            #run sim
            for simulation_rounds in range(ROUNDS):
                for p in (PAIRINGS[condition]):   

                    a = agents[p[0]]
                    b = agents[p[1]]

                    last_round = last_move_list[p[0]] + last_move_list[p[1]]#a_last+b_last

                    # make new choice based on past repuation of both participant
                    if last_round == 'CC':
                        result_a = a.choose(cooperate_CC, defect_CC)
                        result_b = b.choose(cooperate_CC, defect_CC)
                    elif last_round == 'CD':
                        result_a = a.choose(cooperate_CD, defect_CD)
                        result_b = b.choose(cooperate_DC, defect_DC)
                    elif last_round == 'DC':
                        result_a = a.choose(cooperate_DC, defect_DC)
                        result_b = b.choose(cooperate_CD, defect_CD)
                    elif last_round == 'DD':
                        result_a = a.choose(cooperate_DD, defect_DD)
                        result_b = b.choose(cooperate_DD, defect_DD)

                    # update result
                    pair_result = (result_a['button'],result_b['button'])

                    if pair_result == ('cooperate', 'cooperate'):
                        a.respond(5)
                        b.respond(5)
                        (last_move_list[p[0]],last_move_list[p[1]])=('CC')
    
                        
                    elif pair_result == ('cooperate', 'defect'):
                        a.respond(0)
                        b.respond(5)
                        (last_move_list[p[0]],last_move_list[p[1]])=('CD')
                
                    elif pair_result == ('defect', 'cooperate'):
                        a.respond(5)
                        b.respond(0)
                        (last_move_list[p[0]],last_move_list[p[1]])=('DC')
        
                    elif pair_result == ('defect', 'defect'):
                        a.respond(0)
                        b.respond(0)
                        (last_move_list[p[0]],last_move_list[p[1]])=('DD')
        

                    payoffs = GAME[pair_result] 
                    writer.writerow([condition, group_number, simulation_rounds] + list(p) + list(pair_result)+ list(last_round) + list(payoffs))
    
    return()

