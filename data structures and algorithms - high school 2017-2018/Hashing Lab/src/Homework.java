import java.awt.List;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

public class Homework {

	/*
	 * 
	 2)
	 
		public List<String> sortByFirstLetter(List<String> words)
		{
			ArrayList<Queue<String>> queues = new ArrayList<Queue<String>>(26);
			for(String s: words)
			{
				char letter = s.charAt(0);
				queues.get(letter-65).add(s);
			}
			LinkedList<String> sortedWords = new LinkedList<String>();
			for(int i = 0; i<queues.size(); i++)
			{
				Queue<String> q = queues.get(i);
				while(!q.isEmpty())
				{
					sortedWords.add(q.remove());
				}
			}
			return sortedWords;
		}
		
		
	 5)
	 hashing - using a hash function to convert the key into an integer that is used as an index into a hash table
	 chaining - technique that resolves collisions by turning each slot in the hash table into a "bucket" that can hold several values
	 hash function - algorithm that examines input data / values and returns a hash value
	 bucket - a slot that corresponds to a hash value where data is stored
	 collisions - when different keys are hashed into the same index
	 probing - a technique that stores the colliding objects in alternative slots chosen according to a predefined probing function
	 
	 6)
	 a) F - O(1)
	 b) T 
	 c) F - they are traversed based on their hash values, which isn't based on their ascending keys
	 d) T - for a relatively good hash function
	 
	 7)
	 
	 public boolean contains(Record record)
	 {
	 	int hashVal = record.hashCode();
	 	ListNode<Record> list = buckets[hashVal];
	 	while(list!=null)
	 	{
	 		if(list.getValue.equals(record))
	 		{
	 			return true;
	 		}
	 		list = list.getNext();
	 	}
	 	return false;
	 }
	 
	 8) is below
	 Overall the built in hash code was much more effective in reducing collisions, but my algorithm generally kept the number of collisions to under 10
	 */
	
	public void hashFunction()
	{
		String paragraph = "A hash table has sixty entries. Devise and test a function for English words such that all the different from this paragraph are hashed into with no more than four collisions. Do not call any hashCode methods.";
		String[] arr = new String[60];
		arr = paragraph.split(" ");
		
		ArrayList<LinkedList<String>> buckets = new ArrayList<LinkedList<String>>();
		for(int i = 0; i<arr.length; i++)
		{
			buckets.add(new LinkedList<String>());
		}
		for(String s: arr)
		{
			int index =((int) (Math.random()*14)*(((s.length()*13)+12) % 29 + 4) % 17) + (int)(Math.random()*15 + 4);
			//int index = Math.abs(s.hashCode()) % 60;
			LinkedList<String> list = buckets.get(index);
			if(list!=null)
			{
				list.addLast(s);
			}
			else
			{
				list = new LinkedList<String>();
				list.addFirst(s);
			}
		}
		
		int collisions = 0;
		for(int i = 0; i<buckets.size(); i++)
		{
			LinkedList<String> list = buckets.get(i);
			if(list!=null)
			{
				if(list.size()>1)
				{
					collisions++;
				}
			}
		}
		System.out.println("Collisions: " + collisions);
	}
	public static void main(String[] args)
	{
		Homework o = new Homework();
		o.hashFunction();
	}
}
