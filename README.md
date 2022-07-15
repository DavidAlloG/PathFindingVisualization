# Project: Shortest Path Finder
## Author: David García Allo
## Date: 09/07/2022

### Description: 
Returns the shortest path between 'O' (start) and 'X' (end) if it has a solution and returns None if it hasn't.
Also shows the intermediate steps in a terminal screen that remains opened till we press any key on that terminal screen.

### Observations: 
It is a great idea to include the path on the Queue and not only the neighbors like I did on the first attempt.
Also the module curses is a good option to show the intermediate paths because we can clear it and print the next one after
a sleep time, if we used the print commands we will have a lot of outputs and it won't be that easy to visualize.

### Posible improvements: 
1. Adapt it to be showed on a GUI and the posibility of creaete start, end and wall points with onClick functions.
2. Insert an option that allows us to introduce different search algorithms.
