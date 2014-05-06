# http://www.codeskulptor.org/#user30_XbptqQHHHc3YGNa.py

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
PAD_VEL = 5
VEL_ACC = 1.1
TOP_SPD = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global ball_color, PAD_VEL
    ball_pos = [WIDTH/2, HEIGHT/2]
    y_vel = (random.randrange(60, 180)/60) * -1 #always up
    x_vel = random.randrange(120, 240)/60
    if direction == LEFT:
        x_vel = x_vel * -1
    ball_vel = [x_vel, y_vel]

    #Reset
    ball_color = 'White'
    PAD_VEL = 5


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global TOP_SPD

    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0

    score1 = 0
    score2 = 0

    TOP_SPD = 0

    spawn_ball(random.choice([LEFT, RIGHT]))

def colorize(vel):
    global ball_color
    R = 'ff'
    v = max(0, get_vel_avg(vel)-2)
    d = min(510, int(v*50))
    G = ('0%s' % (hex(min(255,510-d))[2:]))[-2:]
    B = ('0%s' % (hex(max(0,255-d))[2:]))[-2:]
    #print R+G+B
    ball_color = R+G+B

def accelerate(cur_vel):
    global PAD_VEL, TOP_SPD
    cur_vel[0] = cur_vel[0]*VEL_ACC
    cur_vel[1] = cur_vel[1]*VEL_ACC
    #make sure we can keep up with the ball
    PAD_VEL = max(PAD_VEL,int(get_vel_avg(cur_vel))+1)
    TOP_SPD = max(TOP_SPD, get_vel_avg(cur_vel))
    colorize(cur_vel)
    return cur_vel

def get_vel_avg(vel):
    return (abs(vel[0])+abs(vel[1]))/2

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Add a little buffer to the collision detection due to visual effect of round ball
    pad_buffer = HALF_PAD_HEIGHT+(BALL_RADIUS/2)

    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= (paddle1_pos - pad_buffer) and ball_pos[1] <= paddle1_pos + pad_buffer:
            ball_vel[0] = -ball_vel[0]
            ball_vel = accelerate(ball_vel)
        else:
            score2 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] >= (paddle2_pos - pad_buffer) and ball_pos[1] <= paddle2_pos + pad_buffer:
            ball_vel[0] = -ball_vel[0]
            ball_vel = accelerate(ball_vel)
        else:
            score1 += 1
            spawn_ball(LEFT)
    elif (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", ball_color)

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= HALF_PAD_HEIGHT and (paddle1_pos + paddle1_vel) <= (HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel) >= HALF_PAD_HEIGHT and (paddle2_pos + paddle2_vel) <= (HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_polygon([(0, (paddle1_pos - HALF_PAD_HEIGHT)),
                   (PAD_WIDTH, (paddle1_pos - HALF_PAD_HEIGHT)),
                   (PAD_WIDTH, (paddle1_pos + HALF_PAD_HEIGHT)),
                   (0, (paddle1_pos + HALF_PAD_HEIGHT))], 1, 'White', 'White')
    canvas.draw_polygon([(WIDTH-PAD_WIDTH, (paddle2_pos - HALF_PAD_HEIGHT)),
                   (WIDTH, (paddle2_pos - HALF_PAD_HEIGHT)),
                   (WIDTH, (paddle2_pos + HALF_PAD_HEIGHT)),
                   (WIDTH-PAD_WIDTH, (paddle2_pos + HALF_PAD_HEIGHT))], 1, 'White', 'White')

    # draw scores
    offset = ((WIDTH/2)+PAD_WIDTH)/2
    canvas.draw_text(str(score1), (offset, 50), 36, 'White', 'sans-serif')
    canvas.draw_text(str(score2), (WIDTH - offset, 50), 36, 'White', 'sans-serif')

    canvas.draw_text('Cur: %s' % str(get_vel_avg(ball_vel)), (PAD_WIDTH+10, HEIGHT - 10), 12, '333333', 'sans-serif')
    canvas.draw_text('Top: %s' % str(TOP_SPD), (WIDTH/2+10, HEIGHT - 10), 12, '333333', 'sans-serif')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += -PAD_VEL
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += PAD_VEL
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel += -PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_VEL


def keyup(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP['w']) or (key == simplegui.KEY_MAP['s']):
        paddle1_vel = 0
    if (key == simplegui.KEY_MAP['up']) or (key == simplegui.KEY_MAP['down']):
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset', new_game, 50)

# start frame
new_game()
frame.start()

