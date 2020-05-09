import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.Queue;

/**
 * Store class - models and displays the store for a given time period
 * @author Richter Jordaan and Bennet Liu
 * @version March 4, 2018
 *
 */
public class Store {
	private Queue<Customer> customers;//queue of waiting customers
	private Employee employee;//queue of waiting employees
	private final int NUM_MINUTES;//length of a business day
	private final int ARRIVAL_PROB;//probability of arrival
	private final int MAX_TRANSACTION;//random integer between 1 and maximum for transaction time
	private double avWaitTime;//the average wait time
	private int maxWaitTime;//the maximum wait time
	//ArrayList<Integer> waitTimes;
	private double sumWaitTimes;//the sum of all the wait times
	private int customersServed;//the number of customers served
	private int tipTotal;//the total amount of tips
	View view;// the view
	Customer currentCust;//the current customer being served
	private int currentTime;// the current time
	private boolean eventHappenedToday;//if something happened today
	private int timeSpeed;//how many seconds to pause the screen between minutes
	/**
	 * 
	 * Constructor, constructs stores and initizilizes variables to indicate the start of a day
	 * @param custList the queue of customers
	 * @param dayLength length of day
	 * @param probOfArriv probability of arrival
	 * @param transMax maximum transaction
	 */
	public Store(Queue<Customer> custList, int dayLength, int probOfArriv, int transMax, int timeSpeed)
	{
		customers = custList;//instantiate customer list
		employee = new Employee(null);//create a new employee
		NUM_MINUTES = dayLength;//length of the day
		ARRIVAL_PROB = probOfArriv;//the probability of someone arriving
		MAX_TRANSACTION = transMax;//lenght of transaction max
		//waitTimes = new ArrayList<Integer>();
		customersServed=0;//0 at the moment
		sumWaitTimes = 0;
		tipTotal=0;
		view = new View();//create a new view
		currentCust = null;
		eventHappenedToday=false;
		this.timeSpeed=timeSpeed;
	}
	/**
	 * helper method that returns true or false whether a customer arrives at that time
	 * 
	 * @return true if a customer arrives or false if a customer does not arrive
	 */
	public boolean doesCustomerArrive()
	{
		int randNum = (int)(Math.random()*100+1);//generate a random number from 1-100
		return randNum <= ARRIVAL_PROB;//if the random number is less than the arrival probability
	}

	/**
	 * helper method that generate a random time from 1-max transaction for how long a customer will be served
	 * 
	 * @return a time that it takes for a customer to be served
	 */
	public int generateTransTime()
	{
		return (int)(Math.random()*MAX_TRANSACTION)+1;//generate random number from 1-max transaction
	}

	/**
	 * 
	 * generates a random tip based on the the amount of money spent
	 * @param c the customer
	 * @return a random tip amount
	 */
	public int getTip(Customer c)
	{
		double percentOfPurchaseToTip = ((Math.random()*8)+3)*0.01;//generates the percent of purchase (which is 3%-8%)
		return (int)(c.getMoneySpent()*(percentOfPurchaseToTip));//multiply the percent by the money spent to get a tip amount

	}

	/**
	 * A helper method that marks the start of the day and prints out all of the necessary information
	 */
	public void startDay()
	{

		view.updateMinute(1);//updates time box in view and sets to time 1
		System.out.println("The store opens; it is minute 1.");
		view.displayEvent("The store opens; it is minute 1.");
		System.out.println("The employee is waiting for customers to arrive...\n");
		view.displayEvent("The employee is waiting for customers to arrive...");
	}

	/**
	 * A helper method that prints out the updated customer information
	 * @param currentTime - the current time
	 * @[aram cust - the current customer
	 */
	public void printUpdatedInfo(int currentTime, Customer cust)
	{
		System.out.println("Minute: " + currentTime);
		view.displayEvent("Minute: " + currentTime);
		System.out.println("Customer: " + cust.getId() + " arrived and is added to queue");
		view.displayEvent("Customer: " + cust.getId() + " arrived and is added to queue");
	}

	/**
	 * @param cust the customer you are pulling out of queue on screen
	 */
	public void createCustomer(Customer cust)
	{
		if(customers!=null)// if there is a customer in the queue
		{
			view.createCustomer(cust.getId(), 25+100*(customers.size()-1), 75);//create a customer in the view behind the last person in the queue
		}
		else
		{
			view.createCustomer(cust.getId(), 25, 75);//first customer so just create customer
		}
	}

