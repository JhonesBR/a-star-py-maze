# a-star-py-maze
## Maze solution finder using different algorithms
This was a project we developed for SI702 (Artificial Intelligence at Unicamp) throughout the semester. Our idea was to develop and visualize an algorithm using artificial intelligence to solve a maze problem, representing especially A* differentiating an admissible and not admissible heuristic.

## Credits
- João Vitor Oliveira de Melo ([JhonesBR][jhones])
- Pedro Henrique Carreto Morais ([Smoow][pedro])
- Diogo Silveira dos Santos ([dyokinn][diogo])
- João Vitor Izael Souza ([izzy-el][izael])
- Luiz Otávio de Oliveira Silva ([LuizOtavios][luiz])
- João Pedro Coelho de Sousa ([ZakisKuniklo][coelho])
- Carlos Eduardo de Andrade Pereira ([m4nko][manco])

## Basic controls and usage
To start the solving you can select one of the algorithms using the keys from 1 to 7 (more info below) and once the algorithm was selected it will start solving (if an automatic algorithm was chosen) and when the end is found a message box will pop up showing how many moves were necessary to reach the end.

We also generate the maze, so if you want to generate another maze you can do it pressing 'G', and reset it (without changes) with 'R'. Also press 'Q' to quit or close the window.

The maze size and window height in pixels can be changed below the comment "Parameters".
If you want to add a delay between steps you can change the top trackbar (representing the delay in ms)

## Algorithms (and keybinds to activate then)
### 1- Manual Search
Not an algorithm, but in manual search you can try to find a solution using the keys 'W', 'A', 'S' and 'D' to control the cursor
### 2- Random Search
Not exactly an algorithm too, in random mode, the cursor will move randomly in a possible direction (respecting the boundaries) and try to find the end of the maze, since it can take a long time you can stop it by pressing 'S' (or holding it to work)
### 3- Depth-first Search (DFS)
Depth-first algorithm will try to find the solution to the maze by exploring as far as possible along each branch before backtracking (backtracking implemented).
### 4- Breadth-first Search (BFS)
Breadth-first algorithm will try to find the solution to the maze by exploring all nodes at the present depth prior to moving on to the nodes at the next depth level.
### 5- Greedy Best-first Search
The Greedy BFS chooses the node to move based on the minimum heuristic (Euclidean distance from the current position to the end), without considering the cost. 
### 6- A* Search
The A* algorithm chooses the node to move based on the minimum heuristic (Euclidean distance from the current position to the end) and the cost to move to the nodes, in the final it can backtrack all the visited nodes going to the nodes with lower cost to get the optimal path. In this case the heuristic is admissible because its lower than the actual cost, since the Euclidean distance by definition is the closest distance to two points. Once the A* finds the path it will start a Flask server from Dash at 127.0.0.1:8050, you can visualize the graph representation of the solution.
### 7- A* Search (Wrong)
The difference of this algorithm is that it implements a wrong heuristic (in our case the Euclidean distance added to a noise based on the height of the maze), making it find the path, but not always the optimal one. Once the A* with the wrong heuristic finds the path it will start a server too, but in port 8051 (127.0.0.1:8050), showing the graph representation of the solution.

## License
MIT

   [diogo]: <https://github.com/dyokinn>
   [izael]: <https://github.com/izzy-el>
   [jhones]: <https://github.com/JhonesBR>
   [luiz]: <https://github.com/LuizOtavios>
   [pedro]: <https://github.com/Smoow>
   [coelho]: <https://github.com/ZakisKuniklo>
   [manco]: <https://github.com/m4nko>