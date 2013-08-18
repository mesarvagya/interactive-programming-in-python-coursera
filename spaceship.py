# program template for Spaceship
''' Created by Sarvagya Pant, IOE, Pulchowk Campus
Kathmandu
'''
import simplegui
import math
import random

# globals for user interface
WIDTH,HEIGHT = 800,600
siz=[WIDTH,HEIGHT]
score,lives,time = 0,3,0
#required constants
d_angle_vel,acc,dec=math.pi/30,12/60,.6/60
CLOCKWISE_ROTATION = {simplegui.KEY_MAP["left"] : False, simplegui.KEY_MAP["right"] : True}
ROCK_ANG_VEL = (-math.pi/15, math.pi/15)
ROCK_VEL = (-5, 5)

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.thrusted_image_center = [self.image_center[0] + self.image_size[0],
                                      self.image_center[1]]
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, self.thrusted_image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                          self.pos, self.image_size, self.angle)     

    def update(self):
        
        for d in range(2):
            self.vel[d]*=(1-dec)
        if self.thrust:
            vector = angle_to_vector(self.angle)
            for d in range(2):
                self.vel[d]+=acc*vector[d]
        for d in range(2):
            self.pos[d] = (self.pos[d] + self.vel[d]) % siz[d]
        
        self.angle += self.angle_vel
        
    def change_angle_vel(self,is_clockwise,down):
        if down:
            if is_clockwise:
                self.angle_vel += d_angle_vel
            else:
                self.angle_vel -= d_angle_vel
        else:
            if is_clockwise:
                self.angle_vel -= d_angle_vel
            else:
                self.angle_vel += d_angle_vel
                
    def have_thruster(self):
        self.thrust = not self.thrust
        if self.thrust:
            ship_thrust_sound.play()
            sound.start()
        else:
            sound.stop()
            ship_thrust_sound.rewind()
    def shoot(self):
        global a_missile
        vector=angle_to_vector(self.angle)
        start_x = self.pos[0] + self.image_center[0] * vector[0]
        start_y = self.pos[1] + self.image_center[0] * vector[1]
        x_vel = self.vel[0] + math.sqrt(2) * vector[0]
        y_vel = self.vel[1] + math.sqrt(2) * vector[1]
        a_missile = Sprite([start_x, start_y], [x_vel, y_vel], 0, 0, missile_image, missile_info, missile_sound)
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle )
    
    def update(self):
        for d in range(2):
            self.pos[d] = (self.pos[d] + self.vel[d]) % siz[d]
        self.angle +=self.angle_vel    
        

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    #drawing lives and score
    canvas.draw_text("Lives", [20, 30], 20, "White")
    canvas.draw_text(str(lives), [20, 60], 20, "White")
    
    canvas.draw_text("Score", [720, 30], 20, "White")
    canvas.draw_text(str(score), [720, 60], 20, "White")
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    x_vel=random.randrange(ROCK_VEL[0],ROCK_VEL[1])
    y_vel=random.randrange(ROCK_VEL[0],ROCK_VEL[1])
    angle=random.random()*2*math.pi
    angle_vel=random.random() * (ROCK_ANG_VEL[1] - ROCK_ANG_VEL[0]) + ROCK_ANG_VEL[0]
    a_rock = Sprite([WIDTH * random.random(), HEIGHT * random.random()], [x_vel, y_vel], angle,angle_vel, asteroid_image, asteroid_info)
    
    
def sound_restart():
    ship_thrust_sound.rewind()
    ship_thrust_sound.play()

    
def down(key):
    if key in CLOCKWISE_ROTATION.keys():
        my_ship.change_angle_vel(CLOCKWISE_ROTATION[key], True)
    if key == simplegui.KEY_MAP["up"]:
        my_ship.have_thruster()
    if key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def up(key):
    if key in CLOCKWISE_ROTATION.keys():
        my_ship.change_angle_vel(CLOCKWISE_ROTATION[key], False)  
    if key == simplegui.KEY_MAP["up"]:
        my_ship.have_thruster()
    
        
    
    # initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], -math.pi/2, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.31, 0.21], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)
msg=''' To run press arrow keys. Spacebar shoots the missiles
Sarvagya Pant
'''
frame.add_label(msg)

timer = simplegui.create_timer(1000.0, rock_spawner)
sound = simplegui.create_timer(25000.0, sound_restart)


# get things rolling
timer.start()
frame.start()
