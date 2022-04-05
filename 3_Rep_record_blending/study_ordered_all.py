import pyibl
import random
import csv
from datetime import date
import pandas as pd

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

GROUPS = 1
ROUNDS = 100
NODES = 6

GAME = {('cooperate', 'cooperate'): (5, 5),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (0, 0)} 

def record_activation(df):
    agent_0_activation = []

    for i in range(len(df)):
        #I need to fix this manually
        c_ins = df.iloc[i][0]['activations']
        d_ins = df.iloc[i][1]['activations']
        #utility, rep, activation & retrival prob
        c_ins_1_u = None
        c_ins_1_r = None
        c_ins_1_a = None
        c_ins_1_rp = None

        c_ins_2_u = None
        c_ins_2_r = None
        c_ins_2_a = None
        c_ins_2_rp = None

        d_ins_1_u = None
        d_ins_1_r = None
        d_ins_1_a = None
        d_ins_1_rp = None

        d_ins_2_u = None
        d_ins_2_r = None
        d_ins_2_a = None
        d_ins_2_rp = None


        if len(c_ins)== 1:
            #utility, rep, activation, retrival
            c_ins_1_u = c_ins[0]['attributes'][0][1] #utility
            c_ins_1_r = c_ins[0]['attributes'][2][1] #rep
            c_ins_1_a = c_ins[0]['activation'] #activation
            c_ins_1_rp= c_ins[0]['retrieval_probability'] #retrival

        elif len(c_ins)== 2:
            c_ins_1_u = c_ins[0]['attributes'][0][1] #utility
            c_ins_1_r = c_ins[0]['attributes'][2][1] #rep
            c_ins_1_a = c_ins[0]['activation'] #activation
            c_ins_1_rp= c_ins[0]['retrieval_probability'] #retrival

            c_ins_2_u = c_ins[1]['attributes'][0][1]
            c_ins_2_r = c_ins[1]['attributes'][2][1]
            c_ins_2_a = c_ins[1]['activation']
            c_ins_2_rp= c_ins[1]['retrieval_probability']

        if len(d_ins)== 1:
            #utility, rep, activation, retrival
            d_ins_1_u = d_ins[0]['attributes'][0][1]
            d_ins_1_r = d_ins[0]['attributes'][2][1]
            d_ins_1_a = d_ins[0]['activation']
            d_ins_1_rp= d_ins[0]['retrieval_probability']

        elif len(d_ins)== 2:
            d_ins_1_u = d_ins[0]['attributes'][0][1]
            d_ins_1_r = d_ins[0]['attributes'][2][1]
            d_ins_1_a = d_ins[0]['activation']
            d_ins_1_rp= d_ins[0]['retrieval_probability']

            d_ins_2_u = d_ins[1]['attributes'][0][1]
            d_ins_2_r = d_ins[1]['attributes'][2][1]
            d_ins_2_a = d_ins[1]['activation']
            d_ins_2_rp= d_ins[1]['retrieval_probability']

        agent_0_activation.append([i,len(df.iloc[i][0]['activations']), 
        c_ins_1_u, c_ins_1_r,c_ins_1_a,c_ins_1_rp,
        c_ins_2_u, c_ins_2_r,c_ins_2_a,c_ins_2_rp,
        len(df.iloc[i][1]['activations']),
        d_ins_1_u, d_ins_1_r,d_ins_1_a,d_ins_1_rp,
        d_ins_2_u, d_ins_2_r,d_ins_2_a,d_ins_2_rp,
        ])
    
    df_activation = pd.DataFrame(agent_0_activation)

    df_activation.columns = ["step","num_c_instance",
    "c_ins_1_utility", "c_ins_1_rep","c_ins_1_activation","c_ins_1_retP",
    "c_ins_2_utility", "c_ins_2_rep","c_ins_2_activation","c_ins_2_retP",
    "num_d_instance",
    "d_ins_1_utility", "d_ins_1_rep","d_ins_1_activation","d_ins_1_retP",
    "d_ins_2_utility", "d_ins_2_rep","d_ins_2_activation","d_ins_2_retP"
    ]

    
    return(df_activation)






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

    


    agent_0_df_list = []
    agent_0_activation_list = []
    #first assign group number (
    # e.g. 10 groups means 10 different group of agents assigned to each condition) 
    for group_number in range(GROUPS):
        #condition = PAIRINGS.keys()
        
        #then assign condition as in network layout
        #the condition are keys of PAIRING, i.e. disconnected, fully connected, ring
        
        for condition in PAIRINGS.keys():
            random.shuffle(PAIRINGS[condition])   
            #create agents
            agents = [pyibl.Agent(str(name),["button", "reputation"], default_utility=5 ) for name in range(NODES) ]

            ######currently only for agent[0]
            agents[0].details = True

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

            df = pd.DataFrame(agents[0].details)

            #record the belnding value
            agent_0_list = []
            for i in range(len(df)):
                agent_0_list.append([i, df.iloc[i][0]['button'],df.iloc[i][0]['reputation'],df.iloc[i][0]['blended'],
                df.iloc[i][1]['button'],df.iloc[i][1]['reputation'],df.iloc[i][1]['blended']])
            #df.iloc[2][1] first iloc[] for row, second [] for column

            df_agent0 = pd.DataFrame (agent_0_list)
            df_agent0.columns = ["round","cooperate","cooperate_rep", "c_blending_value",
                                    "defect", "defect_rep", "d_beldning_value"]          
            
            df_agent0.insert(0, "network", [condition for i in range(len(df_agent0))])
            df_agent0.insert(0, "participant_cluster", [group_number for i in range(len(df_agent0))])

            #record activation
            df_agent_0_activation = record_activation(df)

            df_agent_0_activation.insert(0, "network", [condition for i in range(len(df_agent_0_activation))])
            df_agent_0_activation.insert(0, "participant_cluster", [group_number for i in range(len(df_agent_0_activation))])


            #record in 
            agent_0_df_list.append(df_agent0)
            agent_0_activation_list.append(df_agent_0_activation)
            
    
    merged_df = pd.concat(agent_0_df_list)
    merged_activation = pd.concat(agent_0_activation_list)

    #currently the csv file record the change of belnding value of agent 0
    merged_df.to_csv(f"agent0-blending-log-{date.today()}.csv", sep=',')
    merged_activation.to_csv(f"agent0-activation-log-{date.today()}.csv", sep=',')

    return()