	/**
	 * processCustomer will process one customer in the queue and perform the necessary operations
	 * 
	 * @param beforeHours represents whether the store is currently open, and if false then it is past closing hours
	 */
	/**
	 * @param beforeHours
	 */
	public void processCustomer(boolean beforeHours)
	{
		boolean condition = false;
		if(beforeHours)
		{
			condition = currentTime<=NUM_MINUTES;
		}
		else
		{
			condition = !customers.isEmpty();
		}
		while(condition)//while it is not the end of the day
		{
			view.updateMinute(currentTime);//update the minutes with the current time
			view.clearEvent();//clear all in the view
			view.resetNextLineY();//reset the line
			currentCust = customers.peek();//get the next customer in the queue
			eventHappenedToday = false;
			if(beforeHours)
			{
				if(doesCustomerArrive())//if a customer does arrive
				{
					eventHappenedToday = true;//something happened
					Customer cust = new Customer(customers.size()+1+customersServed , currentTime, this.generateTransTime(), -1);//create new customer
					cust.setArrivalTime(currentTime);//set the correct arrival time

					printUpdatedInfo(currentTime, cust);//print the updated information

					customers.add(cust);//add customer to queue

					createCustomer(cust);//creates the customer in the view

				}
			}

			if(currentCust!=null)//if there is a customer in line
			{
				//System.out.println("" + employee.isBusy());//print out whether or not the employee is busy or not
				if(!employee.isBusy())//if the employee is not busy
				{
					if(!eventHappenedToday)//if no event happened yet print out and display current time
					{
						System.out.println("Minute: " + currentTime);
						view.displayEvent("Minute: " + currentTime);
					}
					view.moveToExit(currentCust.getId());

					view.moveCustomerToEmployee(currentCust.getId());//move customer in view

					System.out.println("Employee is now available to help new customer. Customer " + currentCust.getId() + " departs.");//print out employee can help customer
					view.displayEvent("Employee is now available to help new customer. Customer " + currentCust.getId() + " departs.");//display employee can help customer 
					eventHappenedToday = true;//something happened

					currentCust.setWaitTime(currentTime-currentCust.getArrivalTime());//set the wait time of the current customer
					sumWaitTimes+=currentCust.getWaitTime();//add the customers wait time to the sum of the wait times

					if(currentCust.getWaitTime()>maxWaitTime)//if the current customers wait time is greater than the max wait time
					{
						maxWaitTime = currentCust.getWaitTime();//reassign max wait time
					}

					tipTotal+=this.getTip(currentCust);//add tip of current customer to tip total
					
					
					
					customers.remove();//customer served
					customersServed++;

					for(int i = 1; i<=customers.size(); i++)//shifting all of the customers in line in view
					{
						view.clearCustomer(25+100*(i), 75);//clear customer from view
						view.createCustomer(customersServed+i, 25+100*(i-1), 75);//create customer in next spot
					}

					currentCust = customers.peek();//get the next customer in line

					if(currentCust!=null)// if there is still a customer in the queue after the previous customer has been removed
					{

						employee.setCurrentCustomer(currentCust); ;//send customer to be served by employee
						System.out.println("Employee will be busy with customer " + currentCust.getId() + " until time: " + (currentCust.getTransactionTime()+currentTime));//employee will be serving next customer
						view.displayEvent("Employee will be busy with customer " + currentCust.getId() + " until time: " + (currentCust.getTransactionTime()+currentTime));

						employee.incrementTime();//increment the employee time
					}
					else//there are no customers in the queue so just wait
					{

						eventHappenedToday = true;
						if(beforeHours)
						{
							view.moveToExit(customersServed);
							System.out.println("All customers have been served. Waiting for new customers...");
							view.displayEvent("All customers have been served. Waiting for new customers...");
						}
					}
				}
				else//if the employee is not busy
				{


					employee.incrementTime();//else increment the employees time
				}
			}
			if(eventHappenedToday)
			{
				System.out.println(" ");// add a space in between today and tommorrow
			}
			else
			{
				view.displayEvent("Waiting..");//nothing happened so just waiting
			}

			currentTime++;//increment current time
			view.pause(timeSpeed);//refreshes screen


			if(beforeHours)//if it is before the close of the store
			{
				condition = currentTime<=NUM_MINUTES;//condition is true when the store is not closed yet, and false when the store closed
			}
			else//it is after closing hours
			{
				condition = customers.size()>0;//condition is true when there are customers in the queue
			}
		}
	}

	/**
	 * Simulates one day at the shop
	 */
	public void oneDay()
	{
		currentTime = 1;//start of day


		startDay();


		this.processCustomer(true);

		//now serve remaining customers after numMinutes
		if(customers.size()>0)//if there are still customers left to be served
		{
			System.out.println("We have passed closing hours, so now we will serve the remaining customers\n");
			view.clearEvent();
			view.displayEvent("We have passed closing hours, so now we will serve the remaining customers");
			view.pause(1);
			this.processCustomer(false);//process the customers left remaining in the queue
		}


		System.out.println("\nAll customers have been served. All done. The store will now close\n");//once all of the customers have been served
		view.clearEvent();
		view.displayEvent("All customers have been served. All done. The store will now close");
		view.clearCustomer(215, 295);//clear the customers from view
		view.clearCustomer(645, 520);
	}

	/**
	 * calculateWaitTimes will calculate the wait time as well as the tip and display the results
	 */
	public void calculateWaitTimes()
	{
		if(sumWaitTimes==0)//if there were no customers
		{
			System.out.println("No customers arrived, so there is no data. Sorry!");
			view.updateStatistics(0, 0,0,0, 0);//no customers so update statistics with nothing
			return;
		}
		System.out.println("Statistics from the simulation:");
		//find max and average wait times
		System.out.println("Total customers served: " + customersServed);
		avWaitTime = sumWaitTimes/customersServed;//average wait time is the sum of wait times divided by the customers served
		DecimalFormat df = new DecimalFormat("#.##");      
		avWaitTime = Double.valueOf(df.format(avWaitTime));
		System.out.println( "Average wait time: " + avWaitTime + " minutes.");
		System.out.println("Max wait time: " + maxWaitTime + " minutes.");
		System.out.println("Average tip: " + (tipTotal/customersServed) + " dollars");//the average tip is valvulated by dividing total amount of tips by the customers served
		System.out.println("Total tip  money: " + tipTotal + " dollars");
		view.updateStatistics(customersServed, avWaitTime, maxWaitTime, tipTotal/customersServed, tipTotal);//update the statistics in view
		view.custOfDay();
	}
	/**
	 * @param args - main class to run the simulation
	 * This is where we adjust the time, arrival probability, max transaction length, and time speed
	 * between different test runs
	 */
	public static void main(String[] args)
	{
		Queue<Customer> customers = new  LinkedList<Customer>();
		//8 hour day, 20 percent arrival prob, 4 minute max trans length
		//we made this have a 0 second pause between days to have time to read graphics
		Store store = new Store(customers, 60, 50, 4, 0);
		store.oneDay();
		store.calculateWaitTimes();
	}


}
