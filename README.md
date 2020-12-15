# ML Cellular Automata
We focus on outer totalistic generations of two-dimensional Cellular Automata. They consist of a two-dimensional grid of cells, which live, die, or are in a “dying” transition date depending on a set of rules. Specifically, the cells are updated according to their previous values, and the sum of the values of the other cells in the neighborhood. We decided to use Moore neighborhood for the update rules, which are the surrounding eight cells of a center cell. An alternative would be Neumann neighborhood, which only includes four cells. Rules are classified as **boring** if they lead to a pattern which is static noise with no discernable patterns moving across the screen. For this project, we define **interesting** rules specifically as those that have clear gliders (small patterns that move across the grid) with some individual characteristics. Under most circumstances, it is impossible to tell whether a rule is interesting or boring just by looking at the parameters. A user would have to randomly go through thousands of random rules before finding an interesting one. Even more daunting, under the assumption that we use a Moore neighborhood and a maximum of 10 possible states, there are 2<sup>9</sup> survival rules, 2<sup>9</sup> born rules, and 2<sup>10</sup> states, which leads to a total of 2<sup>28</sup> combinations of rules. 


https://docs.google.com/document/d/1W9Okl6FagUjE5KHXleISY4QuIS9L3nS07TFt2cFl274/edit


Final Paper document website: https://docs.google.com/document/d/1myNg7W3ulfQDqOqyJhoGctVLsFYNC6vusfE-MiP15NE/edit
