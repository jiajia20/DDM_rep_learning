import alhazen
import csv
import math
import pyibl
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import date
from itertools import count
from pprint import pprint
from tqdm import tqdm

NODES = 15
REWIRE = 0.3
ROUNDS = 20 # 100
PARTICIPANTS = 10 # 1000
NETWORKS = "fully_connected,randomly_connected,small_world,lattice,no_network".split(",")

def add_edge(network_matrix, i, j):
    i %= NODES
    j %= NODES
    network_matrix[i][j] = 1
    network_matrix[j][i] = 1

def fully_connected(m):
    for i in range(NODES):
        for j in range(i):
            add_edge(m, i, j)

def randomly_connected(m):
    def is_connected(i=0):
        global visited
        if i == 0:
            visited = set()
        visited.add(i)
        if len(visited) == NODES:
            return True
        for j in range(NODES):
            if i != j and j not in visited and m[i][j]:
                if is_connected(j):
                    return True
        return False
    k = NODES + math.floor(REWIRE * NODES)
    while not is_connected():
        edges = set()
        for i in range(NODES):
            for j in range(NODES):
                m[i][j] = 0
        while len(edges) < k:
            i, j = sorted(random.sample(range(NODES), 2))
            edges.add((i, j))
            add_edge(m, i, j)

def ring(m):
    for i in range(NODES):
        add_edge(m, i, i + 1)

def lattice(m):
    assert NODES > 4
    ring(m)
    for i in random.sample(range(NODES), math.floor(REWIRE * NODES)):
        add_edge(m, i, i + 2)

def small_world(m):
    assert NODES > 6
    ring(m)
    for i in random.sample(range(NODES), math.floor(REWIRE * NODES)):
        add_edge(m, i, random.sample(range(i + 3, NODES + i - 3), 1)[0])

def no_network(m):
    for i in range(math.floor(NODES / 2)):
        add_edge(m, 2 * i, 2 * i + 1)

def network_matrix(kind):
    assert NODES > 2
    result = [[0]*NODES for i in range(NODES)]
    globals()[kind](result)
    return result

def edges(m):
    result = []
    for i in range(NODES):
        for j in range(i + 1, NODES):
            if m[i][j]:
                result.append((i, j) if random.random() < 0.5 else (j, i))
    return result


GAMES = {"independence": {("A", "A"): (5, 5),
                          ("A", "B"): (5, 0),
                          ("B", "A"): (0, 5),
                          ("B", "B"): (0, 0)},
         "interdependence": {("A", "A"): (5, 5),
                             ("A", "B"): (0, 5),
                             ("B", "A"): (5, 0),
                             ("B", "B"): (0, 0)},
         "correspondence": {("A", "A"): (5, 5),
                            ("A", "B"): (0, 0),
                            ("B", "A"): (0, 0),
                            ("B", "B"): (0, 0)},
         "conflict": {("A", "A"): (5, 0),
                      ("A", "B"): (0, 0),
                      ("B", "A"): (0, 0),
                      ("B", "B"): (0, 5)},
         "social_exchange": {("A", "A"): (5, 5),
                             ("A", "B"): (0, 5),
                             ("B", "A"): (5, 0),
                             ("B", "B"): (0, 0)},
         "coordination": {("A", "A"): (5, 5),
                          ("A", "B"): (0, 0),
                          ("B", "A"): (0, 0),
                          ("B", "B"): (5, 5)},
         "high_power": {("A", "A"): (5, 0),
                        ("A", "B"): (5, 0),
                        ("B", "A"): (0, 5),
                        ("B", "B"): (0, 5)},
         "low_power": {("A", "A"): (0, 5),
                       ("A", "B"): (5, 0),
                       ("B", "A"): (0, 5),
                       ("B", "B"): (5, 0)},
}

MAX_SCORE = 0
for d in GAMES.values():
    for t in d.values():
        MAX_SCORE = max(MAX_SCORE, max(t))

