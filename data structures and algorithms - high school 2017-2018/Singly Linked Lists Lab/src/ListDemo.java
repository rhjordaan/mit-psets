/**
 *  Demonstrates the use of the SinglyLinkedList class.
 *
 * @author     G. Peck
 * @created    May 12, 2002
 */
public class ListDemo{
  SinglyLinkedList<Integer> myList;

  public ListDemo(){
    myList = new SinglyLinkedList<Integer>();
  }

  /**
   *  Creates a SinglyLinkedList of 5 Integer nodes
   */
  public void createList(){
    for (int k = 1; k <= 20; k++){
      myList.addLast(new Integer(k));
    }
  }

  /**
   *  Display the first element of the list
   */
  public void displayFirst(){
    System.out.println("First Element: " + myList.getFirst());
  }
  public void displayLast()
  {
	  System.out.println("Last Element: " + myList.getLast());
  }
  public void displaySize()
  {
	  System.out.println("Size: " + myList.getSize());
  }
  /**
   *  Print the contents of myList
   */
  public void print(){
    myList.printList();
    System.out.println();
  }
public static void main(String[] args)
{
	ListDemo test = new ListDemo();
	test.createList();
	//test.displayFirst();
	//test.displayLast();
	test.print();
	test.displaySize();
}
}