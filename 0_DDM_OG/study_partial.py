from datetime import date
from itertools import count
import math
import matplotlib.pyplot as plt
import random

from alhazen import IteratedExperiment
import pyibl

GROUPS = 1000
ROUNDS = 60

PAIRINGS = {
    "disconnected": [[(0, 1), (2, 3), (4, 5)]],
    "ring": [[(0, 1), (2, 3), (4,5)],
             [(1, 2), (3, 4), (0, 5)]],
    "fully-connected": [[(4, 5), (2, 3), (0, 1)],
                        [(3, 5), (2, 4), (0, 1)],
                        [(3, 4), (2, 5), (0, 1)],
                        [(4, 5), (1, 3), (0, 2)],
                        [(3, 5), (1, 4), (0, 2)],
                        [(3, 4), (1, 5), (0, 2)],
                        [(4, 5), (1, 2), (0, 3)],
                        [(2, 5), (1, 4), (0, 3)],
                        [(2, 4), (1, 5), (0, 3)],
                        [(3, 5), (1, 2), (0, 4)],
                        [(2, 5), (1, 3), (0, 4)],
                        [(2, 3), (1, 5), (0, 4)],
                        [(3, 4), (1, 2), (0, 5)],
                        [(2, 4), (1, 3), (0, 5)],
                        [(2, 3), (1, 4), (0, 5)]]}

PAIRS = len(list(PAIRINGS.values())[0][0])
for kind in PAIRINGS.values():
    for pairing in kind:
        assert len(pairing) == PAIRS
NODES = 2 * PAIRS

GAME = {("A", "A"): (5, 5),
        ("A", "B"): (0, 5),
        ("B", "A"): (5, 0),
        ("B", "B"): (0, 0)}

MISMATCH_PENALTY = 0.1
PREPOPULATED_VALUE = 1.05 * max(max(pair) for pair in GAME.values())

pyibl.similarity(True, "opponent")


class Game(IteratedExperiment):

    def __init__(self, **kwargs):
        super().__init__(rounds=kwargs.get("rounds", ROUNDS),
                         participants=kwargs.get("participants", GROUPS),
                         # logfile=f"log-partial-{date.today()}.csv",
                         csv=True,
                         **kwargs)

    def prepare_experiment(self, **kwargs):
        with self.log as w:
            w.writerow(("network,participant cluster,round,"
                        "player 1,player 2,"
                        "player 1 choice,player 2 choice,"
                        "player 1 payoff,player 2 payoff").split(","))

    def run_participant_prepare(self, participant, condition, context):
        self.agents = [pyibl.Agent(str(i), ["choice", "opponent"],
                                        mismatch_penalty=MISMATCH_PENALTY)
                       for i in range(NODES)]
        for a, i in zip(self.agents, count()):
            for o in range(NODES):
                if o != i:
                    for c in "AB":
                        a.populate(PREPOPULATED_VALUE, {"choice": c, "opponent": o})

    def run_participant_run(self, round, participant, condition, context):
        result = 0
        for p in random.choice(PAIRINGS[condition]):
            choices = tuple(self.agents[i].choose(*[{"choice": c, "opponent": j}
                                                    for c in "AB"])["choice"]
                            for i, j in zip(p, reversed(p)))
            if choices == ("A", "A"):
                result += 1 / (PAIRS * GROUPS)
            payoffs = GAME[choices]
            with self.log as w:
                w.writerow([condition, participant, round] + list(p) + list(choices) + list(payoffs))
            for i, j in zip(p, count()):
                self.agents[i].respond(payoffs[j])
        return result

    def finish_condition(self, condition, results):
        return [sum(r[i] for r in results) for i in range(self.rounds)]


def main():

    exp = Game(conditions=list(PAIRINGS.keys()))
    results = exp.run()
    for c in exp.conditions:
        plt.plot(range(1, exp.rounds + 1), results[c], label=c.replace("-", " "))
    plt.title(f"with identity, limited information, {GROUPS:,d} groups of {NODES:d} participants each,\nmismatch={MISMATCH_PENALTY}")
    plt.ylim(0, 1)
    plt.ylabel("fraction coöperating")
    plt.xlabel("round")
    plt.legend()
    # plt.show()
    plt.savefig(f"with-identity-partial-{int(MISMATCH_PENALTY*10):03}.pdf")


if __name__ == '__main__':
    main()
