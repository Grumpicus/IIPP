# http://www.codeskulptor.org/#user31_HjZgYNHUT7_2.py

# implementation of card game - Memory

import simplegui
import random

cards = range(8) + range(8)

# helper function to initialize globals
def new_game():
    global exposed, state, first, second, turns
    random.shuffle(cards)
    exposed = [False for i in range(16)]
    state = 0
    first = 0
    second = 0
    turns = 0
    label.set_text("Turns = %s" % turns)


# define event handlers
def mouseclick(pos):
    global state, first, second, turns
    i = pos[0] // 50
    if not exposed[i]:
        exposed[i] = True
        if state == 0:
            first = i
            state = 1
        elif state == 1:
            second = i
            turns += 1
            label.set_text("Turns = %s" % turns)
            state = 2
        elif state == 2:
            if cards[first] != cards[second]:
                exposed[first] = exposed[second] = False
            first = i
            state = 1
        else:
            print "ERROR: UNEXPECTED STATE"


# cards are logically 50x100 pixels in size
def draw(canvas):
    offset = -50
    for i in range(16):
        offset += 50
        canvas.draw_text(str(cards[i]), [offset+14,65], 42, "White")
        if exposed[i]:
            canvas.draw_polyline([(offset,0),(offset+50,0),(offset+50,100),(offset,100),(offset,0)], 2, "Yellow")
        else:
            canvas.draw_polygon([(offset,0),(offset+50,0),(offset+50,100),(offset,100)], 2, "Yellow", "Green")
            #canvas.draw_text(str(i), [offset+5,14], 12, "Yellow")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

