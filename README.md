# GA-Tetris

The project aims to control an artificial intelligence (AI) in playing games of Tetris to achieve higher scores than a human could reach. <br><br>
As each Tetromino spawns, the AI will generate all the possible ending positions of the block and numerically assign a value to each one, based on how beneficial or penalizing the position is. The AI will take into account: the number of void blocks or gaps created, the overall height of the blocks on the board, the number of ledges created, the number of lines to be cleared, etc. Each metric is assigned a reward or penalty value, which increases the more significant the occurrence is, and contributes to the overall mark of each position. <br><br>
Once the program has calculated all possible positions, it will select the most beneficial one, evidenced by its higher score among others, and perform the moves necessary to reach the desired ending position for the Tetromino. <br> <br>

<div style="position: absolute; bottom: 5px; right: 5px; color: lightgray; font-size: small;">Code adapted from Bofei Wang</div>
