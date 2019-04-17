import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import java.util.regex.Pattern;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
/**
 * Whack-a-mole game using threads.
 * @author Karan Shah
 *
 */
public class Game implements ActionListener {
    /**
     * Instance variables for the text fields.
     */
    private JTextField textOne, textTwo;
    /**
     * Instance variable for the start button.
     */
    private JButton start;
    /**
     * Instance variable for the list of mole buttons.
     */
    private JButton[] buttons;
    /**
     * Instance variable for the scoreCount.
     */
    private int scoreCount;
    /**
     * Constructor for the Game.
     */
    public Game() {
        initComponents();
    }
    /**
     * Instance method that creates the whack-a-mole game.
     */
    private void initComponents() {
        //Font for buttons
        Font font = new Font(Font.MONOSPACED, Font.BOLD, 14);
        //Creating the frame
        JFrame frame = new JFrame("Whack-a-mole GUI");
        frame.setSize(650, 630);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        //Creating the main panel and panel for last row
        JPanel main = new JPanel();
        JPanel rowLast = new JPanel();
        //Instance variable for start button & adding ActionListener
        start = new JButton("Start");
        start.addActionListener(this);
        //Instance variables for text fields
        textOne = new JTextField(10);
        textTwo = new JTextField(10);
        //Time and Score is not modifiable
        textOne.setEditable(false);
        textTwo.setEditable(false);
        //Creating Labels
        JLabel time = new JLabel("Time Left:");
        JLabel score = new JLabel("Score:");
        //Adding labels, text fields, and button to last row
        rowLast.add(start);
        rowLast.add(time);
        rowLast.add(textOne);
        rowLast.add(score);
        rowLast.add(textTwo);
        //Creating the buttons for moles and adding to main panel
        int numHoles = 64;
        buttons = new JButton[numHoles];
        for (int i = 0; i < numHoles; i++) {
            buttons[i] = new JButton(":-(");
            buttons[i].setBackground(Color.RED);
            buttons[i].setFont(font);
            buttons[i].setOpaque(true);
            buttons[i].addActionListener(this);
            main.add(buttons[i]);
        // Adding last row to the main panel
        main.add(rowLast);
        //Setting windows content panel and making window visible
        frame.setContentPane(main);
        frame.setVisible(true);
        }
    }
    /**
     * actionPerformed method used to connect the events in game to actions.
     * @param event Events resulting from the game.
     */
    @Override
    public void actionPerformed(ActionEvent event) {
        if (event.getSource().equals(start)) {
            scoreCount = 0;
            textTwo.setText(Integer.toString(scoreCount));
            Thread gameTimer = new TimerThread(textOne, 20, start);
            gameTimer.start();
            Thread[] init = new Thread[buttons.length];
            for (int i = 0; i < buttons.length; i++) {
                Thread thread = new ButtonsThread(buttons[i], textOne);
                init[i] = thread;
            }
            for (int i = 0; i < init.length; i++) {
                init[i].start();
            }
        }
        for (JButton b:buttons) {
            if (event.getSource().equals(b)) {
                if (b.getBackground().equals(Color.BLUE)) {
                    scoreCount = scoreCount + 1;
                    textTwo.setText(Integer.toString(scoreCount));
                    b.setBackground(Color.GREEN);
                    b.setText(":-O");
                }
            }
        }
    }
    /**
     *
     * Private static inner class that creates timer thread.
     *
     */
    private static class TimerThread extends Thread {
        /**
         * Instance variable for time in text field.
         */
        private JTextField timeLeft;
        /**
         * Instance variable for counter.
         */
        private int counter;
        /**
         * Instance variable for start button.
         */
        private JButton beginButton;
        /**
         * Constructor for this class.
         * @param clock Time in text field.
         * @param time Amount of time to play the game.
         * @param starter Related to start button.
         */
        private TimerThread(JTextField clock, int time, JButton starter) {
            timeLeft = clock;
            counter = time;
            beginButton = starter;
        }
        /**
         * Over run method for thread class.
         */
        @Override
        public void run() {
            try {
               timeLeft.setText(Integer.toString(counter));
                while (counter > 0) {
                    beginButton.setEnabled(false);
                    Thread.sleep(1000);
                    counter = counter - 1;
                    timeLeft.setText(Integer.toString(counter));
                }
                Thread.sleep(5000);
                beginButton.setEnabled(true);
            } catch (InterruptedException e) {
                throw new AssertionError(e);
                }
            }
        }
    /**
     *
     * Private static inner class to create thread for each button.
     *
     */
    private static class ButtonsThread extends Thread {
        /**
         * Instance variable for button.
         */
        private JButton myButton;
        /**
         * Instance variable for the timer in the text field.
         */
        private JTextField myTimer;
        /**
         * Instance variable to generate initialize random.
         */
        private Random random = new Random();
        /**
         * Constructor for class.
         * @param butts Button.
         * @param time Timer in text field.
         */
        private ButtonsThread(JButton butts, JTextField time) {
            myButton = butts; 
            myTimer = time; 
        }
        /**
         * Over run method for thread class.
         */
        @Override
        public synchronized void run() {
            try {
                int counter = 20;
                while (counter > 0) {
                    int randomLightNum = random.nextInt(2);
                    if (randomLightNum == 0) {
                        myButton.setText(":-)");
                        myButton.setBackground(Color.BLUE);
                        Thread.sleep(2000);
                    } 
                    if (randomLightNum == 1) {
                            myButton.setText(":-(");
                            myButton.setBackground(Color.RED);
                            Thread.sleep(2000);
                    }
                    String element = myTimer.getText();
                    boolean isNumber = Pattern.matches("[0-9]+", element);
                    if (isNumber) {
                         counter = Integer.parseInt(element); 
                    }
                }
                if (counter == 0) {
                   myButton.setText(":-(");
                   myButton.setBackground(Color.RED);
                }
        } catch (InterruptedException e) {
            throw new AssertionError(e);
            }
        }
    }
    public static void main(String[] args){
        new Game();
    }
}
