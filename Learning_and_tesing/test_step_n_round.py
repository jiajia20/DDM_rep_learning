#from random import random
import random
def play_round(agents,NODES, agent_set_in_pairs):

    last_move_list = ['o'] *NODES 
    for i in range(NODES):
        last_move_list[i] = random.choice('CD') 

    #initialize buttons
    cooperate_CC = { "button": "cooperate", "reputation": 'CC' }
    cooperate_CD = { "button": "cooperate", "reputation": 'CD' }
    cooperate_DC = { "button": "cooperate", "reputation": 'DC' }
    cooperate_DD = { "button": "cooperate", "reputation": 'DD' }
    defect_CC = { "button": "defect", "reputation": 'CC' }
    defect_CD = { "button": "defect", "reputation": 'CD' }
    defect_DC = { "button": "defect", "reputation": 'DC' }
    defect_DD = { "button": "defect", "reputation": 'DD' }

    # find two agents and PLAY
    for p in random.choice(agent_set_in_pairs):
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

    return(agents)