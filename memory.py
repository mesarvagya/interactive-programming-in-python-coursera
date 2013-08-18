# implementation of card game - Memory

import simplegui
import random

deck = range(0, 8) + range(0, 8)

# helper function to initialize globals
def init():
    global exposed, state, moves
    state = 0
    moves = 0
    label.set_text("Moves = "+str(moves))
    random.shuffle(deck)
    exposed = [False] * 16
     
# define event handlers
def mouseclick(pos):
    global state, exposed, card1, card2, moves
    i = pos[0] // 50
    if state == 0:        
        if exposed[i] == False:
            exposed[i] = True
            card1 = i
            state = 1
    elif state == 1:
        if exposed[i] == False:
            exposed[i] = True
            card2 = i
            state = 2
            moves += 1
            label.set_text("Moves = "+str(moves))
    elif state == 2:       
        if exposed[i] == False:
            if deck[card1] != deck[card2]:
                exposed[card1] = False
                exposed[card2] = False
                card1 = i
                if exposed[i] == False:
                    exposed[i] = True 
                state = 1
            else:
                exposed[card1] = True
                exposed[card2] = True
                card1 = i
                if exposed[i] == False:
                    exposed[i] = True 
                state = 1                          
    
def draw(canvas):
    global state
    draw_pos = [-35,63]
    card_posx = 50   
    for i in range(len(deck)):
            draw_pos[0] += 50
            if exposed[i]:
                    canvas.draw_text(str(deck[i]), draw_pos, 35, "#A09A68", "sans-serif")
            else:
                    shift_factor = i+1
                    canvas.draw_polygon([
                                         [card_posx * shift_factor - card_posx, 0],
                                         [card_posx * shift_factor, 0],
                                         [card_posx * shift_factor, 100],
                                         [card_posx * shift_factor - card_posx, 100]
                                         ], 4, "#2C9287", "#00438A")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
