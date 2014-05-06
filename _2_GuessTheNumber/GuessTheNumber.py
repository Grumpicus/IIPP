# http://www.codeskulptor.org/#user29_BpWnvJCGaD_1.py

import simplegui
import random

# initialize global variables
num_range = 100
target = 50
remain = 7

# helper function to start and restart the game
def new_game():
    global target, remain
    target = random.randrange(0,num_range)
    remain = 7 if num_range is 100 else 10
    print "New game. Range is from 0 to %d" % num_range
    print "Number of remaining guesses is %d\n" % remain

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    new_game()

def validate_guess(guess):
    g = -1 #initialize g just in case
    try:
        g = int(guess)
    except:
        print "%s is not a number!" % guess

    if g < 0 or g > num_range:
        print "Guess a number from 0 to %d" % num_range

    return g

def input_guess(guess):
    # Yes, this code could be more compact but
    # due to the way I want it to print,
    # I'm going to go with this
    global target, remain
    print "Guess was", guess
    g = validate_guess(guess) #returns -1 for invalid guesses

    #First check to see if they got it right
    if g == target:
        print "Correct!\n"
        new_game()
        return

    #If not, see if they are out of guesses
    remain = remain - 1
    if remain == 0:
        print "You ran out of guesses. The number was %d\n" % target
        new_game()
        return

    #No point in showing higher/lower if their guess was invalid
    if 0 < g < num_range:
        print "Higher!" if g < target else "Lower!"

    #I prefer to tell them how many guesses are remaining last
    print "Number of remaining guesses is %d\n" % remain

# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0, 100]", range100, 200)
f.add_button("Range is [0, 1000]", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game and start frame
new_game()

