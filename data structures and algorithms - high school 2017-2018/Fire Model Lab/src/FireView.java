import java.awt.*;
import javax.swing.*;

/**
 *View class 
 *this is the View component
 *The updateView method takes in an array of FireCells
 *and displays them in the window
 *
 *@author Richter Jordaan 
 *@version 3/8/2018
 */

class FireView extends JPanel
{
	//myGrid
    private FireCell[][] myGrid;

    // entry point from model, requests grid be redisplayed
    /**
     * Constructor updateView
     * @param mg - the grid, a 2d array of fireCells
     */
    public void updateView( FireCell[][] mg )
    {
        myGrid = mg;
        repaint();
    }

    /** Displays the grid in the window drawing each square the correct color
     * @param g - the Graphics object 
     */
     public void paintComponent(Graphics g)
    {
        super.paintComponent(g);
        int testWidth = getWidth() / (FireModel.SIZE+1);
        int testHeight = getHeight() / (FireModel.SIZE+1);
        // keep each Fire cell square
        int boxSize = Math.min(testHeight, testWidth);
        int val = 0;
        for ( int r = 0; r < FireModel.SIZE; r++ )
        {
            for (int c = 0; c < FireModel.SIZE; c++ )
            {
                if (myGrid[r][c] != null)
                {
                	val = 0;
                    int ulX = (c+1) * boxSize;
                    int ulY = (r+1) * boxSize;
                    if ( myGrid[r][c].getStatus()==0 )            // dirt
                        g.setColor( new Color(240, 240, 180)  );
                    else if ( myGrid[r][c].getStatus()==1 )      // green tree
                        g.setColor( new Color(90, 190, 90));
                    else{                           // burning tree
                        g.setColor( Color.RED);
                        val = 3;
                        
                    }
                    
                    int topLeftX = ulX+2, topLeftY = ulY+2;
                    int sizeX = boxSize-2, sizeY = boxSize-2;
                    if(val!=3)
                    {
                    	g.fillRect( topLeftX, topLeftY, sizeX, sizeY);
                    	
                    }                    
                    else
                    {
                    	g.fillOval(topLeftX, topLeftY, sizeX, sizeY);
                    }
                }
            }
        }
    }
}
