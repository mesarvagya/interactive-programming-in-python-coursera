# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import math;
import random;

# initialize global variables used in your code
comp_guess_1=0;
comp_guess_2=0;
choice=0;
steps_1=math.log(100-0+1)/math.log(2)
steps_1=math.ceil(steps_1)
steps_1=int(steps_1)
steps_2=math.log(1000-0+1)/math.log(2)
steps_2=math.ceil(steps_2);


def init():
    range100();
    
       
# define event handlers for control panel
    
def range100():
    global choice
    choice=1
    print "New Game. Range is from 0 to 100"
    global comp_guess_1
    comp_guess_1=random.randrange(0,100);
    print "Number of Guesses= ",steps_1
    print "Origianl Guess ",comp_guess_1
    print("\n")
    
    
    # button that changes range to range [0,100) and restarts

def range1000():
    global choice
    choice=2
    #Initialized the choice
    print "New Game. Range is from 0 to 1000"
    global comp_guess_2
    comp_guess_2=random.randrange(0,1000);
    print "Guess ",comp_guess_2 
    print("\n") 
    
def get_input(guess):
    guess=int(guess)
    global steps_1 #printed 7
    
    steps_1=steps_1-1 #printed 6 and so on
    print steps_1
    
    if (choice==1 and steps_1>0):
        print "Hello from if"
    else : "Print break"
    
init()  
get_input(90)
get_input(40)
get_input(90)
get_input(40)


 
          

