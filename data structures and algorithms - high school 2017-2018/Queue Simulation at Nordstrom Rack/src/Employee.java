/**
 * @author Richter Jordaan and Bennet Liu
 * represents an employee with its current customer c
 *
 */
public class Employee {

	private int transLength;//length of transaction
	private Customer customer;// the customer the employee is serving
	private boolean isBusy;// whether the employee is serving a customer or not

	/**
	 * constructor that constructs and employee
	 * @param c - the employee's customer
	 */
	public Employee(Customer c)
	{
		customer = c;
		if(c!=null)
		{
			transLength = c.getTransactionTime();
		}
		isBusy = false;//not busy at the moment

	}

	/**
	 * Sets the employee to serve the customer
	 * 
	 * @param cust, the custoemr that is being served
	 */
	public void setCurrentCustomer(Customer cust)
	{
		customer = cust;//set the customer to the instance variable
		if(cust!=null)//if there is a customer
		{
			transLength = cust.getTransactionTime();//get the transaction length from the customer and set it to the translength of the employee
		}
		isBusy = false;// employee is busy now

	}

	/**
	 * getTranslength is getter that returns the trans length
	 * 
	 * @return the transaction length of the employee
	 */
	public int getTransLength() {
		return transLength;
	}

	/**
	 * getter method that returns the customer being currently served
	 * @return customer being served
	 */
	public Customer getCustomer() {
		return customer;
	}

	/**
	 * 
	 * getter method that returns if the employee is busy or not
	 * 
	 * @return true if employee is busy and false if employee is not busy
	 */
	 public boolean isBusy() {
		return transLength!=0;
	}

	/**
	 * increment time increments the employees time by subtracting 1 minute fromt he transaction length
	 */
	public void incrementTime()
	{
		transLength--;
	}

	/**
    * Sets the transaction time for the employee
	 * @param transTime set the transaction time of the 
	 */
	public void setTransLength(int transTime)
	{
		transLength = transTime;
	}

}
