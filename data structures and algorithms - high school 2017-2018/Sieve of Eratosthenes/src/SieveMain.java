// This program computes all the prime numbers up to a given integer n.  It
// uses the classic "Sieve of Eratosthenes" to do so.

import java.util.*;

public class SieveMain {
    public static void main(String[] args) {
        System.out.println("This program computes all prime numbers up to a");
        System.out.println("maximum using the Sieve of Eratosthenes.");
        System.out.println();
        Scanner console = new Scanner(System.in);
        Sieve s = new Sieve();
        for(;;) {
            System.out.print("Maximum n to compute (0 to quit)? ");
            int max = console.nextInt();
            if (max == 0)
                break;
            System.out.println();
            s.findPrimes(max);
            //first make sure reportResults throws exception if findPrimes hasn't been called yet
           s.reportResults();
          //also make sure getMax and getCount throws exception if findPrimes hasn't been called yet
            int count = s.getCount();
            int maxVal = s.getMax();
            int percent = count * 100 / maxVal;
            System.out.println("\n% of primes = " + percent);
            
            //test efficiency of Sieve vs Sieve2
            System.out.println("Time taken to compute for Queue: " + s.getTime());
            Sieve2 s2 = new Sieve2();
            s2.findPrimes(max);
            System.out.println("Time taken to compute for ArrayDeque: " + s2.getTime());
            if(s.getTime()<s2.getTime())
            {
            	System.out.println("Queue is faster");
            }
            else if(s.getTime()>s2.getTime())
            {
            	System.out.println("ArrayDeque is faster");
            }
            else
            {
            	System.out.println("The Queue and ArrayDeque are equally fast");
            }
            System.out.println();

            
        }
    }
}