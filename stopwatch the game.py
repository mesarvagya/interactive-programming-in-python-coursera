# template for "Stopwatch: The Game"
import simplegui
# define global variables
duration=100
msg=""
count=0
toshowx=0
toshowy=0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(count):
    milli=count%10;
    count=count-milli;
    count=count/10;
    sec=count%60;
    count=count-sec;
    count=count/60;
    minu=count%60;
    global msg    
    if sec<10:
        milli=str(milli)
        sec=str(sec)
        minu=str(minu)
        msg = minu + ":"+ "0" + sec + "." + milli
        #print msg
    else :
        milli=str(milli)
        sec=str(sec)
        minu=str(minu)
        msg = minu + ":"+ sec + "." + milli
        #print msg
    return msg
# define event handlers for buttons; "Start", "Stop", "Reset"
def start() :
    
    timer.start()
    #print "ok from start"
   
    
def stop() :
    global count, toshowx, toshowy
    if (count % 10 ) == 0:
        toshowx+=1
        toshowy+=1
    else : toshowy+=1
        
   # print count
    timer.stop()
   # print "ok from stop"
    
def reset() :
    timer.stop()
    global msg,count,toshowx, toshowy
    print "ok from reset"
    count=0
    toshowx=0
    toshowy=0
    msg = format(count)
    frame.set_draw_handler(draw)

# define event handler for timer with 0.1 sec interval
def tock():
    global count
    count+=1
    msg=format(count)
    
    
def draw(canvas):
    showxy = str(toshowx) + "/" + str(toshowy)
    canvas.draw_text(showxy, (200,50), 30 , "Red" )
    canvas.draw_text(msg, (70,150), 80, "White")
    

# define draw handler

    
# create frame
frame=simplegui.create_frame("Stopwatch",300,300)
# register event handlers
frame.add_button("Start", start, 50)
frame.add_button("Stop", stop, 50)
frame.add_button("Reset", reset, 50)
# start timer and frame
timer=simplegui.create_timer(duration,tock)
frame.set_draw_handler(draw)
frame.start()

# Please remember to review the grading rubric