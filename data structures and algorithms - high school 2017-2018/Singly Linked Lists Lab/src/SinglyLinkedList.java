import java.io.File;
import java.util.*;

/**
 *  Implementation of lists, using singly linked elements.
 *
 * @author     G. Peck
 * @created    April 27, 2002
 */
public class SinglyLinkedList<E extends Comparable<E>>{
  private ListNode<E> first;  // first node
  private ListNode<E> last; //last node
  private int size;
  
  /**
   *  Constructor for the SinglyLinkedList object
   *  Generates an empty list.
   */
  public SinglyLinkedList(){
	  first = null;
	  last = null;
	  size = 0;
  }

  /**
   *  Returns the first element in this list.
   *
   * @return  the first element in the linked list.
   */
  public E getFirst(){
	  if(first == null)
	  {
		  throw new NoSuchElementException();
	  }
	  return first.getValue();
  }

  /**
   *  Inserts the given element at the beginning of this list.
   *
   * @param  value  the element to be inserted at the beginning of this list.
   */
  public void addFirst(E value){
    // note the order that things happen:
    // head is parameter, then assigned
	  if(first == null)
	  {
		  first = new ListNode<E>(value);
		  last = first;
	  }
	  else
	  {
		  first = new ListNode<E>(value, first);
	  }
	  size++;
  }
  /**
   * getLast method - get the value, an E, of the value of the last node
   * if list is empty, throw NoSuchElementException
 * @return the value of the last node, of type E
 */
public E getLast()
  {
	  if(last == null)
	  {
		  throw new NoSuchElementException();
	  }
	  return last.getValue();
  }
  /**
   * addLast method - void method that adds the parameter, of type E, making it the last node
 * @param value
 */
public void addLast(E value)
  {
	//if list is empty, simply make the list of size 1
	  if(first == null)
	  {
		  first = new ListNode<E>(value);
		  last = first;
	  }
	  //otherwise add the parameter value to end of list
	  else
	  {
		  last.setNext(new ListNode<E>(value));
		  last = last.getNext();
	  }
	  size++;
  }
  /**
   * getSize method - returns size of list
 * @return the size of the list, an int
 */
public int getSize()
  {
	  return size;
  }
  /**
   *  Print the contents of the entire linked list
   */
  public void printList()
  	{
	  ListNode<E> ptr = first;
	  while(ptr!= null)
	  {
		  System.out.print(ptr.getValue() + " ");
		  ptr = ptr.getNext();
	  }
    }

  /**
   *  Returns a string representation of this list. The string
   *  representation consists of the list's elements in order,
   *  enclosed in square brackets ("[]"). Adjacent elements are
   *  separated by the characters ", " (comma and space).
   *
   * @return    string representation of this list
   */
  public String toString(){
	  String str = "[";
	  ListNode<E> ptr = first;
	  while(ptr!= null)
	  {
		  str = str + ptr.getValue() + ", ";
		  ptr = ptr.getNext();
	  }
	  return str + "]";
  }
  /**
   * insert method - void method that creates the list in ascending order based on id
 * @param id -id, of type E, to be inserted in list
 */
public void insert(E id)
  {
	//if list is empty or the element is smaller id than the first value, add first
			  if(first == null || id.compareTo(first.getValue())<=0)
			  {
				  this.addFirst(id);
				  return;
			  }
			  //if greater in id than last value, addLast
			  else if(id.compareTo(last.getValue())>0)
			  {
				  this.addLast(id);
				  return;
			  }
			  //otherwise find right spot for it
			  else
			  {
				  ListNode<E> prev = first;
				  ListNode<E> temp = first.getNext();
				  while(temp != null)
				  {
					  if(id.compareTo(temp.getValue())<0 && id.compareTo(prev.getValue())>0)
					  {
						  prev.setNext(new ListNode<E>(id, temp));
						  size++;
						  return;
					  }
					  prev = temp;
					  temp = temp.getNext();
				  }
			  }
  }
  /**
   * find method - returns the value of the id given as a parameter, null if not found
 * @param target - id whose value is to be searched for
 * @return - the value of the id, null if not found
 */
public E find(E target)
  {
	  ListNode<E> ptr = first;	  
	  while(ptr!=null)
	  {
		  if(ptr.getValue().compareTo(target)==0)
		  {
			  return ptr.getValue();
		  }
		  ptr = ptr.getNext();
	  }
	  return null;
  }
  /**
 * @param data - id of type E to be removed
 * @return - true if id was found and removed, false if not
 */
public boolean remove(E data)
  {
	//if empty list, there is nothing to remove
	  if(first == null)
	  {
		  return false;
	  }
	  //my two pointers don't account for the first value being what is to be looked for, so I added this if statement to avoid error
	  else if(first.getValue().equals(data))
	  {
		  first = first.getNext();
		  size--;
		  return true;
	  }
	  //if not first element, find the element if it is there and remove it
	  ListNode<E> prev = first;
	  ListNode<E> current = first.getNext();
	  while(current!=null)
	  {
		  if(current.getValue().equals(data))
		  {
			  prev.setNext(current.getNext());
			  size--;
			  return true;
		  }
		  prev = current;
		  current = current.getNext();
	  }
	  //return false if not found
	  return false;
  }
  /**
 * clear method - void method that clears list
 * sets first and last to null, size to 0
 */
public void clear()
  {
	  first = null;
	  last = null;
	  size = 0;
  }
  /**
 * printBackwards method - void method that calls the recursive helper method if list isn't empty to print list backwards
 * 
 */
public void printBackwards()
  {
	//if empty list, give error message
	  if(first == null)
	  {
		  System.out.println("Empty list. Sorry!");
	  }
	  else
	  {
		  //call helper method
		  this.displayBackwards(first);
	  }
  }
  /**
 * displayBackwards - void recursive method that prints out the list backwards
 * base case - empty list
 * @param head - the first node, the last value printed
 */
public void displayBackwards(ListNode<E> head)
  {
	//if the list isn't empty
	  ListNode<E> ptr = head;
	  if(ptr != null)
	  {
		  //recursively call method, moving the pointer one towards end
		  displayBackwards(ptr.getNext());
		  //when recursive calls are done, methods will be completed starting with last node, so print out the values to print out the list backwards
		  System.out.println(ptr.getValue());
	  }
	  
  }
  /**
   * size method - returns size of list
   * testing class wanted a size method in addition to getSize so I added this method 
 * @return an integer representing the size of the list
 */
public int size()
  {
	  return this.getSize();
  }
/*20
196        60
18618        64
2370        65
18410        56
18465        27
19967        45
17911        96
184        14
18871        69
14088        92
18061         3
206        31
13066         8
12705        14
15917        51
15814        60
15320        82
8303        90
7282        73
12328        63*/
}