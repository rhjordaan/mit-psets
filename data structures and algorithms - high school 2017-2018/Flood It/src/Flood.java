

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;


/**
 * This is the Controller component
 * It creates the window with the colored grid
 * the buttons for choosing colors
 * and launches the main program
 * @author Richter Jordaan
 * @version March 15, 2018
 *
 */
class Flood extends JFrame implements ActionListener
{

	private static final long serialVersionUID = 1L;
	private JButton redButton, greenButton, blueButton, yellowButton, pinkButton, blackButton;
	private FloodView view;
    private FloodModel model;
    JLabel label;
    JPanel topPanel;
    boolean extraColors;
    /**
     * Create the buttons, view and model
     * add the buttons in the controlPanel
     */
    Flood()
    {
        super("Flood It!");
        extraColors = false;
        JPanel controlPanel = 
            new JPanel(new FlowLayout(FlowLayout.CENTER));
        
        topPanel = 
                new JPanel(new FlowLayout(FlowLayout.CENTER));

        //build all the color buttons
        redButton = new JButton("Red");
        redButton.addActionListener(this);
        redButton.setEnabled(true);
        redButton.setBackground(Color.RED);
        redButton.setOpaque(true);
        controlPanel.add(redButton);
        
        greenButton = new JButton("Green");
        greenButton.addActionListener(this);
        greenButton.setEnabled(true);
        greenButton.setBackground(Color.GREEN);
        greenButton.setOpaque(true);
        controlPanel.add(greenButton);
        

        blueButton = new JButton("Blue");
        blueButton.addActionListener(this);
        blueButton.setEnabled(true);
        blueButton.setBackground(Color.BLUE);
        blueButton.setOpaque(true);
        controlPanel.add(blueButton);
        
        yellowButton = new JButton("Yellow");
        yellowButton.addActionListener(this);
        yellowButton.setEnabled(true);
        yellowButton.setBackground(Color.YELLOW);
        yellowButton.setOpaque(true);
        controlPanel.add(yellowButton);
        
        
        // build the view
        view = new FloodView();
        setSize(650, 650);
        view.setBackground(Color.white);
        
        //get level of difficulty, add buttons and create model accordingly
        
        String[] possibleChoices = { "Easy", "Medium", "Hard", "Custom" };
        String difficulty = (String)(JOptionPane.showInputDialog(null,
        		"Choose your difficulty:", "",
        		JOptionPane.INFORMATION_MESSAGE, null,
        		possibleChoices, possibleChoices[0]));
        
        int size=0;
        int turns = 0;
        if(difficulty.equals("Custom"))
        {
        	size = Integer.parseInt(JOptionPane.showInputDialog("What size screen do you want?"));
        	turns = Integer.parseInt(JOptionPane.showInputDialog("How many turns do you want?"));
        	extraColors = JOptionPane.showInputDialog("Do you want two additional colors? Enter 'Yes' or 'No'").equals("Yes");
        }
        
        if(difficulty.equals("Easy"))
        {
            model = new FloodModel(view,1,0,0,false);
        }
        else if(difficulty.equals("Medium"))
        {
            model = new FloodModel(view,2,0,0,false);
        }
        else if(difficulty.equals("Hard"))
        {
        	extraColors = true;
            model = new FloodModel(view,3,0,0,true);
           
            
        }
        else
        {
        	model = new FloodModel(view,4,size,turns,extraColors);
        }
        if(extraColors)
        {
        	 pinkButton = new JButton("Pink");
             pinkButton.addActionListener(this);
             pinkButton.setEnabled(true);
             pinkButton.setBackground(Color.PINK);
             pinkButton.setOpaque(true);
             controlPanel.add(pinkButton);
             
             blackButton = new JButton("Black");
             blackButton.addActionListener(this);
             blackButton.setEnabled(true);
             blackButton.setBackground(Color.BLACK);
             blackButton.setOpaque(true);
             controlPanel.add(blackButton);
        }
        
        Container c = getContentPane();
        c.add(controlPanel, BorderLayout.SOUTH);
        c.add(view, BorderLayout.CENTER);
        c.add(topPanel,BorderLayout.NORTH);
        

        //make label for the tries display
        label = new JLabel("Tries: " + model.getTries() + " out of " + model.TURNS);
        topPanel.add(label);
    }
    


    /* 
     * Listen for a button clicked event
     * depending on which button is clicked, call the
     * makeMove method with correct color
     * if game is over, disable all the buttons
     */
    public void actionPerformed(ActionEvent e)
    {
    	//see what color is requested and make the move
        JButton b = (JButton)e.getSource();
        int val = 0;
        if(b == redButton)
        {
        	val = FloodCell.RED;
        }
        else if(b == greenButton)
        {
        	val = FloodCell.GREEN;
        }
        else if(b == blueButton)
        {
        	val = FloodCell.BLUE;
        }
        else if(b == yellowButton)
        {
        	val = FloodCell.YELLOW;
        }
        else if( b == pinkButton)
        {
        	val = FloodCell.PINK;
        }
        else
        {
        	val = FloodCell.BLACK;
        }
        //if game is over disable buttons and display appropriate message
        if(model.makeMove(val))
        {
        	redButton.removeActionListener(this);
        	greenButton.removeActionListener(this);
        	yellowButton.removeActionListener(this);
        	blueButton.removeActionListener(this);
        	if(extraColors)
        	{
        		blackButton.removeActionListener(this);
            	pinkButton.removeActionListener(this);
        	}
        	if(model.getTries()>=model.TURNS)
        	{
        		JOptionPane.showMessageDialog(null, "You are out of turns. You lose!");
        	}
        	else
        	{
        		JOptionPane.showMessageDialog(null, "You win! Congratulations.");
        	}
        }  
        label.setText("Tries: " + model.getTries() + " out of " + model.TURNS);
        topPanel.add(label);
        
    }
    
    
    public static void main(String[] args)
    {
        Flood floodGame = new Flood();
        floodGame.setDefaultCloseOperation(EXIT_ON_CLOSE);
        floodGame.setVisible(true);
    }
}
