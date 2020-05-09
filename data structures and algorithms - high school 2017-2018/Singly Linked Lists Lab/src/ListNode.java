/**
 *  Implementation of a node of a singly linked list.
 *
 *  Adapted from the College Board's AP Computer Science AB:
 *  Implementation Classes and Interfaces.
 */
public class ListNode<E extends Comparable<E>>{
  private E value;
  private ListNode<E> next;

  /**
   *  Constructs a new element with object initValue,
   *  followed by next element
   *
   * @param  initValue  New element object
   * @param  initNext   Reference to next element
   */
  public ListNode(E initValue, ListNode<E> initNext){
    value = initValue;
    next = initNext;
  }

  /**
   *  Constructs a new tail of a list with object initValue
   *
   * @param  initValue  New element object
   */
  public ListNode(E initValue){
    this(initValue, null);
  }

  /**
   *  Sets the value attribute of the ListNode object
   *
   * @param  theNewValue  value attribute of the ListNode object
   */
  public void setValue(E theNewValue){
    value = theNewValue;
  }

  /**
   *  Sets reference to new next value
   *
   * @param  theNewNext  The new next value
   */
  public void setNext(ListNode<E> theNewNext){
    next = theNewNext;
  }

  /**
   *  Returns value associated with this element
   *
   * @return    The value associated with this element
   */
  public E getValue(){
    return value;
  }

  /**
   *  Returns reference to next value in list
   *
   * @return    The next value in the list
   */
  public ListNode<E> getNext(){
    return next;
  }
}
