/**
 * Implements the doubly-linked list of messages for Teletext
 */

import java.awt.Graphics;

/**
 * TeletextList class - models a Teletext screen that continually provides the news, represented by a circular linked list
 * Headlines can be added or removed based on the user's input
 * @author Richter Jordaan
 * @version January 24, 2018
 */
public class TeletextList
{
  private ListNode2 heading, topNode;

  /**
   * Creates a circular list of headlines.
   * First creates a circular list with one node, "Today's headlines:".
   * Saves a reference to that node in heading.
   * Adds a node holding an empty string before heading
   * and another node holding an empty string after heading.
   * Appends all the strings from headlines to the list, after
   * the blank line that follows heading,
   * preserving their order.  Sets topNode equal to heading.
   */
  public TeletextList(String[] headlines)
  {
	  heading = new ListNode2("Today's headlines:");
	  heading.setPrevious(heading);
	  heading.setNext(heading);
	  this.addBefore(heading, " ");  
	  ListNode2 node = this.addAfter(heading, " ");
	  for(String msg: headlines)
	  {
		  node = this.addAfter(node, msg);
	  }
	  topNode = heading;
  }

  /**
   * Inserts a node with msg into the headlines list after the blank
   * line that follows heading.
   * @param String msg representing the headline to be inserted
   * void method - no return type
   */
  public void insert(String msg)
  {
	  this.addAfter(heading.getNext(), msg);
  }

  /**
   * Deletes the node that follows topNode from the headlines list,
   * unless that node happens to be heading or the node before or after
   * heading that holds a blank line.
   * void method - no return type
   */
  public void delete()
  {
	if(topNode.getNext() != heading && topNode.getNext() != heading.getPrevious() && topNode.getNext() != heading.getNext())
	{
		this.remove(topNode.getNext());
	}
  }

  /**
   * Scrolls up the headlines list, advancing topNode to the next node.
   * void method - no return type
   */
  public void scrollUp()
  {
	 topNode = topNode.getNext();
  }

  /**
   * Adds a new node with msg to the headlines list before a given node.
   * Returns a referenece to the added node.
   * @param ListNode representing the node to add before
   * @param a String representing the headline to add in
   * @return a ListNode2 object representing the node that was added
   * 
   */
  private ListNode2 addBefore(ListNode2 node, String msg)
  {
    ListNode2 newNode = new ListNode2(msg, node.getPrevious(), node);
    node.getPrevious().setNext(newNode);
    node.setPrevious(newNode);
    return newNode;
  }

  /**
   * Adds a new node with msg to the headlines list after a given node.
   * Returns a referenece to the added node.
   * @param ListNode representing the node to add after
   * @param a String representing the headline to add in
   * @return a ListNode2 object representing the node that was added
   */
  private ListNode2 addAfter(ListNode2 node, String msg)
  {
	  ListNode2 newNode = new ListNode2(msg, node, node.getNext());
	  node.getNext().setPrevious(newNode);
	  node.setNext(newNode);
	  return newNode;
  }

  /**
   * Removes a given node from the list.
   * @param ListNode node - the node to be removed
   */
  private void remove(ListNode2 node)
  {
	  node.getPrevious().setNext(node.getNext());
	  node.getNext().setPrevious(node.getPrevious());
  }

  /**
   * Draws nLines headlines in g, starting with topNode at x, y
   * and incrementing y by lineHeight after each headline.
   */
  public void draw(Graphics g, int x, int y, int lineHeight, int nLines)
  {
    ListNode2 node = topNode;
    for (int k = 1; k <= nLines; k++)
    {
      g.drawString((String)node.getValue(), x, y);
      y += lineHeight;
      node = node.getNext();
    }
  }
}
