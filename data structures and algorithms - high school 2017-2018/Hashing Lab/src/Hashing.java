import java.awt.dnd.peer.*;
import java.awt.color.*;
import java.awt.font.*;
import java.io.*;
import java.util.Scanner;

public class Hashing{
  HashTable table;

  final int TABLESIZE = 600;

  public Hashing(){
    table = new HashTable(1);
  }

  public void search(){
    int idToFind;
    Item location;

    Scanner console = new Scanner(System.in);

    System.out.println("Testing search algorithm\n");
    System.out.print("Enter Id value to search for (-1 to quit) --> ");
    idToFind = console.nextInt();

    while (idToFind >= 0){
      location = (Item)table.find(new Item(idToFind, 0));
      if (location == null)
        System.out.println("Id = " + idToFind + "  No such part in stock");
      else
        System.out.println("Id = " + location.getId() +
                           "  Inv = " + location.getInv());
     System.out.println();
    
      System.out.println("Enter Id value to search for (-1 to quit) --> ");
      idToFind = console.nextInt();
    }
    this.stats();
  }
  
  /**
 * stats method - void method that prints out the statistics associated with the run of searches
 * statistics demonstrate how effective the hashing function was
 */
public void stats()
  { 
      System.out.println("Capacity: " + table.getCapacity());
      System.out.println("Hashcode of Item: id % 100");
     
	  System.out.println("Number of null pointers: " + table.getNumberOfNulls());
	  System.out.println("Percentage of null pointers: " + (table.getNumberOfNulls()/(double)table.getCapacity())*100);
	 
	  System.out.print("Average length of linked list: ");
	  System.out.printf("%.2f", table.getAvLength());
	  System.out.println("");
	  System.out.println("Longest linked list length: " + table.getLongestList());
	  System.out.print("Load factor for the table: ");
	  System.out.printf("%.2f", (double)table.getSize()/table.getCapacity());
	  System.out.println("\n");
  }

  public void loadFile(){
    Scanner inFile;

    String fileName = "file400.txt";
    int id, inv;
	try{

	    inFile = new Scanner(new File(fileName));
	
	    int howMany = inFile.nextInt();
	    for (int k = 1; k <= howMany; k++){
	      id = inFile.nextInt();
	      inv = inFile.nextInt();
	      table.add(new Item(id, inv));
	    }
    }catch(IOException i){
    	System.out.println("Error: " + i.getMessage());
    }
  }
  public static void main(String[] args)
  {
	  Hashing obj = new Hashing();
	  obj.loadFile();
	  obj.search();
  }
}