import javax.swing.JOptionPane;

/**
 *This is the Model class
 *It will solve recursively the problem of seeing how far
 *a forest fire will spread dependent on the placement of the trees
 *It is called by the Controller class
 *
 *@author Richter Jordaan
 *@version March 8, 2018
 */
 
 public class FireModel
{
    public static int SIZE = 47;
    private FireCell[][] myGrid;
    private FireView myView;

    /**
     * FireModel constructor
     *Fill the myGrid array with random FireCells.
     *Send the array to the View Class to be displayed
     *@param myView display class
     */
      public FireModel(FireView view)
    {
        myGrid = new FireCell[SIZE][SIZE];
        int setNum = 0;
        for (int r=0; r<SIZE; r++)
        {
            for (int c=0; c<SIZE; c++)
            {
                myGrid[r][c] = new FireCell();
            }
        }
        myView = view;
        myView.updateView(myGrid);
    }

    /**
     * void recursiveFire method - recursively models the path of the fire for a single cell
     * @param row - an integer representing the row of the cell to spread the fire around
     * @param col- an integer representing the col of the cell to spread the fire around
     */
    public void recursiveFire(int row, int col)
    {
 		//slow it down
 		try {
			Thread.sleep(4);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		myView.updateView(myGrid);
    	//if in bounds, is a tree
     	if(isInBounds(row,col) && myGrid[row][col].getStatus()==FireCell.GREEN)
     	{
     		//set this status to burning
     		myGrid[row][col].setStatus(FireCell.BURNING);
     		//burn neighboring trees
     		recursiveFire(row-1,col);
     		recursiveFire(row+1,col);
     		recursiveFire(row,col-1);
     		recursiveFire(row,col+1);
     	}
    }
    /**
     * isInBounds method - checks to see if the row,col will not give an arrayIndexOutOfBoundsException
     * @param row - row of the cell to check, an int
     * @param col- col of the cell to check, an int
     * @return boolean: true if in bounds, false otherwise
     */
    public boolean isInBounds(int row, int col)
    {
    	return row>=0 && row<SIZE && col>=0 && col<SIZE;
    }
    
    /**
     * solve method - a void method to invoke the recursive fire method that solves the problem
     *After the new updated grid is complete it is sent to the View Class
     *Extra Credit:  animate the fire!- hint: not done in this method
     */
     public void solve()
    {     
    	//set all cells on last row on fire
     	for(int col = 0; col<SIZE; col++)
     	{
     		recursiveFire(SIZE-1,col);
     	}
     	
        myView.updateView(myGrid); 
        //see whether the town was spared
        boolean spared = true;
        for(int col = 0; col<SIZE; col++)
        {
        	if(myGrid[0][col].getStatus()==FireCell.BURNING)
        	{
        		spared = false;
        		break;
        	}
        }
        //display right message
        if(spared)
        {
        	JOptionPane.showMessageDialog(null, "The city of Blackhawk, Colorado was spared.");
        }
        else
        {
        	JOptionPane.showMessageDialog(null, "Fire reached city of Blackhawk, Colorado.");
        }
        
    }
    
}

