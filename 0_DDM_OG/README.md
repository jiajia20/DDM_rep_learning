# Binary Network Game

This is a simple PyIBL model for an extension to an environment of small networkds of multiple players 
of the binary games described in
[Balliet, Tybur and Van Lange, *Functional Interdependence Theory: An Evolutionary Account
of Social Situations*](https://journals.sagepub.com/doi/10.1177/1088868316657965).

## Modified 
**Study** design for binary choice game to be played in disconnected network (pairs), ring network and fully connected networks. Network size is 6.

**Game** provide different pay-off matrix and fifferent network structure of the networked prisoner-dillema like game between paris of networked agents.

**Study** provide 1)6 agent 2)completetly interdepdent pay-off 3)among fully-connected, ring and disconnected(pair) participants

**Study_modified** change the network size from 6 to 12.

**Study_partial** provide partial matching (provide panalty for getting a differen value than those seen before， it also include the identity of the alter into the instance learned 

**Study_partial_feedback** include the palter’s identity, added penalty for seeing different result than expected (aka partial matching) and  also added a discontunted value of alter’s payoff in one’s own payoff

**study_wopp** include participant’s identity but NOT give panalty when the value is not as expected (without the partial matching penalty term)

**study_wopp_feedback** include idenity, no partial matching and included alter’s return.

