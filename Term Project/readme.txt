To run the game:
-Run Game.py


To use the game:
Practice mode -
	- Click on a tile adjacent to the blank for them to swap positions
	- All other buttons are intuitive
	- Solve button may take anywhere between 0 and 60 seconds to create the solution, since it is optimized (I'd say 90% are solved within 5 secs, though)
Race Mode -
	-Fairly intuitive, player1 completes their board, screen will show before player2's turn, player2 completes board, and then there is a results screen
Maze Mode - 
	- If there is an available path, use WASD to move between tiles
	- Navigate to the mousehole before time/moves run out (1 move = 1 movement of a tile)
	- Level 2: collect all cheese before proceeding to mousehole
	- Level 3: Avoid mousetraps while proceeding to mousehole
	- Level 4: Avoid moving cats while proceeding to mousehole
	- Level 5/random: do all of the above
	- Levels are locked until previous are completed, to work around this, change self.maxLevel var in Maze.py to 5 in order to be able to access all levels
Uploader -
	- Move any .png or .jpg file to the "images" folder in the project
	- Type in the name of the file, including the .png or .jpg, and press enter (e.g. dog.jpg)
