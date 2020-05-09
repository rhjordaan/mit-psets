import java.util.Collections;
import java.util.LinkedList;
import java.util.Queue;

/**
 * Sieve class - calculates the prime numbers up to a certain n and reports the results
 * @author Richter Jordaan
 * @version February 11, 2018
 *
 */
public class Sieve{
	private Queue<Integer> nums;
	private Queue<Integer> primeNums;
	boolean callMade;
	int lastN;
	private final long seed = System.currentTimeMillis();
	private long totalTime;
	
	/**
	 * Sieve constructor - instantiates the instance vars, including the numss
	 * 
	 */
	public Sieve()
	{
		nums = new LinkedList<Integer>();
		primeNums = new LinkedList<Integer>();
		callMade = false;
		lastN = 0;
	}
	
	/**
	 * findPrimes method - a void method that calculates the primes up to a certain n using Eratosthenes' method
	 * @param n - an integer representing the number is the last possible value of n for a prime
	 */
	public void findPrimes(int n)
	{
		nums.clear();
		primeNums.clear();
		lastN = n;
		callMade=true;
		if(n<2)
		{
			throw new IllegalArgumentException();
		}
		int p = 2;
		//create nums of possible primes
		long timeOffSet = System.currentTimeMillis();
		for(int i=2; i<=n; i++)
		{
			nums.add(i);
		}
		do
		{
			//if number isn't prime, add it back
			p = nums.remove();
			primeNums.add(p);
			
			int size = nums.size();
			for(int index = 0; index<size; index++)
			{
				int val = nums.remove();
				if(val%p!=0)
				{
					nums.add(val);
				}
			}
		}
		while(p<Math.sqrt(n) && !nums.isEmpty());
		while(!nums.isEmpty())
		{
			//add remaining values in original nums to primeNums
			primeNums.add(nums.remove());
		}
		totalTime += System.currentTimeMillis() - timeOffSet;
	}
	
	/**
	 * reportResults method - a void method that prints out the primes, the max n
	 * This method should report the primes to System.out. It throws an IllegalStateException 
	 * if no legal call has been made yet on the findPrimes method.
	 * 
	 */
	public void reportResults()
	{
		if(!callMade)
		{
			throw new IllegalStateException();
		}
		else
		{
			System.out.println("Max n: " + this.getMax());
			//make a copy so that primeNums is not destroyed
			Queue<Integer> copy = new LinkedList<Integer>();
			int i = 0;
			while(!primeNums.isEmpty())
			{
				int val = primeNums.remove();
				copy.add(val);
				//every 12 primes get a new line
				if(i%12==0)
				{
					System.out.println("");
					System.out.print(val + " ");
				}
				else
				{
					System.out.print(val + " ");
				}
				i++;
			}
			//don't destroy primeNums nums
			primeNums=copy;
		}
	}
	
	/**
	 * getMax method - returns the last value of n that was called for the findPrimes method 
	 * It throws an IllegalStateException if no legal call has been made yet 
	 * on the findPrimes method.
	 * @return an integer representing that last value of n that was called for the findPrimes method
	 */
	public int getMax()
	{
		if(!callMade)
		{
			throw new IllegalArgumentException();
		}
		return lastN;
	}
	
	/**
	 * getCount method - returns an integer representing the number of primes that was found in the last
	 * call to the findPrimes method
	 * It throws an IllegalStateException if no legal call has been made yet on the findPrimes method
	 * @return an integer representing the number of primes that were found on the last call of findPrimes
	 */
	public int getCount()
	{
		if(!callMade)
		{
			throw new IllegalStateException();
		}
		return primeNums.size();
	}
	public long getTime()
	{
		return totalTime;
	}
}
