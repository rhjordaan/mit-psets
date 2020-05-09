import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;

/**
 *this is the Controller component
 *It draws the window that will run forest fire simulation
 *It creates the view and adds it to the window.
 *It creates the model that will solve the fire problem
 *
 *@author
 *@version
 *
 **/

public class Fire extends JFrame
{

    private FireView view;
    private FireModel model;

    Fire()
    {
        super("Forest Fire");

        // build the view
        view = new FireView(); //create the view component
        view.setBackground(Color.white);
        Container c = getContentPane();
        c.add(view, BorderLayout.CENTER);

        // build the model
        model = new FireModel(view);
    }
    public void run()
    {
    	model.solve();
    }
    

    
    public static void main(String[] args)
    {
        Fire smokey = new Fire();
        smokey.addWindowListener(new WindowAdapter()
                                 {
                                     public void windowClosing(WindowEvent e)
                                     {
                                         System.exit(0);
                                     }
                                 }
                                );
        smokey.setSize(570, 640);
        smokey.show();
        smokey.run();
    }
}

