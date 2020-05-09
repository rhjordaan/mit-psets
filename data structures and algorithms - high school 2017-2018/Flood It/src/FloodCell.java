import java.awt.*;

import javax.swing.*;
/**
 * This is the representation of a color
 * a cell's color should be assigned to 1 of four colors
 * use an algorithm of your choice to randomly assign the colors
 * 
 * @author Richter Jordaan
 * @version March 15, 2018
 *
 */
public class FloodCell {

	public static final int BLUE = 0, GREEN = 1, YELLOW = 2, RED = 3, PINK = 4, BLACK = 5;
	private int status; //color of cell

	/**
	 * FloodCell constructor - constrcuts a cell with a random color
	 * @param hard - true if the user wants a 'difficult' game, with more colors
	 */
	public FloodCell(boolean hard)
	{
		//if hard then there are 6 possible colors, otherwise there are 5
		if(hard)
		{
			status = (int)(Math.random()*6);
		}
		else
		{
			status = (int)(Math.random()*4);
		}
	}

	
	/**
	 * getStatus method - returns the current color of the cell
	 * @return an int representing the current color of the cell
	 */
	public int getStatus()
	{
		return status;
	}
	/**
	 * setStatus method - sets the cell's color to the value of color, the param
	 * @param color - an int representing the new color of the cell
	 */
	public void setStatus(int color)
	{
		status = color;
	}

}
