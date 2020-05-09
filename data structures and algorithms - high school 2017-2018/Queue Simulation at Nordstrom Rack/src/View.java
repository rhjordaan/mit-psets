import java.awt.Color;
import java.awt.Font;

/**
 * @author Richter Jordaan and Bennet Liu
 * @version 2.28.18
 * View class - draws and maintains the screen representing the Store
 */
public class View {
	
	int nextLineY; //next line represents the next line in the text box where new text can be added
	/**
	 * View constructor - sets up the screen
	 */
	public View()
	{
		nextLineY = 640;
		//set canvas size and x,y scale
		StdDraw.setCanvasSize(1400, 700);
		StdDraw.setXscale(0, 1400);
		StdDraw.setYscale(0,700);
		
		//set up the spaces designated for the interior of store as well as space for customer queue
		StdDraw.setPenRadius(0.01);
		StdDraw.setPenColor(Color.pink);
		StdDraw.filledRectangle(1185, 450, 215, 250);
		StdDraw.setPenColor(Color.LIGHT_GRAY);
		StdDraw.filledRectangle(700, 100, 700, 100);
		StdDraw.setPenColor(Color.WHITE);
		StdDraw.setPenRadius(0.01);
		StdDraw.filledRectangle(700, 75, 700, 50);
		StdDraw.setPenRadius();
		StdDraw.setPenColor();
		
		//draw in pictures for screen
		StdDraw.text(250,680, "Welcome to Nordstrom's Rack!");
		StdDraw.picture(800, 650, "exit.jpg", 200,100);
		StdDraw.picture(225, 500, "employee.jpg",250,250);
		StdDraw.picture(324, 454, "tips.jpg",35, 70);
		
		//draw in the text for the queue
		StdDraw.line(0, 200, 1400, 200);
		StdDraw.text(100, 210, "Customer Queue Below");
		
		//reset the font to make it smaller and then draw in text for the employee's last customer serve
		Font font = new Font("SANS_SERIF", Font.PLAIN, 10);
		StdDraw.textLeft(20, 350, "Last customer served");

		//draw in rectangle and text for today's events headlines
		StdDraw.rectangle(225, 630, 200, 35);
		StdDraw.textLeft(30, 650, "Today's Events:");

		
		//draw in rectangle for the minute/time
		StdDraw.rectangle(530, 320, 50, 30);
		font = new Font("SANS_SERIF", Font.PLAIN, 18);
		StdDraw.setFont(font);
		StdDraw.text(530, 330, "Minute");
		
		//draw in statistics table
		StdDraw.rectangle(830, 400, 100, 75);
		font = new Font("SANS_SERIF", Font.PLAIN, 10);
		StdDraw.setFont(font);
		StdDraw.text(830, 460, "Data Statistics");
		StdDraw.textLeft(750, 440, "Customers served: ");
		StdDraw.textLeft(750, 420, "Average Wait Time: ");
		StdDraw.textLeft(890, 420, "minutes");
		StdDraw.textLeft(750, 400, "Max Wait Time ");
		StdDraw.textLeft(880, 400, "minutes");
		StdDraw.textLeft(750, 380, "Average Tip: ");
		StdDraw.textLeft(890, 380, "dollars");
		StdDraw.textLeft(750, 360, "Total Tip Money: ");
		StdDraw.textLeft(890, 360, "dollars");
		StdDraw.setFont();
		
		//draw in images needed for the screen
		StdDraw.picture(1300, 200, "checkout.png",200,50);
		StdDraw.picture(550, 530, "path.jpeg", 560, 95,45);
		StdDraw.picture(800, 650, "exit.jpg", 200,100);
		StdDraw.picture(1190, 600, "logo.jpg", 390, 200);
		StdDraw.picture(1100, 400, "rack1.jpg", 200, 150);
		StdDraw.picture(1310, 370, "jans.jpg", 170, 150);
		StdDraw.picture(1110,270, "randShoppers.jpeg", 170,100);
	}

