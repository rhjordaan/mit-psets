/**
 *  Encapsulates an Inventory Item
 *
 * @author     K Jans
 * @created    July 18, 2002
 */

public class Item implements Comparable<Item>{

  private int myId;
  private int myInv;

  /**
   *  Constructor for the Item object
   *
   * @param  id   id value
   * @param  inv  inventory value
   */
   
  public Item(int id, int inv){
    myId = id;
    myInv = inv;
  }

  /**
   *  Gets the id attribute of the Item object
   *
   * @return    The id value
   */
   
  public int getId(){
    return myId;
  }

  /**
   *  Gets the inv attribute of the Item object
   *
   * @return    The inv value
   */
   
  public int getInv(){
    return myInv;
  }

  /**
   *  Compares two Item objects by their id (myId) fields
   *
   * @param  other  Item object to compare to
   * @return              positive int if myId > other.myId
   *                      0 if myId == other.myId
   *                      negative int if myId < other.myId
   * @see java.lang.Comparable#compareTo(java.lang.Object)
 */
public int compareTo(Item other){
    return myId - other.myId;
  }

  /**
   *  Compares the Item to the specified object
   *
   * @param  otherObject  Item object to compare to
   * @return              true if equal, false otherwise
   * @see java.lang.Object#equals(java.lang.Object)
 */
public boolean equals(Object other){
      if (other instanceof Item && other != null)
          return this.compareTo((Item)other) == 0;
      else 
          return false;
      
  }

  /** 
   * String version of an Item
   * @see java.lang.Object#toString()
 */
public String toString(){
    return "Id=" + myId + ",Inv=" + myInv;
  }
}

