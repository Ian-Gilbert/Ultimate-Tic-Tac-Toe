# Ultimate Tic Tac Toe
This is a game of Ultimate Tic Tac Toe, written in python. The GUI is created using PyGame.

<p align="center">
	<img src="Images/Completed Board.png" width=50%></img>
</p>

## How To Play
On the surface, ultimate tic tac toe is the same as the standard game: there are nine squares arranged in a 3x3 grid which can each be marked as either an 'X' or an 'O', and three in a row wins the game. Unlike the original game, however, you cannot simply mark a square as 'X' or 'O'. Instead, each square consists of an additional tic tac toe game, which must be won to mark the big square. The overall board is called the 'global board', and the smaller boards are called 'local boards'. The game is won when a player wins three local boards in a row.

On the first turn, Player 'X' can choose any square in any local board they like. From then on, however, the next move will be determined in part by the previous player's move. For example, if Player 'X' plays in the bottom left square of their local board, Player 'O' must then make their next move somewhere in the bottom left local board. This will then determine which local board Player 'X' must play in, and so on. This creates interesting situations in which you may purposefully not win a local board for fear of placing your opponent in an even better position.

<p align="center">
	<img src="Images/First Move.png" width=50%></img>
</p>

**_Important Note:_** Each local board can be won, lost, or drawn (meaning every space is used up, there is no forecasting a draw), at which point no more moves may be made on that board. If a player is sent to such a board, they may then play in any open board they choose (this is something to avoid). Other implementations of the game allow you to play in a local board that has already been won, however this leads to an unbeatable strategy, as described in [this video](https://www.youtube.com/watch?v=weC1pAeh2Do).

For more information about the game, check out [this link](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

For an online version of the game, check out [CreativityGames](http://ultimatetictactoe.creativitygames.net/) or [bejofo](http://bejofo.net/ttt).

## Artificial Intelligence
This game features multiple difficulty levels of AI to play against. These are outlined below:

#### Very Easy (Minimax)
The easiest bot uses the very well-known minimax algorithm to solve a standard tic tac toe board. For each move, the bot checks if the next local board has been determined. If not, it uses the minimax algorithm to decide which board to play on. Once it has the board, it again uses the minimax algorithm to choose its space on the board.

The minimax algorithm works very well for standard tic tac toe, where the entire game is solved very quickly and a simple heuristic function (reward/punishment for win, lose, draw) can be applied. This is not so easy for ultimate tic tac toe, and so this bot bypasses the issue by only being aware of the local games. As a result, it cannot make strategic descisions as to where it wants to send or avoid sending its opponent. It can also make very predictable moves, which makes it easier to send it where you want. These are necessary skills to master in order to improve in ultimate tic tac toe, and so this is an ideal entry level bot.

The minimax algortithm used was based heavily on the one written by [Clederson Cruz](https://github.com/Cledersonbc/tic-tac-toe-minimax)

#### [Other difficulties need to be developed]

## Prerequisites
In order to run the game you must have PyGame installed on your computer, which can be done using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install pygame
```

## TODO
* ~~Build a command line version of the game~~
* ~~Reorganize logic so that board number is requested at the beginning of each turn, and the focus is updated at the end of the turn, to better match how the GUI will work~~
* ~~Build the GUI~~
* Add a menu area
  * Reset Button
  * Button to display the rules
  * Choose to play 1v1 or against the AI
  * Display text (i.e. who's turn, display the winner, etc...)
* Create an AI
  * ~~Easy difficulty (minimax)~~
  * Harder difficulty (Monte Carlo Tree Search Algorithm)
  * Other, if we find something else
