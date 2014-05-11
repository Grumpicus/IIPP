# Mini-project #6 - Blackjack
import simplegui
import random

# constants
FRAME_SIZE = 600
TITLE = "Blackjack"
TITLE_SIZE = 50
TITLE_LOC = [200, 100]

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
CARD_IMAGES = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
SPACING = 5

DH_LOC = (50, 250)
PH_LOC = (50, 450)
TIP_OFFSET = 25
COL_1_OFFSET = 100
COL_2_OFFSET = 400
DH_LABEL_LOC = (DH_LOC[0], DH_LOC[1] - TIP_OFFSET)
INST_LOC = (DH_LABEL_LOC[0] + COL_1_OFFSET, DH_LABEL_LOC[1])
DH_TIP_LOC = (DH_LOC[0], DH_LOC[1] + CARD_SIZE[1] + TIP_OFFSET)
PH_LABEL_LOC = (PH_LOC[0], PH_LOC[1] - TIP_OFFSET)
OUTCOME_LOC = (PH_LABEL_LOC[0] + COL_1_OFFSET, PH_LABEL_LOC[1])
SCORE_LOC = (PH_LABEL_LOC[0] + COL_2_OFFSET, PH_LABEL_LOC[1])
PH_TIP_LOC = (PH_LOC[0], PH_LOC[1] + CARD_SIZE[1] + TIP_OFFSET)

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
CARD_BACK = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")
# +1 because the CARD_BACK is 2 pixels smaller
CARD_BACK_X = CARD_BACK_CENTER[0] + DH_LOC[0] + 1 + SPACING
CARD_BACK_Y = CARD_BACK_CENTER[1] + DH_LOC[1] + 1
CARD_BACK_POS = (CARD_BACK_X, CARD_BACK_Y)

in_play = False
outcome = ""
instructions = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(CARD_IMAGES, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)


# define hand class
class Hand:
    def __init__(self):
        self.contents = []

    def __str__(self):
        output = "Hand contains"
        for card in self.contents:
            output += " " + str(card)
        return output

    def add_card(self, card):
        self.contents.append(card)

    def get_value(self):
        total = 0
        has_ace = False
        for card in self.contents:
            total += VALUES[card.get_rank()]
            has_ace = has_ace or (card.get_rank() == "A")

        if not has_ace:
            return total
        else:
            if total + 10 > 21:
                return total
            else:
                return total + 10

    def draw(self, canvas, pos):
        x = pos[0] - CARD_SIZE[0]
        for card in self.contents:
            x += CARD_SIZE[0] + SPACING
            y = pos[1]
            card.draw(canvas, [x, y])


# define deck class
class Deck:
    def __init__(self):
        self.contents = []
        for suit in SUITS:
            for rank in RANKS:
                self.contents.append(Card(suit, rank))
                #self.shuffle()

    def shuffle(self):
        random.shuffle(self.contents)

    def deal_card(self):
        return self.contents.pop()

    def __str__(self):
        output = "Deck contains"
        for card in self.contents:
            output += " " + str(card)
        return output


#define event handlers for buttons
def deal():
    global outcome, instructions, in_play, deck, dh, ph, score

    if in_play:
        outcome = "Hand unfinished. You lost."
        score -= 1
    else:
        outcome = ""

    deck = Deck()
    deck.shuffle()

    dh = Hand()
    ph = Hand()

    ph.add_card(deck.deal_card())
    dh.add_card(deck.deal_card())
    ph.add_card(deck.deal_card())
    dh.add_card(deck.deal_card())

    instructions = "Hit or stand?"
    in_play = True


def hit():
    global outcome, instructions, in_play, score

    if in_play:
        instructions = "Hit or stand?"
        outcome = ""
        ph.add_card(deck.deal_card())
        if ph.get_value() > 21:
            outcome = "Busted! Dealer won."
            in_play = False
            score -= 1
            instructions = "New deal?"


def stand():
    global outcome, instructions, in_play, score
    if in_play:
        while dh.get_value() < 17:
            dh.add_card(deck.deal_card())

        if dh.get_value() > 21:
            outcome = "Dealer busted! You won!"
            score += 1
        elif dh.get_value() >= ph.get_value():
            outcome = "Dealer won."
            score -= 1
        else:
            outcome = "You won!"
            score += 1
        in_play = False
        instructions = "New deal?"


# draw handler
def draw(canvas):
    # title
    canvas.draw_text(TITLE, TITLE_LOC, TITLE_SIZE, "Black", "sans-serif")

    # dealer hand
    dh.draw(canvas, DH_LOC)
    if in_play:
        canvas.draw_image(CARD_BACK, CARD_BACK_CENTER, CARD_BACK_SIZE, CARD_BACK_POS, CARD_BACK_SIZE)
    else:
        # dealer tooltip
        canvas.draw_text(str(dh.get_value()), DH_TIP_LOC, 12, "Black")
    # dealer labels
    canvas.draw_text("Dealer", DH_LABEL_LOC, 24, "Black")
    canvas.draw_text(outcome, OUTCOME_LOC, 24, "Black")

    # player hand
    ph.draw(canvas, PH_LOC)
    # player tooltip
    canvas.draw_text(str(ph.get_value()), PH_TIP_LOC, 12, "Black")
    # player labels
    canvas.draw_text("Player", PH_LABEL_LOC, 24, "Black")
    canvas.draw_text(instructions, INST_LOC, 24, "Black")
    canvas.draw_text("Score: %d" % score, SCORE_LOC, 24, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", FRAME_SIZE, FRAME_SIZE)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit", hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# We can't do this until the frame is created
TITLE_LOC[0] = (FRAME_SIZE - frame.get_canvas_textwidth(TITLE, TITLE_SIZE, "sans-serif")) / 2

# get things rolling
deal()
frame.start()