from datetime import date
from itertools import count
import math
import matplotlib.pyplot as plt
import random

from alhazen import IteratedExperiment
import pyibl

GROUPS = 1000
ROUNDS = 100

PAIRINGS = {
    "disconnected": [[(0, 1), (2, 3), (4, 5,),(6, 7),(8, 9),(10, 11),(12, 13),(14, 15)]],
    "ring": [[(0, 1), (2, 3), (4,5),(6, 7),(8, 9),(10, 11),(12, 13),(14, 15)],
             [(1, 2), (3, 4),(5, 6),(7, 8),(9, 10),(11, 12),(13, 14),(15,0)]],

    "fully-connected": [[(0, 1), (2, 3), (4,5),(6, 7),(8, 9),  (10, 11),(12, 13),(14, 15)],
                        [(0, 2), (2, 4), (4,6),(6, 8),(8, 10), (10, 12),(12, 14),(14, 1)],
                        [(0, 3), (2, 5), (4,7),(6, 9),(8, 11), (10, 13),(12, 15),(14, 2)],
                        [(0, 4), (2, 6), (4,8),(6, 10),(8, 12),(10, 14),(12, 1),(14, 3)],
                        [(0, 5), (2, 7), (4,9),(6, 11),(8, 13),(10, 15),(12, 2),(14, 4)],
                        [(0, 6), (2, 8), (4,10),(6,12),(8, 14),(10, 1),(12, 3),(14, 5)],
                        [(0, 7), (2, 9), (4,11),(6, 13),(8,15),(10, 2),(12, 4),(14, 6)],
                        [(0, 8), (2, 10),(4,12),(6, 14),(8, 1),(10, 3),(12, 5),(14, 7)],
                        [(0, 9), (2, 11),(4,13),(6, 15),(8, 2),(10, 4),(12, 6),(14, 8)],
                        [(0, 10), (2,12),(4,14),(6, 1),(8, 3), (10, 5),(12, 7),(14, 9)],
                        [(0, 11), (2,13),(4,15),(6, 2),(8, 4), (10, 6),(12, 8),(14, 10)],
                        [(0, 12), (2,14),(4,1),(6, 3),(8, 5),  (10, 7),(12, 9),(14, 11)],
                        [(0, 13), (2,15),(4,2),(6, 4),(8, 6),  (10, 8),(12, 10),(14, 12)],
                        [(0, 14), (2, 1),(4,3),(6, 5),(8, 7),  (10, 9),(12, 11),(14, 13)]]
    }

PAIRS = len(list(PAIRINGS.values())[0][0])
for kind in PAIRINGS.values():
    for pairing in kind:
        assert len(pairing) == PAIRS
NODES = 2 * PAIRS

GAME = {('cooperate', 'cooperate'): (5, 5),
        ('cooperate', 'defect'): (0, 5),
        ('defect', 'cooperate'): (5, 0),
        ('defect', 'defect'): (0, 0)} #new code

PREPOPULATED_VALUE = 1.05 * max(max(pair) for pair in GAME.values())


class Game(IteratedExperiment):

    def __init__(self, **kwargs):
        super().__init__(rounds=kwargs.get("rounds", ROUNDS),
                         participants=kwargs.get("participants", GROUPS),
                         logfile=f"log-{date.today()}.csv",
                         csv=True,
                         **kwargs)

    def prepare_experiment(self, **kwargs):
        with self.log as w:
            w.writerow(("network,participant cluster,round,"
                        "player 1,player 2,"
                        "player 1 choice,player 2 choice,"
                        "player 1 rep,player 2 rep," #new code
                        "player 1 payoff,player 2 payoff").split(","))

    def run_participant_prepare(self, participant, condition, context):
        self.agents = [pyibl.Agent(str(i), ["button", "reputation"],default_utility=PREPOPULATED_VALUE)
                       for i in range(NODES)]
        

    def run_participant_run(self, round, participant, condition, context):
        result = 0
        last_moves = [None]*NODES
        #initialize options
        cooperate_CC = { "button": "cooperate", "reputation": 'CC' }
        cooperate_CD = { "button": "cooperate", "reputation": 'CD' }
        cooperate_DC = { "button": "cooperate", "reputation": 'DC' }
        cooperate_DD = { "button": "cooperate", "reputation": 'DD' }
        defect_CC = { "button": "defect", "reputation": 'CC' }
        defect_CD = { "button": "defect", "reputation": 'CD' }
        defect_DC = { "button": "defect", "reputation": 'DC' }
        defect_DD = { "button": "defect", "reputation": 'DD' }

        #initialize first move 
        for n in range(0,16): #0-15
            globals()[f'last_move_{n}'] = random.choice('CD')

        for p in random.choice(PAIRINGS[condition]):
            # figure which opponent
            a = self.agents[p[0]]
            b = self.agents[p[1]]

            # also find their last move
            a_last = globals()[f'last_move_{p[0]}']
            b_last = globals()[f'last_move_{p[1]}']
            last_round = a_last+b_last

            # make new choice based on past repuation of both participant
            if last_round == 'CC':
                result_a = a.choose(cooperate_CC, defect_CC)
                result_b = b.choose(cooperate_CC, defect_CC)
            elif last_round == 'CD':
                result_a = a.choose(cooperate_CD, defect_CD)
                result_b = b.choose(cooperate_CD, defect_CD)
            elif last_round == 'DC':
                result_a = a.choose(cooperate_DC, defect_DC)
                result_b = b.choose(cooperate_DC, defect_DC)
            else:
                result_a = a.choose(cooperate_DD, defect_DD)
                result_b = b.choose(cooperate_DD, defect_DD)

            # update result
            pair_result = (result_a['button'],result_b['button'])

            if pair_result == ('cooperate', 'cooperate'):
                a.respond(5)
                b.respond(5)
                #result += 1 / (PAIRS * GROUPS)
                a_last = 'C'
                b_last = 'C'
                
            elif pair_result == ('cooperate', 'defect'):
                a.respond(0)
                b.respond(5)
                a_last = 'C'
                b_last = 'D'
            elif pair_result == ('defect', 'cooperate'):
                a.respond(5)
                b.respond(0)
                a_last = 'D'
                b_last = 'C'
            else:
                a.respond(0)
                b.respond(0)
                a_last = 'D'
                b_last = 'D'
            
            globals()[f'last_move_{p[0]}'] = a_last
            globals()[f'last_move_{p[1]}'] = b_last

            payoffs = GAME[pair_result]
            with self.log as w:
                w.writerow([condition, participant, round] + list(p) + list(pair_result)+ list(last_round) + list(payoffs))
            
            #if choices == ("A", "A"):
            
            # record somewhere what each player did this time for consulting next time
            # last_moves[p[0]] = choices[p[0]]
            # last_moves[p[1]] = choices[p[1]]
            
            # for i, j in zip(p, count()):
            #     self.agents[i].respond(payoffs[j])
        return #result

    def finish_condition(self, condition, results):
        return #[sum(r[i] for r in results) for i in range(self.rounds)]


def main():

    exp = Game(conditions=list(PAIRINGS.keys()))
    exp.run()
    #results = exp.run()
    # for c in exp.conditions:
    #     plt.plot(range(1, exp.rounds + 1), results[c], label=c.replace("-", " "))
    # plt.title(f"no identity, {GROUPS:,d} groups of {NODES:d} participants each")
    # plt.ylim(0, 1)
    # plt.ylabel("fraction cooperating")
    # plt.xlabel("round")
    # plt.legend()
    # # plt.show()
    # plt.savefig("no-identity.pdf")

if __name__ == '__main__':
    main()
