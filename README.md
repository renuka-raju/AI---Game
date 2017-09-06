# AI---Game

Adversarial Constraint Satisfaction by Game-tree Search
Python version 3.5 

The map coloring game obeys the following rules:
1. There are two players, Player 1 and the opponent Player 2. Each player takes
turns as in chess or tic-tac-toe. That is, Player 1 takes a move to color a node,
then Player 2, then back to Player 1 and so forth. In the game, you could
assume Player 1 will always start first (i.e. Player 1 is the MAX player, Player 2
is the MIN player).
2. The players can only color neighbors of nodes that have already been colored
in the map. Adjacent nodes could not have the same color.
3. The score of each player is defined as the total sum of weights of their colored
nodes.
4. The terminal state of the game is that no more nodes could be colored in the
map based on rule 2. It could be either all nodes in the map have been
colored, or no possible assignment could be made according to rule 2.
1 Brown, K. N., Little, J., Creed, P. J., & Freuder, E. C. (2004). Adversarial Constraint Satisfaction by Game-Tree
Search. In ECAI (pp. 151–155). Retrieved from
http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0151.pdf
5. The evaluation function of the colored map state could be defined as
Score_Player1 – Score_Player2. The leaf node values are always calculated
from this evaluation function. Although there might be a better evaluation
function, you should comply with this rule for simplicity.
Node Expanding rule in alpha-beta pruning algorithm:
When expanding a node in the game tree (i.e. choosing an action), you need to
expand first based on the alphabetical order of the state name, and then based on
the color name (if state names are equal). For example, if you have the (state, color)
pair (CA,G) and (Q,R) , you need to first expand (CA,G).And If you have the pair
(CA,G) and (CA,R), you need expand (CA,G) first.

Pass the input file as a command line argument