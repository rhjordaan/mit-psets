/**
 * Customer class - represents a customer that can join the queue and shop
 * @version March 1, 2018
 * @author Richter Jordaan and Bennet Liu
 *
 */
public class Customer {	
	private int id;//customers ID
	private int arrivalTime;//arrival time
	private int transactionTime;//length of transaction
	private int waitTime;//customer's wait time
	private int moneySpent;//money that the customer's spends
	
	/**
	 * Customer constructor - default constructor that instantiates a customer
	 */
	public Customer()
	{
		this(1,0,5,-1);
	}
	
	/**
	 * Constructor - assigns customer's instance field to the parameter values
	 * @param id - int representing the customer's id
	 * @param arrivalTime - int representing the arrivalTime
	 * @param transactionTime - int representing the transactin time
	 * @param waitTime - int representing the wait time
	 */
	public Customer(int id, int arrivalTime, int transactionTime, int waitTime)
	{
		this.id=id;
		this.arrivalTime=arrivalTime;
		this.transactionTime=transactionTime;
		this.waitTime = waitTime;
		moneySpent =(int) (Math.random()*170 +30);//random amount of money spent between 30-200$
	}

	/**
	 * get the customer's id
	 * @return the customer's id, an int
	 */
	public int getId() {
		return id;
	}
	/**
	 * get the customer's arrival time
	 * @return an int representing the arrival time
	 */
	public int getArrivalTime() {
		return arrivalTime;
	}

	/**
	 * get the customer's transaction time
	 * @return an int represent the transaction time
	 */
	public int getTransactionTime() {
		return transactionTime;
	}
	
	/**
	 * set the trasnaction time 
	 * @param transTime, int representing value to set transactionTime to
	 */
	public void setTransactionTime(int transTime)
	{
		transactionTime = transTime;
	}
	/**
	 * set the wait time
	 * @param wtTime, int representing value to set waitTime to
	 */
	public void setWaitTime(int wtTime)
	{
		waitTime = wtTime;
	}
	/**
	 * set arrival time
	 * @param aT - an int representing the time to set the arrival time to
	 */
	public void setArrivalTime(int aT)
	{
		arrivalTime = aT;
	}
	/**
	 * get the wait time of the customer
	 * @return the customer's wait time, an int
	 */
	public int getWaitTime()
	{
		return waitTime;
	}
	/**
	 * get the money spent
	 * @return the customer's purhcase amount
	 */
	public int getMoneySpent(){
		return moneySpent;
	}
}