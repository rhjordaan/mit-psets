/**
 *  Lesson 31 Ordered List
 *  This class will test the Ordered List Class
 *
 * @author     K Jans
 * @created    January 16, 2018
 */

import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class OrderedList
{
    private Scanner console;

    /**
     * Constructor - creates the Scanner
     */
    public OrderedList()
    {
        console = new Scanner(System.in); 
    }


    /**
     * Search the list for an item
     * @param list - head of linked list
     */
    public void testFind(SinglyLinkedList<Item> list)
    {
        int idToFind;
        Item location;

        System.out.println("Testing search algorithm\n");
        System.out.print("Enter Id value to search for (-1 to quit) --> ");
        idToFind = console.nextInt();

        while (idToFind >= 0)
        {
            location = ((Item)list.find(new Item(idToFind, 0)));
            if (location == null)
                System.out.println("Id = " + idToFind + "  No such part in stock");
            else
                System.out.println(location);
            System.out.println();
            System.out.print("Enter Id value to search for (-1 to quit) --> ");
            idToFind = console.nextInt();
        }
        console.nextLine(); //eat up white space in scanner
    }

    /**
     * Delete an item from the list
     * @param list - head of linked list
     */
    public void testDelete(SinglyLinkedList<Item> list)
    {
        int idToDelete;

        System.out.println("Testing delete algorithm\n");
        System.out.print("Enter Id value to delete (-1 to quit) --> ");
        idToDelete = console.nextInt();

        while (idToDelete >= 0)
        {
            Item idInvItem = new Item(idToDelete, 0);

            if (!list.remove(idInvItem))
                System.out.println("Id# " + idToDelete + "  No such part in stock");
            else
                System.out.println("     Id #" + idToDelete + " was deleted");
            System.out.println();
            System.out.print("Enter Id value to delete (-1 to quit) --> ");

            idToDelete = console.nextInt();
        }
        console.nextLine(); //eat up white space in scanner
    }

    /**
     * Create a linked list from the data in a file
     * @param list - 
     */
    public void readData(SinglyLinkedList<Item> list)
    {
        FileReader inFile;

        String fileName = "file20.txt";
        int id, inv;
        try {
            inFile = new FileReader(fileName);
            Scanner readFile = new Scanner(inFile);

            int howMany = readFile.nextInt();
            for (int k = 1; k <= howMany; k++)
            {
                id = readFile.nextInt();
                inv = readFile.nextInt();
                list.insert(new Item(id, inv));
            }
            readFile.close();


        }
        catch (IOException e)
        {
            System.out.println("Error processing file"+ e);
        }
    }

    public void mainMenu (SinglyLinkedList<Item> head)
    {
        String choice;
        console = new Scanner(System.in);

        do
        {
        	System.out.print("noah is dumb");
            System.out.println("Linked List algorithm menu\n");
            System.out.println("(1) Read data from disk");
            System.out.println("(2) Print ordered list");
            System.out.println("(3) Search list");
            System.out.println("(4) Delete from list");
            System.out.println("(5) Clear entire list");
            System.out.println("(6) Count nodes in list");
            System.out.println("(7) Print list backwards");
            System.out.println("(Q) Quit\n");
            System.out.print("Choice ---> ");
            choice = console.nextLine() + " ";  // kludge to ensure choice.charAt(0) > 0

            System.out.println();

            if ('1' <= choice.charAt(0) && choice.charAt(0) <= '7')
            {
                switch (choice.charAt(0))
                {
                case '1' :
                    readData(head);
                    System.out.println(head);
                    break;
                case '2' :
                    System.out.println();
                    System.out.println("The List printed inorder\n");
                    head.printList();
                    System.out.println();
                    break;
                case '3' :
                    testFind(head);
                    break;
                case '4' :
                    testDelete(head);
                    break;
                case '5' :
                    head.clear();
                    break;
                case '6' :
                    System.out.println("Number of nodes = " + head.size ());
                    System.out.println();
                    break;
                case '7' :
                    head.printBackwards();
                    break;
                }
            }
        }
        while (choice.charAt(0) != 'Q' && choice.charAt(0) != 'q');
    }

    public static void main(String[] args)
    {
        OrderedList test = new OrderedList();
        SinglyLinkedList<Item> list = new SinglyLinkedList<Item>();

        test.mainMenu (list);
    }
}