


import java.awt.*;

import javax.swing.*;


/**
 
 * FloodModel class- recursively models the grid
 * @author Richter Jordaan
 * @version March 15, 2018
 *
 */
public class FloodModel
{
	public static int SIZE = 20;
	public static int TURNS = 25;
	private FloodCell[][] myGrid;
	private FloodView myView;
	private int tries;

	/**
	 * Constructor of Model
	 * create the grid and fill it with Flood Cells
	 * assign the view and then update it with the new grid
	 * intialize tries to 0
	 * @param view - GUI for the flood it game
	 */
	public FloodModel(FloodView view, int difficulty, int size, int turns, boolean extraColors)
	{
		//if the game is in easy, the size is 15x15 and the user gets 30 turns
		if(difficulty==1)
		{
			SIZE = 15;
			TURNS = 30;
		}
		//if the game is medium, the size is 20x20 and the user gets 25 turns
		//if the game is hard, the size is 25x25, the user gets 15 turns, and there are 6 colors
		else if(difficulty == 3)
		{
			SIZE = 25;
			TURNS = 15;
		}
		else if(difficulty==4)
		{
			SIZE = size;
			TURNS = turns;
		}
		//construct the cells
		myGrid = new FloodCell[SIZE][SIZE];
		for(int row = 0; row<SIZE; row++)
		{
			for(int col = 0; col<SIZE; col++)
			{
				myGrid[row][col] = new FloodCell(extraColors);
			}
		}
		//set tries to 0 and update view
		tries=0;
		myView = view;
		myView.updateView(myGrid);
	}

	/**
	 * Helper method to check if row and col are in bounds
	 * @param row in grid
	 * @param col in grid
	 * @return true if row,col are in bounds
	 */
	private boolean isInBounds(int row, int col)
	{
		return row>=0 && row<SIZE && col>=0 && col<SIZE;
	}

	/**
	 * Recursive method to fill the grid starting at 0,0 with
	 * a new color.  All adjacent squares that match the color at 0,0
	 * will be replaced by the new color.
	 * @param r - row to start recursion
	 * @param c - column to start recursion
	 * @param newColor - color to change to
	 * @param pastColor - color currently at 0,0
	 */
	public void recursiveFlood(int r, int c, int newColor, int pastColor)
	{
		if(isInBounds(r,c) && myGrid[r][c].getStatus()==pastColor)
		{
			myGrid[r][c].setStatus(newColor);
			recursiveFlood(r-1,c,newColor,pastColor);
			recursiveFlood(r+1,c,newColor,pastColor);
			recursiveFlood(r,c-1,newColor,pastColor);
			recursiveFlood(r,c+1,newColor,pastColor);
		}
	}

	/**
	 * Method to make one color change on the grid
	 * get the color at 0,0 and flood the grid
	 * determine if the game is over
	 * @param color - color to "flood" the grid with
	 * @return true if the game is over (you won or lost)
	 */
	public boolean makeMove(int color)
	{   
		tries++;
		if(color!=myGrid[0][0].getStatus())
		{
			recursiveFlood(0,0,color,myGrid[0][0].getStatus());
		}
		myView.updateView(myGrid);
		return gameWon();
	}

	/**
	 * helper method for makeMove to determine if
	 * user has "flooded" the grid with one color
	 * @return true if the grid is one color
	 */
	private boolean gameWon()
	{
		if(tries>=TURNS)
		{
			return true;
		}
		int color = myGrid[0][0].getStatus();
		for(int row = 0; row<SIZE; row++)
		{
			for(int col = 0; col<SIZE; col++)
			{
				if(myGrid[row][col].getStatus()!=color)
				{
					return false;
				}
			}
		}
		return true;
	}
	/**
	 * get the user's tries
	 * @return tries, an int
	 */
	public int getTries()
	{
		return tries;
	}
}

