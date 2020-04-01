# B551 Assignment 1: Searching

**Submitted by:** Sidharth Vishnu Bhakth, Madhura Bartakke, Shreyas Bhujbal / svbhakth-mabartak-sbhujbal

**Part 1: The Luddy puzzle**

**Search Abstraction:** The program uses an A* search algorithm which finds the optimal solution to the problem. The algorithm is implemented with a priority queue with a cost function and a heuristic function. The state with the lowest combination of cost + heuristic will be popped from the priority queue and used to find the optimal path.

We have used the number of moves as the cost function and the number of misplaced tiles at each state as the heuristic function. We had also implemented Manhattan distance of each state from the goal state as a heuristic function. However, we decided to use the former since for each state closer to goal, the number of misplaced tiles reduces. Since we expand the nodes with the lowest heuristic (since our cost for each set of states gets incremented by 1, the heuristic determines the order in which we expand the nodes), the algorithm always considers the "cheapest" path from a given set of states. Hence, the heuristic amy be considered admissible.

**Set of valid states:** For a given state, the set of valid state is the next state with the lowest sum of cost and heuristic functions.

**Cost function:** We have used the number of moves from initial state as the cost function.

**Heuristic function:** The number of misplaced tiles for each state is the heuristic function.

**Initial State:** Initial state is the starting board given as input to the program.

**Goal State:** The goal state is the solved state of the puzzle.

**References:**

1. MIT OCW 6.034 Artificial Intelligence: Lecture 5: Search: Optimal, Branch and Bound, A* - https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-034-artificial-intelligence-fall-2010/lecture-videos/lecture-5-search-optimal-branch-and-bound-a/
2. Introduction to A* - http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html
3. A* search - https://brilliant.org/wiki/a-star-search/


**Part 2: Road trip!**

In this problem, we were given dataset of major highways segments of United States (and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits. We were also given dataset of cities and towns with corresponding latitude-longitude positions. The job is to implement algorithms that find good driving directions between pairs of cities and cost funtion given by the user.Cost-function is one of:-segments tries to find a route with the fewest number of turns (i.e. edges of the graph). 
-distance tries to find a route with the shortest total distance.
-time tries to find the fastest route, for a car that always travels at the speed limit.
-mpg tries to find the most economical route, for a car that always travels at the speed limit and whose mileage per gallon (MPG) is a function of its velocity (in miles per hour).

**Functions used:**

**Successor**
Finds and returns successor rows from road_segment.txt of the given state

**Heuristic**
Returns heuristic value for the given 2 pairs of longitudes and latitudes. 

**check_valid_names**
Checks whether the given names of cities is valid or not. It looks for the names of the cities in city-gps.txt file

**return_city**
This function takes the state(row from the road_segment.txt file) and returns the next city given in the file

**solve_multiple**
This functions implements the algorithm on the given inputs and returns the solution in the given format.

**Description:**
We take the input in the format as mentioned above. For this problem, we have used the A* algorithm. Initially, we are trying to implement a heuristic. This heuristic would find the distance between two cities using the haversine formula by taking the latitude and the longitude values. We didnt use the heuristic in our final solution because not all the cities mentioned in the road_segments.txt file exist in city-gps.txt file. So we decided to drop the heuristic function and considered the path taken so far for optimising the solution. We wrote similar 4 codes (as 'if' conditions) each for 4 types of costs namely mpg, segments, distance, time. We used the PriotityQueue module to implement a priority.


**Part 3: Choosing a team**

**Objective** - In this problem, we need to assemble team of robots. SICE has the set of robots to choose from. Each robot *i* will have an hourly rate *Pi* and skill level *Si*. The problem is to select team of robots such that their sum has the greatest skill but with a fixed budget.

**Working** – The given problem uses Dynamic Programming which examines all possible ways to solve the problem and give the best solution. This approach uses function comb which stores all the combinations of the robots. Function approx_solve takes all the combinations and compares each elements with the budget. If the element has cost less than the budget, it validates that element else discards it. In this way it checks all the combinations and gives the best combination back.

**Set of valid states:**  Valid states are all the combinations of states for a given data.

**Goal State:** Goal state is set of all robots such that total cost is within the budget and skill is maximum.

**References:**

1. Knapsack using Dynamic Programming - http://www.es.ele.tue.nl/education/5MC10/Solutions/knapsack.pdf

