

import java.awt.*;

import javax.swing.*;

/*
  this is the View component
*/

class FloodView extends JPanel
{
	static final long serialVersionUID = 1L;
	private FloodCell[][] myGrid;

    // entry point from model, requests grid be redisplayed
    public void updateView( FloodCell[][] mg )
    {
        myGrid = mg;
        repaint();
    }
    public void paintComponent(Graphics g)
    {
        super.paintComponent(g);
        int testWidth = getWidth() / (FloodModel.SIZE+1);
        int testHeight = getHeight() / (FloodModel.SIZE+1);
        // keep each Flood cell square
        int boxSize = Math.min(testHeight, testWidth);

        for ( int r = 0; r < FloodModel.SIZE; r++ )
        {
            for (int c = 0; c < FloodModel.SIZE; c++ )
            {
                if (myGrid[r][c] != null)
                {
                    int ulX = (c+1) * boxSize;
                    int ulY = (r+1) * boxSize;
                    
                    int val = myGrid[r][c].getStatus();
                    switch(val)
                    {
                    case 0:
                    	g.setColor(Color.BLUE);
                    	break;
                    case 1:
                    	g.setColor(Color.GREEN);
                    	break;
                    case 2:
                    	g.setColor(Color.YELLOW);
                    	break;
                    case 3:
                    	g.setColor(Color.red);
                    	break;
                    case 4:
                    	g.setColor(Color.pink);
                    	break;
                    default:
                    	g.setColor(Color.black);
                    	break;
                    }

                    int topLeftX = ulX+2, topLeftY = ulY+2;
                    int sizeX = boxSize-2, sizeY = boxSize-2;
                    g.fillRect( topLeftX, topLeftY, sizeX, sizeY);
                }
            }
        }
    }
}