PREPOPULATED_VALUE = 1.2 * MAX_SCORE


class NetworkedGameExperiment(alhazen.IteratedExperiment):

    def __init__(self, **kwargs):
        super().__init__(rounds=kwargs.get("rounds", ROUNDS),
                         participants=kwargs.get("participants", PARTICIPANTS),
                         # logfile=f"log-{date.today()}.csv",
                         # csv=True,
                         **kwargs)

    # def prepare_experiment(self, **kwargs):
    #     with self.log as w:
    #         w.writerow(("game,network,participant-cluster,round,"
    #                     "john-player,mary-player,"
    #                     "john-choice,mary-choice,"
    #                     "john-payoff,mary-payoff").split(","))

    def run_participant_prepare(self, participant, condition, context):
        self.agents = [pyibl.Agent(str(i), ["choice", "role"],
                                   default_utility=PREPOPULATED_VALUE)
                       for i in range(NODES)]
        self.net = edges(network_matrix(condition[1]))
        self.game = GAMES[condition[0]]

    def run_participant_run(self, round, participant, condition, context):
        means = defaultdict(float)
        result = []
        for e in random.sample(self.net, len(self.net)): # shuffle
            choices = tuple(self.agents[i].choose(*[{"choice": c, "role": role}
                                                    for c in "AB"])["choice"]
                            for i, role in zip(e, count()))
            means["".join(choices)] += 1 / len(self.net)
            payoffs = self.game[choices]
            means["payoffs"] += sum(payoffs) / (2 * len(self.net))
            for i, p in zip(e, payoffs):
                self.agents[i].respond(p)
            result.append(e + choices + payoffs)
        return (result, means)

    def run_participant_finish(self, participant, condition, result):
        means = []
        with self.log as w:
            for (r, d), i in zip(result, count()):
                # for p in r:
                #     w.writerow(condition + (participant, i) + p)
                means.append(d)
        return means

    def finish_condition(self, condition, result):
        means = [defaultdict(float) for i in range(self.rounds)]
        for sub in result:
            for d, i in zip(sub, count()):
                for k in d:
                    means[i][k] += d[k] / self.participants
        return means

def main():
    print("Alhazen version", alhazen.__version__)
    print("PyIBL version", pyibl.__version__)
    conditions = []
    for g in GAMES:
        for n in NETWORKS:
            conditions.append((g, n))
    result_map = NetworkedGameExperiment(conditions=conditions).run()
    for g, i in zip(GAMES, count()):
        fig, axs = plt.subplots(len(NETWORKS), sharex=True)
        fig.set_figheight(10)
        fig.subplots_adjust(hspace=0.5)
        fig.suptitle(f"{g} game, {PARTICIPANTS} participant clusters")
        for n, j in zip(NETWORKS, count()):
            results = result_map[(g, n)]
            for choices in ["AA", "BB", "AB", "BA"]:
                axs[j].plot(range(1, len(results) + 1),
                            [r[choices]  for r in results],
                            label=choices)
                axs[j].set_title(f"{n}")
            axs[j].set_ylim((0, 1))
            axs[j].plot(range(1, len(results) + 1),
                        [r["payoffs"] / MAX_SCORE for r in results],
                        "k:",
                        label="payoffs")
            ax2 = axs[j].twinx()
            ax2.set_ylim((0, MAX_SCORE))
            ax2.set_yticks([0, MAX_SCORE / 2, MAX_SCORE])
            if j == 0:
                axs[j].legend(ncol=3, fontsize="x-small")
            if j == math.floor(len(NETWORKS) / 2):
                axs[j].set(ylabel="fraction of pairs making this pair of choices")
                ax2.set(ylabel="mean payoff")
            if j == len(NETWORKS) - 1:
                axs[j].set(xlabel="round")
        for ax in axs.flat:
            ax.label_outer()
        fig.savefig(f"graph-{date.today()}-{i:02d}-{g}.pdf")
        fig.clf()


if __name__ == '__main__':
    main()
