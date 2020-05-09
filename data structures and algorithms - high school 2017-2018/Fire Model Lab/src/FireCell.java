/**
 * FireCell class - represents a cell that is either dirt, a tree, or a burning tree
 * @author Richter Jordaan
 * @version March 8, 2018
 *
 */
public class FireCell
{
    public static final int DIRT = 0, GREEN = 1, BURNING = 2;
    int status; //representing which of the three it is

    /**
     * FireCell constructor - create a fireCell with a 60% chance of being a tree 
     *and 40% chance of dirt
     */
     public FireCell()
    {
	   if(Math.random()<0.6)
	   {
		   //tree
		   status = 1;
	   }
	   else
	   {
		   status = 0;
	   }
	}
    
    /**
     * getStatus method - return the state of the cell
     *@ return an integer representing the type of cell: DIRT, GREEN or BURNING
     *
     */
     public int getStatus()
    {
        return status;
    }
    
    /**
     * setStatus method - set the type of cell: DIRT, GREEN or BURNING
     * @param n- an int representing the status to set the cell to
     *
     */
     public void setStatus(int n)
    {
        status = n;
    }
}

