# Mini-project #6 - Blackjack
""" Created BY Sarvagya Pant,IOE
Pulchow Campus,
Kathmandu Nepal"""
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
wins=0
loses=0
game_no=0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card=[]	# create Hand object

    def __str__(self):
        result=""
        for card in self.card:
            result += str(card)+' '
        return result# return a string representation of a hand

    def add_card(self, card):
        self.card.append(card)	# add a card object to a hand

    def get_value(self):
        value=0
        aces = False #Say no aces
        for card in self.card:
            value+=VALUES[card.get_rank()]
            if card.get_rank()=="A":
                aces=True
        if value+10<=21 and aces:
            value +=10
        return value
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        
            # compute the value of the hand, see Blackjack video
    def is_busted(self):  #Handling the bust in Game
        return self.get_value()>21
    def clear(self):
        self.cards = []
   
    def draw(self, canvas, pos, in_play):
        if not in_play:
            for i in range(len(self.card)):
                self.card[i].draw(canvas, [pos[0] + (i % 5) * 75, pos[1] + (i // 5) * 100])
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                              [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]],
                              CARD_BACK_SIZE)
            for i in range(1, len(self.card)):
                self.card[i].draw(canvas, [pos[0] + (i % 5) * 75, pos[1] + (i // 5) * 100])	   
 
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(s ,r) for s in SUITS for r in RANKS]
        self.i = -1
       
    def shuffle(self):
        self.i = -1
        random.shuffle(self.cards)
        
    def deal_card(self):        
        self.i -= 1        
        return self.cards.pop(len(self.cards)-1)
        # deal a card object from the deck
    
    def __str__(self):
        result=""
        #self.cards=self.cards[0:self.i].append(self.cards[self.i])        
        
        for card in self.cards:
            result += str(card)+" "
        return result
            # return a string representing the deck
        
#define event handlers for buttons
def deal():
    global outcome, in_play ,player_hand, dealer_hand, game_no
    player_hand=Hand()
    dealer_hand=Hand()
    deck.shuffle()
    game_no+=1
    if in_play:
        loses += 1
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    outcome = "Hit or stand?"
    in_play = True

def hit():
    global loses, outcome, in_play
    if in_play:
        player_hand.add_card(deck.deal_card())# if the hand is in play, hit the player
        if player_hand.is_busted():# if busted, assign a message to outcome, update in_play and score
            outcome = 'You have been busted. New Deal?'
            loses += 1
            in_play = False
        # replace with your code below

def stand():
    global wins,loses,outcome,in_play
    if in_play:
        in_play=False
        while dealer_hand.get_value()<17: # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.is_busted():
            wins+=1
            outcome = "You Won. Dealer is busted. New Deal?"
        elif dealer_hand.get_value()>=player_hand.get_value(): # compare the hand values
            loses+=1
            outcome = "You Lose. New Deal?"
        else :
            wins+=1
            outcome="You Won. New Deal?"
            
# draw handler    
def draw(canvas):
    canvas.draw_text("BlackJack", [25,25], 30, "Purple")    
    canvas.draw_text("Dealer", [10, 150], 30, "Black")
    canvas.draw_text("Player", [10, 400], 30, "Black")
    canvas.draw_text("Player :" + str(wins) , [375, 25], 24, "Black")
    canvas.draw_text("Dealer :" + str(loses) , [375,50],24,"Black")
    canvas.draw_text("Game No:" + str(game_no), [375, 70], 18, "Black")
    canvas.draw_text(outcome, [100, 300], 20, "White")
    #hands
    dealer_hand.draw(canvas, [100, 100], in_play)
    player_hand.draw(canvas, [100, 350], False)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")
howtoplay = """Get a Score of less than or equal to 21 without getting busted
Ace has value 1 or 11. Face cards has 10 and numbers with respective values.
Play Good !!!
\xa9 Sarvagya Pant,IOE,Pulchowk Campus,
Lalitpur , Nepal
"""

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label(howtoplay)
frame.set_draw_handler(draw)


# get things rolling
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()
deal()

frame.start()
# remember to review the gradic rubric