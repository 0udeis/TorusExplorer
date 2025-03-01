# TorusExplorer

A simulation for online graph explorations on tori.

This project was used for the bachelor's thesis Exploration of Grid-Like
Graphs with Predictions. We consider the cyclic graph exploration problem: The explorer must visit all vertices of an unweighted, undirected graph $G=(V, E)$ and return to the starting vertex $v_0$. In our case, $G$ will be a cylindrical ladder or a torus. We consider the fixed-graph scenario, in which all vertices of $G$ have a unique label. The explorer has no initial knowledge of $G$, except for its general shape. In particular, it does not know its dimensions. Upon arriving at a vertex, the explorer learns all its incident edges and neighboring vertices.  Additionally, the explorer may take trusted or untrusted advice, which points it to the vertex it should visit next for an optimal solution.

This project can be used to create tori and simulate the explorer.
The code was written using ChatGPT.

## trusted.py

This program was used for simulating explorations on tori with trusted advice. An optimal solution for the cyclic graph exploration problem on tori will always form a Hamiltonian cycle. Therefore, in trusted.py, an explorer cannot visit a vertex multiple times.

### How it works

Run trusted.py. In the two text fields, enter $m$ and $n$. They must be integers with $m\leq 13, n\leq 24$. You can use the arrow keys to navigate to the vertex in which you want to start. Press space for marking the starting vertex $v_0$. Now, using the arrow keys will paint the path you take. You can see the visited vertices in blue and see the familiar and newly familiar vertices as black or orange dots. If you want to undo a step, press backspace.

### Known Issues

- The size of $m$ and $n$ cannot be larger than 13 or 24 respectively, because it will not fit on the canvas.
- Using backspace to undo a step might also remove a digit in the entry fields. Similarly, when using the arrow keys to navigate the explorer, the cursor in the text fields also moves.
- No vertex can be visited multiple times. This includes $v_0$. It is therefore not possible to actually finish an exploration by returning to $v_0$.

## untrusted.py

This program was used for simulating explorations on tori with untrusted advice. The main difference is that visiting a vertex multiple times is now possible.

### How it works

Run untrusted.py. Enter $m, n$ as above. Use the arrow keys to navigate to the vertex you want to start and press space. Unlike before, the starting vertex will be shown in green. Use the arrow keys to explore the torus. Visiting a vertex multiple times will make it a darker shade of blue (or green in the case of $v_0$). Familiar and newly familiar vertices are shown as before.

### Known Issues

- As for trusted.py, $m, n$ cannot be larger than 13 or 24, respectively.
- Using backspace for undoing an action has not been implemented. Instead, you need to restart the exploration.
