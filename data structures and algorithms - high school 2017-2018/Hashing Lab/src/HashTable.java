/**
 *  Hash-Coded Data Storage Table
 *  Maximum size is 600
 *
 * @author     
 * @created    
 *
 */
import java.util.*;

/**
 * HashTable class - models a hash table with each bucket a LinkedList
 * allows user to add, search for, and analyze the data
 * @author Richter Jordaa
 * @version April 28, 2018
 *
 */
/**
 * @author richterjordaan
 *
 */
public class HashTable{
  private int size; // the amount of data stored in the table
  private int capacity; //the number of slots available for storage
  private ArrayList <ListNode> myHashTable; //The table of linked lists!

  /**
 * HashTable default constructor - instanties size and hash table, sets capacity to 600, then fills the table with nulls
 */
public HashTable(){
    size = 0;
    capacity = 600;
    myHashTable = new ArrayList<ListNode>(capacity);
    fillWithNulls();
  }


/**
* HashTable default constructor - instanties size and hash table, sets capacity to numSlots, then fills the table with nulls
* @param an int representing the number of slots/buckets to set capacity to
*/
public HashTable(int numSlots){
    size = 0;
    capacity = numSlots;
    myHashTable = new ArrayList<ListNode>(capacity);
    fillWithNulls();
  }

 /**
 * fillWithNulls method - void method that sets all of the buckets in the hash table (of linked lists) to null
 */
public void fillWithNulls(){
	  for(int i = 0; i<capacity; i++)
	  {
		  myHashTable.add(null);
	  }
  }
  
  /**
   * getSize method - returns the size of the hash table
 * @return an int representing the size of the hash table
 */
public int getSize(){
    return size;
  }

  /**
   * getCapacity method - returns the capacity of the hash table
 * @return an int representing the capacity of the hash table
 */
public int getCapacity(){
   return capacity;
  }

  /**
   * add method - adds Object obj to the hash table
 * @param obj - the object, which can be cast to an item, to add to the hash table
 */
public void add(Object obj){
	//find linked list reference 
	  ListNode list =  myHashTable.get(((Item)obj).hashCode());
	  //add obj to the end of the linked list
	  if(list!=null)
	  {
		  ListNode ptr = list;
		  if(ptr.getNext()==null)
		  {
			  ptr.setNext(new ListNode(obj));
		  }
		  else
		  {
			  while(ptr.getNext()!=null)
			  {
				  ptr = ptr.getNext();
			  }
			  ptr.setNext(new ListNode(obj));
		  }
	  }
	  else
	  {
		  ListNode node = new ListNode(obj, list);
		  myHashTable.set(((Item)obj).hashCode(), node);
	  }
	  size++;
  }

  /**
   * find method - searches for Comparable object which can be cast to an Item target, returning the item if found, else returning null
 * @param target - a Comparable object, can be cast into Item, representing the item to look for
 * @return - the item corresponding to the id if found, else null
 */
public Object find(Comparable target){
  // will attempt to find idToFind in table, if found return the item object
  // else return null
	  ListNode list =  myHashTable.get(((Item)target).hashCode());
	  ListNode ptr = list;
	  while(ptr!=null)
	  {
		  if(((Item)ptr.getValue()).equals((Item)target))
		  {
			  return ((Item)ptr.getValue());
		  }
		  ptr = ptr.getNext();
	  }
	  return null;
  }

  /**
   * getNumberOfNulls method - returns the number of null linked list / empty buckets, in the hash table
 * @return an int representing then number of null buckets
 */
public int getNumberOfNulls(){
    int count = 0;
    for(ListNode node: myHashTable)
    {
    	if(node == null)
    	{
    		count++;
    	}
    }
    return count;
  }

  /**
   * getLongestList method - returns the length of the longest list in the hash table
 * @return an int representing the length of the longest linked list / bucket as the first element
 */
public int getLongestList (){
    int longest = 0;
    for(ListNode node: myHashTable)
    {
    	int count = 0;
    	ListNode ptr = node;
		while(ptr!=null)
		{
			count++;
			ptr = ptr.getNext();
		}
    	if(count>longest)
    	{
    		longest = count;
    	}
    }
    return longest;
  }
public double getAvLength()
{
	return ((double)size)/(capacity-this.getNumberOfNulls());
}
}