	/**
	 * 
	 * createCustomer - void method that creates a customer with a given id at given coordinates
	 * @param id - the id of the customer to draw
	 * @param x - the x coordinate of the center of the customer
	 * @param y - the y coordinate of the center of the customer
	 */
	public void createCustomer(int id, int x, int y)
	{
		//draw in the customer
		StdDraw.picture(x, y, "shopper.png", 50,100);
		
		
		
		//draw in the id in the top left of the image
		Font font = new Font("SANS_SERIF", Font.BOLD, 7);
		StdDraw.setFont(font);
		StdDraw.text(x-15, y+25, ""+id);
		StdDraw.setFont();
	}
	/**
	 * moveCustomerToEmployee - void method that moves the customer first in the queue to the employee
	 * @param id - the id of the customer to move
	 */
	public void moveCustomerToEmployee(int id)
	{
		//clear the customer first in the queue and the one currently with employee
		this.clearCustomer(25, 75);
		this.clearCustomer(215, 295);
		//add employee at coordinates next to employee
		this.createCustomer( id, 215, 295);
	}
	/**
	 * moveToExit method - moves the customer currently with employee to the exit sign
	 * @param id - id of customer to move
	 */
	public void moveToExit(int id)
	{
		//if id of the customer currently at first in queue is greater than 1, then the one currently with employee has the id one less than that
		if(id>1)
		{
			//clear customer currently with near exist sign and move the new one there
			this.clearCustomer(645, 530);
			this.createCustomer(id-1,645, 520);
		}
	}
	/**
	 * clearCustomer - void method that clears the customer at the given x,y coordinates
	 * @param x - x coord of center of customer
	 * @param y - y coord of center of customer
	 */
	public void clearCustomer(int x, int y)
	{
		//create filled white rectangle over the customer to clear it
		StdDraw.setPenColor(Color.WHITE);
		StdDraw.filledRectangle(x, y, 50, 50);
		StdDraw.setPenColor();
	}
	/**
	 * update the statistics on the screen based on information from store
	 * @param customersServed - an integer representing the total number of customers served
	 * @param waitTime - a double representing the the wait time 
	 * @param maxWait - the max wait time, int
	 * @param avTip - the average tip, an int
	 * @param totTip - total tip, an int
	 */
	public void updateStatistics(int customersServed, double waitTime, int maxWait, int avTip, int totTip)
	{
		//set font and update the data that is applicable
		Font font = new Font("SANS_SERIF", Font.PLAIN, 10);
		StdDraw.setFont(font);
		if(customersServed!=-1)
		{
			StdDraw.textLeft(860, 440, ""+customersServed);
		}
		if(waitTime!=-1)
		{
			StdDraw.textLeft(860, 420, "" + waitTime);
		}
		if(maxWait!=-1)
		{
			StdDraw.textLeft(860, 400, ""+maxWait);
		}
		if(avTip!=-1)
		{
			StdDraw.textLeft(860, 380, ""+avTip);
		}
		if(totTip!=-1)
		{
			StdDraw.textLeft(860, 360, ""+totTip);
		}
		StdDraw.setFont();
	}
	/**
	 * displayEvent method - shows the event in the text box on the screen
	 * @param s - the string to display
	 */
	public void displayEvent(String s)
	{
		//set font and display event
		Font font = new Font("SANS_SERIF", Font.PLAIN, 8);
		StdDraw.setFont(font);
		StdDraw.textLeft(30, nextLineY, s);
		nextLineY-=10;
	}
	/**
	 * clearEvent method - clears the text box of today's event
	 * will be called after every minute
	 */
	public void clearEvent()
	{
		StdDraw.setPenColor(Color.WHITE);
		StdDraw.filledRectangle(226, 621, 198, 24);
		StdDraw.setPenColor();
	}
	/**
	 * reset next line - void method to be called every minute to reset the spot to put the text
	 */
	public void resetNextLineY()
	{
		nextLineY=640;
	}
	/**
	 * pause method - pauses the screen for given time
	 * @param timeIncrement - the number of seconds to pause the screen for after each minute
	 */
	public void pause(double timeIncrement)
	{
		StdDraw.pause((int)timeIncrement*1000);
	}
	/**
	 * updateMinute method - updates the minute count after each minute
	 * @param minute - an integer representing the current time
	 */
	public void updateMinute(int minute)
	{
		//clear current minute
		StdDraw.setPenColor(Color.WHITE);
		StdDraw.filledRectangle(530, 310, 48, 10);
		StdDraw.setPenColor();
		//resest new minute
		Font font = new Font("SANS_SERIF", Font.PLAIN, 15);
		StdDraw.setFont(font);
		StdDraw.text(530, 310, ""+minute);
		StdDraw.setFont();
	}
	/**
	 * custOfDay method - reveals and circle the customer of the day!
	 * it's always Ms. Jans!
	 */
	public void custOfDay()
	{
		StdDraw.text(700, 220, "Customer of the day is...");
		StdDraw.setPenColor(Color.RED);
		StdDraw.setPenRadius(0.003);
		StdDraw.circle(1310,400, 50);
		StdDraw.setPenColor();
		StdDraw.setPenRadius();
		StdDraw.text(890, 220, "Ms. Jans!");
		StdDraw.setPenColor(Color.LIGHT_GRAY);
		StdDraw.filledRectangle(700, 100, 700, 75);
		StdDraw.setPenColor();
	}
}