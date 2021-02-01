# Machine Learning Cellular Automata

## Introduction to Cellular Automata
We focus on outer totalistic generations of two-dimensional Cellular Automata. They consist of a two-dimensional grid of cells, which live, die, or are in a “dying” transition date depending on a set of rules. Specifically, the cells are updated according to their previous values, and the sum of the values of the other cells in the neighborhood. We decided to use Moore neighborhood for the update rules, which are the surrounding eight cells of a center cell. An alternative would be Neumann neighborhood, which only includes four cells. Rules are classified as **boring** if they lead to a pattern which is static noise with no discernable patterns moving across the screen. For this project, we define **interesting** rules specifically as those that have clear gliders (small patterns that move across the grid) with some individual characteristics. Under most circumstances, it is impossible to tell whether a rule is interesting or boring just by looking at the parameters. A user would have to randomly go through thousands of random rules before finding an interesting one. Even more daunting, under the assumption that we use a Moore neighborhood and a maximum of 10 possible states, there are 2<sup>9</sup> survival rules, 2<sup>9</sup> born rules, and 2<sup>10</sup> states, which leads to a total of 2<sup>28</sup> combinations of rules. 

## Data Collection Pipeline
To obtain boring rules, we manually went through random examples, and collected rules that died out immediately or generated static noise or boring non-glider patterns. For interesting rules, we used Cellular Automata Rules Lexicon, and examples provided in Visions of Chaos and only recorded those with gliders. We ended up with 105 boring and 35 interesting sets of rules. 

We used the CA Generation Algorithm to generate frames and create images. Next, we applied data augmentation due to the limited number of rules that we identified. We reused the boring rules 10 times, and the interesting rules 30 times with different initial configuration. We generated 140 images for each of the patterns. 

Then we did image stitching. We chose to use frames from 100 to 108. Because when we were running examples, we noticed that this is roughly when the patterns were all apparent. Each pattern corresponds to one stitched together 3 by 3 image. We assembled training data with a 50% interesting and 50% boring split. 

## Training with Convolutional Neural Network 
We tuned the hyperparameters and found out that batch normalization and more data inclusion greatly improved the accuracy of the Neural Network. Without batch normalization, the testing accuracy was only 65.08%. After batch normalization and dropout, we were able to achieve 93.44% training accuracy and 84.12% testing accuracy on the testing set with 10% interesting data. The test recall is 100%, indicating every interesting configuration has been correctly labeled as such. 



https://docs.google.com/document/d/1W9Okl6FagUjE5KHXleISY4QuIS9L3nS07TFt2cFl274/edit


Report link: https://docs.google.com/document/d/1myNg7W3ulfQDqOqyJhoGctVLsFYNC6vusfE-MiP15NE/edit

Additional resources: https://docs.google.com/document/d/1OJUDrcS4e6k4R0dp6ehwz5xQAVcQ2ZfuoSWXfg6luRU/edit
