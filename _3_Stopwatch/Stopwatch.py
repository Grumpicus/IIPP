# http://www.codeskulptor.org/#user30_FA9MfxUyzof9eUR_3.py

# template for "Stopwatch: The Game"
import simplegui

# frame and canvas global variables
square_frame_size = 200
margin = 10
score_size = 24

# other global variables
counter = 0
tries = 0
wins = 0

"""
since we're dynamically positioning the score
(in order to right-align it) we don't need to
recalculate score_pos for every draw event,
so we'll make the position a global variable
and only recalculate it when the score changes
"""
score_pos = [0,30] # only the second value matters; the first is (re)set by update_score()
score = "" # (re)set by update_score()

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    one_second = 10 # 1 tick = 100 milliseconds
    one_minute = one_second * 60
    minutes = t // one_minute
    seconds = t % one_minute // one_second
    tenths = t % one_minute % one_second
    return "%d:%02d.%d" % (minutes, seconds, tenths)

# use a function because this is called 3 different places
def update_score():
    global score, score_pos
    score = "%d/%d" % (wins, tries)
    score_pos[0] = square_frame_size - margin - frame.get_canvas_textwidth(score, score_size)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    if not timer.is_running(): # if the timer is already running, no need to do anything
        timer.start()

def stop():
    global tries, wins
    if timer.is_running(): # if the timer isn't running, no need to do anything
        timer.stop()
        tries += 1
        if counter % 10 == 0:
            wins += 1
        update_score()

def reset():
    global counter, tries, wins
    if timer.is_running():
        timer.stop()
    counter = tries = wins = 0
    update_score()

# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter), [60,110], 36, "White")
    canvas.draw_text(score, score_pos, score_size, "Green")

# create frame
frame = simplegui.create_frame("Stopwatch: The Game", square_frame_size, square_frame_size)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)

# start frame
update_score()
frame.start()
