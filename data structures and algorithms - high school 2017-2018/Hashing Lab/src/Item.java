import java.security.*;
import java.util.*;
/**
 *  Description of the Class
 *
 * @author     G. Peck
 * @created    July 18, 2002
 */

public class Item implements Comparable
{
  private int myId;
  private int myInv;

  /**
   *  Constructor for the Item object
   *
   * @param  id   id value
   * @param  inv  inventory value
   */
  public Item(int id, int inv)
  {
    myId = id;
    myInv = inv;
  }

  /**
   *  Gets the id attribute of the Item object
   *
   * @return    The id value
   */
  public int getId()
  {
    return myId;
  }

  /**
   *  Gets the inv attribute of the Item object
   *
   * @return    The inv value
   */
  public int getInv()
  {
    return myInv;
  }
/**
 *    * hashCode method 1
 * creates a hashCode for the item's ID.  
 * This function returns the id modulus the capacity
 * Overrides the object hashCode method
 *
 * @return   efficient hashCode based on ID, the id modulus the capacity
 **/
  public int hashCode1()
  {
	 return myId%600;
  }
  /**
   *    * hashCode method 2
   * creates a hashCode for the item's ID.  
   * This function returns the tangent of the id modulus the capacity
   * Overrides the object hashCode method
   *
   * @return   efficient hashCode based on ID, the tangent of the id modulus the capacity
   **/
  public int hashCode2()
  {
	 return ((int)Math.tan(myId))%600;
  }
  /**
   *    * hashCode method 3
   * creates a hashCode for the item's ID.  
   * This function returns the sum of the digits of the id modulus the capacity
   * Overrides the object hashCode method
   *
   * @return   efficient hashCode based on ID, the sum of the digits of the id of the id modulus the capacity
   **/
  public int hashCode3()
  {
	  int sumDigits = 0;
	  int id = myId;
	  while(id/10!=0)
	  {
		  sumDigits+=id%10;
		  id/=10;
	  }
	  return (int)(Math.pow(4,  sumDigits))%600;
  }
  /**
   * hashCode method 4
   * creates a hashCode for the item's ID.  
   * This function returns the last digit of the id raised to the power of the inventory, modulus the capacity
   * Overrides the object hashCode method
   *
   * @return   efficient hashCode based on ID, the last digit of the id raised to the power of the inventory, modulus the capacity
   **/
  public int hashCode4()
  {
	 int id = myId;
	 while(id/10>1)
	 {
		 id/=10;
	 }
	 return (int)(Math.pow(id, myInv)%600);
  }
	  
	  
	// return ((int)(Math.random() * myInv) + (int)(Math.cos(Math.toDegrees(myInv)))%600);
/*	  
	  int sumDigits = 0;
	  int id = myId;
	  while(id/10!=0)
	  {
		  sumDigits+=id%10;
		  id/=10;
	  }
	  return sumDigits;*/
	  
	  //return (int)Math.pow(((int)(Math.random()*myId))%5, myInv%5);
	  

  /**
   *  Compares two Item objects by their Id (myId) fields
   *
   * @param  otherObject  Item object to compare to
   * @return              positive int if myId > otherObject.myId
   *                      0 if myId == otherObject.myId
   *                      negative int if myId < otherObject.myId
   */
  public int compareTo(Object otherObject)
  {
    Item other = (Item) otherObject;

    return myId - other.myId;
  }

  /**
   *  Compares the Item to the specified object
   *
   * @param  otherObject  Item object to compare to
   * @return              true if equal, false otherwise
   */
  public boolean equals(Object otherObject)
  {
    return this.compareTo(otherObject) == 0;
    //Item other = (Item)otherObject;
    //return myId == other.myId;
  }

  public String toString()
  {
    return "Id= " + myId + ",Inv= " + myInv;
  }
}

