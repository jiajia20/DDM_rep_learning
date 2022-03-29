# Reputation_learning_in_loop
This version I rewrite the looping code so that experiment no longer run in parallel but in four loop one within the other. 

There's two python file
**study_ordered** is the 6-agent version

**study_order_large** is the 12-agent version

## Loops

### 1 - steps
` for p in (PAIRINGS[condition]):`
A *step** is the inner most loop. A step takes two agent to interact with each other. During the step, each agent:

1) learn each other and their own reputation. 
In the current model, the reputation is defied as whether the actor chooses to cooperate or defect in the last step with whoever last they play with. Cooperat = **G**ood reputation, Defect = **B**ad reputation.

2) The reputation combo of (ego - alter) (i.e GG, GB,BG, BB) will then be used to led the agent to choose to cooperate or defect with their current pairs.

3) Based on what they and their alter choose in the current step, they got the pay-off determined by the `GAME` payoff matrix. 

4) The agents then respond to the pay-off
In the current model, the utlity is exactly the same as the pay-off matrix specified. Agent can also choose to include their neighbor’s payoff in their utility fouction (i.e. being somewhat altruistic)
 
Each paring have to play a step, a paring come from the agent combination of each different condition

### 2 - simulation rounds
`for simulation_rounds in range(ROUNDS):`
A **round** in the second inner loop. In a round, everyone play once and only once with its neighbor on their social graph

### 3 - condition
`for condition in PAIRINGS.keys():`
The **condition** is the second outter most loop. A condition means creating a set of new agents. The agents are connected to each other either in

**disconnected** condition - pair-wise, each agent connect to only one other agent, no overlap, 

**ring** condition - each agent connect with two other agent, the social graph look like a ring

**fully-connected** condition - each agents connect to all the other agents in the graph.

In this step, new ibl agents are create for each condition. One can imagine this to be having between-subject test among the three sets of agents. In the current game there are either 6 or 12 agents in each condition. 

## 4 - Groups
`for group_number in range(GROUPS`

The gourp is the out-most loop. To makesure reproducibility, we included multile group (usually 100) for each condition, and average the number of each monitored variable across groups to reduce random noice. 
Thus the number of iteration of the simulation is determined by numbers of condition (3 - disconnected, ring, fully-connected) times the number of group (usually 100)