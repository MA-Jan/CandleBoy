# Game Name: CandleBoy
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
# Author: Jeffrey Ray
# Start Date: 09/03/2020
# End Date: 13/04/2020
# File Name: Master_Copy.py
# Description: 2D Platformer, collapsing field of view, orbs of light restore vision, orbs fill light bar, use light to attack enemies, beat all 6 sewers

# CODING INFORMATION:
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
# use "DP!" to indicate a line is only for Debugging-Purposes, these lines can be deleted or commented out later - ctr-f "DP!"
# all objects, items, enemies, ect. should be contained in classes

import pygame, math, time, random

pygame.init() # This will initiate PyGame, and allow you to then make various commands with PyGame

# --- GLOBAL VARIABLES ---
#width = 
#height = 
#c_screen = ()

# temporary display, ratio (4:3)
# this display will be used to construct / arrange graphics, and will be resized to fit screen
display_width = 800
display_height = 600 # constant dimensions of screen
center_screen = (display_width//2,display_height//2)

gameDisplay = pygame.display.set_mode((display_width, display_height)) # Define our display (in pixels)
pygame.display.set_caption('CandleBoy') # Window Title

clock = pygame.time.Clock() # Game Clock
fps = 60 # Game will run at 60 frames/s (use fps to refernce)

scroll_time = 15 # seconds for section to move off screen completely
screen_speed = math.ceil( display_width / (scroll_time * fps))

fall_screen = 1.5 # time (s) it takes to fall height of game window
# Sum of Arithmetic Series - https://www.mathsisfun.com/algebra/sequences-sums-arithmetic.html
# display_height = n/2 * (2a(n-1)*d)
# d = ? (common difference)
# a = d
n = fall_screen * fps # frames to fall screen (total # of terms)
# display_height = n/2 * 2(n-1) * d^2
# display_height / n(n-1) = d^2

# Gravity = d (additional distance added each frame)
default_gravity = math.sqrt(display_height / (n*(n-1)))
# 600 = 45 * (178d^2)
# d = ∴ 0.2736902757519867
# 1.50 seconds to fall screen - max. fall speed is 25pix/s (after 90frames)

# slower fall speed (for wall sliding)
fall_screen = 6.0
n = fall_screen * fps
slide_speed = display_height / n # constant

gravity = default_gravity # this is the universal gravity (affects everything)

# --- COLORS ---
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255) 
yellow = (255,255,0) 
cyan = (0,255,255) 
magenta = (255,0,255) # pure colors
dark_blue = (0,52,102)
dark_red = (153,0,0)
cb_yellow = (255,235,59)

# --- WORLDS ---
worlds = {1: (), 2: (), 3: (), 4: (), 5: (), 6: (), 7: ()} # list of all world NAMES, 0 is basic set
# each world has 3 subworlds
# WORLD 1
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 2
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 3
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 4
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 5
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 6
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# WORLD 0
n1 = 'Forgotten Forest'
n2 = ''
n3 = ''
# clean-up
del n1; del n2; del n3

# --- GRAPHICS ---
# load graphics here: ex. image_variable = pygame.image.load('myGraphic.png')
# Background:
background_tilesheet = pygame.image.load(r'Graphics\Candleboy_Background_Sheet.png').convert_alpha()
background_set = [] # see the .pdn background sheet for reference*
for y in range(10):
    for x in range(3):
        new_sprite = background_tilesheet.subsurface((x*1600,y*600,1600,600))
        background_set.append(new_sprite)
# Player:
candleboy_spritesheet = pygame.image.load(r'Graphics\Candleboy_Player_Spritesheet.png').convert_alpha()
candleboy_player = candleboy_spritesheet.subsurface(0,0,38,58)
candleboy_player_rev = candleboy_spritesheet.subsurface(0,58,38,58)
candleboy_shooting = candleboy_spritesheet.subsurface(0,232,38,58)
candleboy_shooting_rev = candleboy_spritesheet.subsurface(38,232,38,58)

candleboy_walking = [] # right walking animation sprites
for x in range(1,5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,0,38,58)
    candleboy_walking.append(new_sprite)
candleboy_walking_rev = [] # left walking animation sprites
for x in range(1,5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,58,38,58)
    candleboy_walking_rev.append(new_sprite)
candleboy_jumping = [] # 0-up, 1-down
for x in range(2):
    new_sprite = candleboy_spritesheet.subsurface(x*38,116,38,58)
    candleboy_jumping.append(new_sprite)
candleboy_jumping_rev = [] # 0-up, 1-down
for x in range(2):
    new_sprite = candleboy_spritesheet.subsurface(x*38,174,38,58)
    candleboy_jumping_rev.append(new_sprite)
candleboy_sliding = [] # 0-up, 1-neutral, 2-down
for x in range(2,5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,116,38,58)
    candleboy_sliding.append(new_sprite)
candleboy_sliding_rev = [] # 0-up, 1-neutral, 2-down
for x in range(2,5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,174,38,58)
    candleboy_sliding_rev.append(new_sprite)
candleboy_dying = [] # in order (first to last)
for x in range(5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,290,38,58)
    candleboy_dying.append(new_sprite)
candleboy_dying_rev = [] # in order (first to last)
for x in range(5):
    new_sprite = candleboy_spritesheet.subsurface(x*38,348,38,58)
    candleboy_dying_rev.append(new_sprite)
candleboy_dead = candleboy_spritesheet.subsurface(114,232,38,58)
candleboy_dead_rev = candleboy_spritesheet.subsurface(152,232,38,58)

# Status Bar:
status_bar = pygame.image.load(r'Graphics\Candleboy_Statusbar.png').convert_alpha()
score_spritesheet = pygame.image.load(r'Graphics\Candleboy_Score.png').convert_alpha()
score_title = score_spritesheet.subsurface((0,37,55,17)) # load pieces of spritesheet to permanent memory
number_0 = score_spritesheet.subsurface((0,0,12,11))
number_1 = score_spritesheet.subsurface((12,0,7,11))
number_2 = score_spritesheet.subsurface((19,0,11,11))
number_3 = score_spritesheet.subsurface((30,0,10,11))
number_4 = score_spritesheet.subsurface((0,12,11,11))
number_5 = score_spritesheet.subsurface((11,12,11,11))
number_6 = score_spritesheet.subsurface((22,12,11,11))
number_7 = score_spritesheet.subsurface((33,12,10,11))
number_8 = score_spritesheet.subsurface((0,24,11,11))
number_9 = score_spritesheet.subsurface((11,24,11,11))
comma = score_spritesheet.subsurface((22,24,4,13))
lightbar = pygame.image.load(r'Graphics\Candleboy_Lightbar.png').convert()
# Score(x4):
big_score_spritesheet = pygame.image.load(r'Graphics\Candleboy_Big_Score.png').convert()
big_score_title = big_score_spritesheet.subsurface((0,164,220,36))
big_number_0 = big_score_spritesheet.subsurface((0,0,48,44))
big_number_1 = big_score_spritesheet.subsurface((48,0,32,44))
big_number_2 = big_score_spritesheet.subsurface((80,0,40,44))
big_number_3 = big_score_spritesheet.subsurface((120,0,40,44))
big_number_4 = big_score_spritesheet.subsurface((0,48,44,44))
big_number_5 = big_score_spritesheet.subsurface((44,48,44,44))
big_number_6 = big_score_spritesheet.subsurface((88,48,44,44))
big_number_7 = big_score_spritesheet.subsurface((132,48,40,44))
big_number_8 = big_score_spritesheet.subsurface((0,96,44,44))
big_number_9 = big_score_spritesheet.subsurface((44,96,44,44))
big_comma = big_score_spritesheet.subsurface((88,96,16,52))
# Platforms:
platform_spritesheet = pygame.image.load(r'Graphics\Candleboy_Platform_Spritesheet.png').convert_alpha()
ground_tile = platform_spritesheet.subsurface((0,100,800,100))
green_block = platform_spritesheet.subsurface((0,0,50,50))
purple_block = platform_spritesheet.subsurface((50,0,50,50))
brown_block = platform_spritesheet.subsurface((100,0,50,50))
blue_block = platform_spritesheet.subsurface((150,0,50,50))
white_block = platform_spritesheet.subsurface((200,0,50,50))
black_block = platform_spritesheet.subsurface((250,0,50,50))
main_platform_block = green_block # default
falling_platform_block = platform_spritesheet.subsurface((0,50,50,50))
moving_platform_block = platform_spritesheet.subsurface((50,50,50,50))
spike_sprite = platform_spritesheet.subsurface((150,50,50,50))
passable_platform = platform_spritesheet.subsurface((200,50,50,20)) # height=20
slippery_platform = platform_spritesheet.subsurface((300,0,50,50))
# Enemies:
enemy_spritesheet = pygame.image.load(r'Graphics\Candleboy_Enemy_Spritesheet.png').convert_alpha()
tormentor_sprites = [] # Tormentor
for x in range(5):
    new_sprite = enemy_spritesheet.subsurface((x*140,0,140,61))
    tormentor_sprites.append(new_sprite)
tormentor_sprites_rev = []
for x in range(5):
    new_sprite = enemy_spritesheet.subsurface((x*140,61,140,61))
    tormentor_sprites_rev.append(new_sprite)
tormentor_damaged = enemy_spritesheet.subsurface((273,312,140,61))
tormentor_damaged_rev = enemy_spritesheet.subsurface((413,312,140,61))
purple_ghost_sprites = [] # purple ghost
for x in range(5):
    new_sprite = enemy_spritesheet.subsurface((x*78,122,78,42))
    purple_ghost_sprites.append(new_sprite)
purple_ghost_sprites_rev = []
for x in range(5):
    new_sprite = enemy_spritesheet.subsurface((x*78,164,78,42))
    purple_ghost_sprites_rev.append(new_sprite)
pink_ghost_sprites = [] # pink ghost
for x in range(6):
    new_sprite = enemy_spritesheet.subsurface((x*78,206,78,42))
    pink_ghost_sprites.append(new_sprite)
pink_ghost_sprites_rev = []
for x in range(6):
    new_sprite = enemy_spritesheet.subsurface((x*78,248,78,42))
    pink_ghost_sprites_rev.append(new_sprite)
transformed_ghost_sprites = [] # transformed ghost
for x in range(2):
    new_sprite = enemy_spritesheet.subsurface((x*60,290,60,24))
    transformed_ghost_sprites.append(new_sprite)
transformed_ghost_sprites_rev = []
for x in range(2,4):
    new_sprite = enemy_spritesheet.subsurface((x*60,290,60,24))
    transformed_ghost_sprites_rev.append(new_sprite)
abyss_sprites = [] # abyss
for x in range(5):
    new_sprite = enemy_spritesheet.subsurface((x*50,314,50,59))
    abyss_sprites.append(new_sprite)
# Projectiles/Misc.
misc_spritesheet = pygame.image.load(r'Graphics\Candleboy_Miscellaneous.png').convert_alpha()
shadow_orb_small = []
for x in range(2):
    new_sprite = misc_spritesheet.subsurface((x*12,54,12,12))
    shadow_orb_small.append(new_sprite)
shadow_orb_large = []
for x in range(4):
    new_sprite = misc_spritesheet.subsurface((x*24,66,24,24))
    shadow_orb_large.append(new_sprite)
lightbeam_sprite = misc_spritesheet.subsurface((0,45,23,9))
orb_sprites = []
for x in range(3):
    new_sprite = misc_spritesheet.subsurface((x*44,0,44,44))
    orb_sprites.append(new_sprite)
# Menu Buttons
buttons_spritesheet = pygame.image.load(r'Graphics\Candleboy_Buttons.png').convert_alpha()
active_start = buttons_spritesheet.subsurface((0,0,250,60))
inactive_start = buttons_spritesheet.subsurface((250,0,250,60))
active_controls = buttons_spritesheet.subsurface((0,60,220,46))
inactive_controls = buttons_spritesheet.subsurface((220,60,220,46))
active_retry = buttons_spritesheet.subsurface((1,146,143,39))
inactive_retry = buttons_spritesheet.subsurface((147,146,143,39))
active_quit = buttons_spritesheet.subsurface((0,106,112,40))
inactive_quit = buttons_spritesheet.subsurface((112,106,112,40))
active_main_menu = buttons_spritesheet.subsurface((0,181,247,38))
inactive_main_menu = buttons_spritesheet.subsurface((247,181,247,38))
active_back = buttons_spritesheet.subsurface((239,106,112,40))
inactive_back = buttons_spritesheet.subsurface((375,106,112,40))
# Menu Titles
game_over_title = pygame.image.load(r'Graphics\Candleboy_Game_Over.png').convert_alpha()
# Main Menu
main_menu_spritesheet = pygame.image.load(r'Graphics\Candleboy_Main_Menu.png').convert_alpha()
title_screen_set = []
for x in range(13):
    new_sprite = main_menu_spritesheet.subsurface((x*800,0,800,600))
    title_screen_set.append(new_sprite)
title_screen_set_rev = []
for x in range(13):
    new_sprite = main_menu_spritesheet.subsurface((x*800,600,800,600))
    title_screen_set_rev.append(new_sprite)
# Entrances - regular (6)
purple_entrance = title_screen_set[0]
green_entrance = title_screen_set[5]
blue_entrance = title_screen_set_rev[0]
brown_entrance = title_screen_set_rev[5]
pink_entrance = title_screen_set_rev[6]
gray_entrance = title_screen_set[9]
# - alternates (foil) (5)
alt_red_entrance = title_screen_set[6]
alt_purple_entrance = title_screen_set[7]
alt_green_entrance = title_screen_set[8]
alt_blue_entrance = title_screen_set_rev[7]
alt_brown_entrance = title_screen_set_rev[8]
alt_gray_entrance = title_screen_set_rev[9]
# - special (2)
special_entrace_1 = title_screen_set[12]
special_entrance_2 = title_screen_set_rev[12]
# - player overlays (2 sets of 6)
player_overlays = [title_screen_set[1],title_screen_set[2],title_screen_set[3],title_screen_set[4],title_screen_set[10],title_screen_set[11]]
player_overlays_rev = [title_screen_set_rev[1],title_screen_set_rev[2],title_screen_set_rev[3],\
    title_screen_set_rev[4],title_screen_set_rev[10],title_screen_set_rev[11]]
# Menu Animations
scary_face_red = pygame.image.load(r'Graphics\Candleboy_Scary_Face.png').convert()
scary_face_purple = pygame.image.load(r'Graphics\Candleboy_Scary_Face_Purple.png').convert() # can make trasparent, but transparent background turns black
large_ghost_img = pygame.image.load(r'Graphics\Candleboy_Big_Ghost.png').convert_alpha()
cloud_background = pygame.image.load(r'Graphics\Candleboy_Cloud_Overlay.png').convert()
# Controls Menu
controls_menu_img = pygame.image.load(r'Graphics\Candleboy_Controls_Menu.png').convert_alpha()

del new_sprite
del x
del y

# --- Music/SFX ---
# load audio here: ex. main_theme = pygame.mixer.music.load('mySong.mp3')
# load sfx here: ex. effect_1 = pygame.mixer.Sound('sound.wav')


# --- CLASSES ---
class Entity(): # for all physical objects
    def __init__(self,pos,w=0,h=0,img=None): # pos=(x,y) w=width, h=height, img=Filepath_of_Image
        self.x = pos[0]
        self.y = pos[1]
        # use the dimensions of the passed image by default
        if w == 0 and h == 0:
            try:
                self.width = img.get_width()
                self.height = img.get_height()
            except:
                print('No dimensions found for ' + str(self)) # no image or width/height
        else:
            self.width = w
            self.height = h
        self.image = img  # Load the image
        self.hitbox = Hitbox(pos,self.width,self.height) # Create a hitbox - bound by topleft
        self.color = yellow # display color when debugging
        self.air_vel = 0 # additional speed travelled on screen

    def draw(self):
        if self.image:
            gameDisplay.blit(self.image,(self.x,self.y)) # copy the entity's graphic to the screen
        else:
            pygame.draw.rect(gameDisplay, self.color, (self.x,self.y,self.width,self.height)) # DP!

class Hitbox(): # used to determine collision for entities
    def __init__(self,pos,w,h):
        # Hitbox initially has the same dimensions as the entity which contains it
        self.x = pos[0]
        self.y = pos[1]
        self.width = w
        self.height = h
        self.color = red

    def draw(self): # DP!
        pygame.draw.rect(gameDisplay,self.color,(self.x,self.y,self.width,self.height))


class Player(Entity):
    def __init__(self,pos,w=0,h=0,img=None):
        super(Player,self).__init__(pos,w,h,img) # inherit all attr of Entity
        # OVERIDE the player's hitbox size (don't include shooting arm)
        self.hitbox.width = 29 # 38 is true width
        self.hitbox.height = 50 # 58 is true height
        self.hitbox.y += 8 # anchor the hitbox to the bottom of candleboy
        self.offset = self.width - self.hitbox.width # 9

        self.alive = True
        self.dead = False # when alive and dead are both false, player is dying (animation)
        self.hp = 1 #! death after 1 hit
        self.difficulty = 0
        self.spawn_point = (100,display_height - 100 - self.height) # starting position
        # move hitbox RELATIVE ++
        x_change = self.spawn_point[0] - self.x
        y_change = self.spawn_point[1] - self.y
        self.x += x_change
        self.y += y_change
        self.hitbox.x += x_change
        self.hitbox.y += y_change

        self.spritesheet = candleboy_spritesheet # contains all animation poses for the player

        run_screen = 3.5 # (s) to run width of screen
        self.run_speed = display_width / (run_screen*fps) # defualt pixels moved per frame
        self.dir = 0 # 1 or -1 (direction Left or Right) only in x-axis, 0 represent no motion
        self.falling = True
        self.fall_speed = 0
        self.jumping = False
        self.wall_jumping = False
        self.wall_slide = False
        self.slipping = False # alternative to wall slide, you cannot wall jump/slide
        self.has_wall = 0 # -1=left, 0=none, 1=right
        self.can_jump = True # cannot jump again without releasing the jump button

        self.jump_release = False # fall early
        self.jump_time = 0 # before quick release
        self.fast_gravity = 0 # the increased gravity will make you complete your junp path faster

        # Jump Time
        # only activate gravity after jump is done accelerating
        n = jump_time * fps # (total # of terms)
        d = gravity

        jump_height = 150 # Jump Height (pixels) = gravity(↓↓) + jumpspeed(↑)
        # Physics Acceleration Equations - https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/a/what-are-the-kinematic-formulas
        # Vf^2 = Vo^2 + 2aΔy
        # 0 = s^2 -2gh
        # 2gh = s^2
        # s =  ? (jump_speed)

        # Jump Speed = s (velocity up)
        self.jump_speed = math.sqrt(2*gravity*jump_height) # constant*

        # Jump Time
        # Δy = Vot + 1/2*at^2
        # 0 = s*n + 1/2(-g*n^2)
        # s/(1/2g) = n
        # n / fps = seconds
        self.full_jump_time = self.jump_speed / (1/2 * gravity) / fps #  time it takes to complete a FULL jump (up and down) depends on gravity


        self.vel = [0,0] # distance to be travelled in the (x,y) axis
        self.color = red # Player is red when debugging

        # Animation
        self.face_right = True # determines the direction the player faces in the X-AXIS (the player faces the right by defualt)
        self.walking = False
        self.shooting = False # is the player currently shooting
        self.shooting_frames = 0.25*fps
        self.shooting_counter = 0
        seconds = 0.5 # time it takes animation to complete
        self.walking_frames = seconds*fps / 4 # number of frames each walking position will appear before changing
        self.walking_counter = 0
        self.walking_index_dir = 1 # forwards (-1 for backwards)
        seconds = 0.75 #!
        self.dying_frames = seconds*fps / 5
        self.dying_counter = 0
        self.animation_index = 0 # position of sprite in list


        self.charges = 5 # available bullets or ammo (shooting cond. based on lightbar not ammo) - max of 5 on screen
        self.light_beams = [] # list of bullets
        self.reload_1 = 0.25 # after first shot
        self.reload_2 = 0.75 # after every burst of shots
        self.max_burst = 2 # longer reload time every 2 shots in a row
        self.consecutive_shots = 1 # the first shot is the reference (it is consecutive)
        self.hold_shot = False # was shooting being held down - shot at the first available frame to shoot
        self.reload_time = self.reload_1 # seconds before you can shoot again
        self.reload_counter = 0 # tracks frames before player can shoot

        # Radius of the player field of view, not covered by darkness
        self.max_visibility = 450
        self.min_visibility = 80
        self.visible_radius = 200 # start the game with THIS visibility (44% filled)
        self.temporary_radius = 25 # when the game starts, the radius quickly grows to the correct value - starting from this
        self.radius_growth = (self.visible_radius-self.temporary_radius) / 2 * fps # 2 seconds to fill

        self.light_filled = 100 * (self.visible_radius / self.max_visibility) # percent of light bar filled
        self.default_diminish_speed = 4 # percent of light lost per second (25! seconds to lose completely)
        self.diminish_speed = self.default_diminish_speed
        self.beam_cost = 7 # percent of light lost when a bullet is shot
        self.orb_light = 21 # percent that an orb fills the light bar (5! orbs to complete fill)
        self.orbs_collected = 0 # tally total orbs

        self.enemies_slain = 0 # tracks enemies killed
        self.sections_cleared = 0 # tracks sections the player has passed
        self.elapsed_time = 0 # tracks the duration of the run
        self.score = 0 # total points earned by the player

    def calculate_score(self):
        self.score = 5 * self.elapsed_time # 5 points per second
        self.score += 50 * self.orbs_collected
        self.score += 100 * self.sections_cleared
        self.score += 150 * self.enemies_slain
        self.score = int(self.score)
        return self.score
    
    def update_time(self):
        self.elapsed_time += 1/fps

    def calc_gravity(self): # fast gravity for quick release
        # Δy = Vot + 1/2 at^2
        # 2*(Δy - Vot)/t^2 = a
        y = 0 # the top of jump path is where ever the jump was RELEASED, (if released)
        vo = self.jump_speed
        t = self.jump_time # time of release
        #a = ? (gravity)
        a = 2*(y-vo*t)/t**2
        self.fast_gravity = a

    def choose_image(self,controls): # determines which pose of the player to use, based on player's state
        # Candleboy's spritesheet is split into lists of animation cycles
        # controls - represents if a control button was pressed this frame
        # FIND THE STATE of the player:
        selected_image = None #@
        animating = False # is the image static or part of a set

        if not self.alive: # Death Animation
            # choose an animation set to use
            if self.face_right:
                dying_animations = candleboy_dying
            else:
                dying_animations = candleboy_dying_rev

            if self.animation_index == 5: # ALL animation frames completed
                self.dead = True # player is done dying, now they are dead
                if self.face_right:
                    selected_image = candleboy_dead
                else:
                    selected_image = candleboy_dead_rev
            else: # in the process of dying
                animating = True
                selected_image = dying_animations[self.animation_index] # choose image
                self.dying_counter += 1 # increase animation counter
                if self.dying_counter >= self.dying_frames:
                    self.dying_counter = 0
                    self.animation_index += 1 # advance animation sprite
                    
        elif self.shooting: # shooting, overrides all actions (only 1 sprite)
            if self.face_right:
                selected_image = candleboy_shooting
            else:
                selected_image = candleboy_shooting_rev
            self.shooting_counter += 1
            if self.shooting_counter >= self.shooting_frames: # timer
                self.shooting_counter = 0
                self.shooting = False

        # Air motion
        elif self.vel[1] <= 0 and (self.jumping or self.wall_jumping): # jumping up - you can jump without going up
            if self.has_wall == -1: # left of wall
                selected_image = candleboy_sliding[0]
            elif self.has_wall == 1: # right of wall
                selected_image = candleboy_sliding_rev[0]
            else: # no wall
                if self.face_right:
                    selected_image = candleboy_jumping[0]
                else:
                    selected_image = candleboy_jumping_rev[0]

        elif self.vel[1] > 0 and self.falling: # falling down - there is 1 frame of falling without speed
            if self.has_wall == -1: # left of wall
                selected_image = candleboy_sliding[2]
            elif self.has_wall == 1: # right of wall
                selected_image = candleboy_sliding_rev[2]
            else: # no wall
                if self.face_right:
                    selected_image = candleboy_jumping[1]
                else:
                    selected_image = candleboy_jumping_rev[1]

        # Ground motion
        elif controls and not self.jumping and not self.falling and not self.wall_jumping: # Walking [x] only
            if self.has_wall == -1: # left of wall
                selected_image = candleboy_sliding[1]
            elif self.has_wall == 1: # right of wall
                selected_image = candleboy_sliding_rev[1]
            else: # no wall - WALKING CYCLE
                animating = True
                # choose an animation set to use
                if self.face_right:
                    walking_animations = candleboy_walking
                else:
                    walking_animations = candleboy_walking_rev
                selected_image = walking_animations[self.animation_index] # choose image
                #print(self.animation_index) #DP!
                self.walking_counter += 1 # increase animation counter
                if self.walking_counter >= self.walking_frames:
                    self.walking_counter = 0
                    self.animation_index += self.walking_index_dir # advance animation sprite
                    # change animation direction
                    if self.animation_index == 3:
                        self.walking_index_dir = -1
                    elif self.animation_index == 0:
                        self.walking_index_dir = 1

        # Basic - not moving
        elif self.vel == [0,0] and (not self.falling and not self.jumping and not self.wall_jumping): # Stationary
            if self.face_right:
                selected_image = candleboy_player
            elif not self.face_right:
                selected_image = candleboy_player_rev
            else:
                print('ERROR-SPRITE 1')
        else:
            print('SPRITE FAILED') # no state recognized

        # if player is not currently in an animation cycle, reset the index to start from the beginning of the next cycle entered
        if not animating:
            self.animation_index = 0
            self.walking_index_dir = 1 # reset the direction of walking

        # Finally upload the desired image
        self.image = selected_image
            
    def turn_right(self):
        self.face_right = True
        self.x += self.offset # bump back to the right

    def turn_left(self):
        self.face_right = False
        self.x -= self.offset # bump back to the left

    def update_direction(self):
        if self.dir == 1 and not self.face_right: # turn right
            self.turn_right()
        elif self.dir == -1 and self.face_right: # turn left
            self.turn_left()
        else:
            # not moving - keep using previous direction
            pass

        # now re-align the player's hitbox
        self.update_hitbox()

    def update_hitbox(self): # [x] realign
        if self.face_right: # hitbox aligns to the left of the player
            self.hitbox.x = self.x
        elif not self.face_right: # hitbox aligns to the right of player
            self.hitbox.x = self.x + self.width - self.hitbox.width
        else:
            print('ERROR-FACE DIRECTION')
            
    def update_vel(self):
        x = self.run_speed * self.dir
        y = self.fall_speed
        if self.jumping or self.wall_jumping:
            y -= self.jump_speed # constant (gravity varies)
        # update player's velocity
        self.vel = [x,y]

    def enforce_gravity(self):
        if (self.falling or self.jumping or self.wall_jumping) and not self.wall_slide: # falling or any jumping
            if self.jump_release: # jump release
                self.fall_speed += self.fast_gravity # fall faster
            else:
                self.fall_speed += gravity # normal gravity
        elif self.wall_slide: # sliding
            self.fall_speed = slide_speed
            self.jumping = False # jumping stops when you slide
            self.wall_jumping = False
        else:
            self.fall_speed = 0 # stationary [y]

    def move(self): # move player & hitbox coordinates based on velocity
        # x-direction
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        if self.hitbox.x < 0: # player got forced off screen (squished between screen and block)
            self.die()
        # y-direction
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]

    def check_priority(self,key_priority,new_priority):
        execute = False # determines if the target is important enough to execute
        if key_priority != None:
            if new_priority <= key_priority:
                execute = True
        else:
            execute = True
        return execute

    def update_priority(self,platforms):
        self.priority_x = 0 # default 0, lower values are more important - highest priority in the x-axis
        self.priority_y = 0 # highest priority in the y-axis
        # define player bounds
        my_left = self.hitbox.x + self.vel[0]
        my_right = self.hitbox.x + self.hitbox.width + self.vel[0]
        my_top = self.hitbox.y + self.vel[1]
        my_bottom = self.hitbox.y + self.hitbox.height + self.vel[1]
        my_sides = [my_top,my_bottom,my_left,my_right]
        # pixels between the side of a surface and the side of the player
        closest_side_vertical = None # smallest vertical distance (horizontal sides)
        closest_side_horizontal = None # smallest horizontal distance (vertical sides)
        # ONLY for top of platforms
        full_contact = False # determines if the player is completely on the top of a STATIONARY platform

        for p in platforms:
            # define paltform bounds
            p_left = p.hitbox.x
            p_right = p.hitbox.x + p.hitbox.width
            p_top = p.hitbox.y
            p_bottom = p.hitbox.y + p.hitbox.height
            p_moving = hasattr(p,'path') # the platform is a moving platform if it has a specified path
            p_sides = [p_top,p_bottom,p_left,p_right] # top, bot, left, right
            
            # stationary/moving platforms
            p.priority[0] = 0
            p.priority[1] = 0

            # Whichever platform is closest to the player will take priority
            # TOP and BOTTOM
            for side_index in range(2):
                if my_left < p_right and my_right > p_left: # x-axis intercept

                    if closest_side_vertical == None:
                        closest_side_vertical = p_sides[side_index]
                    else:
                        if side_index == 0: # to get the opposite side (ex. left gets right, right gets left)
                            my_index = 1
                        elif side_index == 1:
                            my_index = 0
                        else:
                            print('ERROR-123124')

                        if abs(p_sides[side_index] - my_sides[my_index]) < closest_side_vertical:
                            closest_side_vertical = abs(p_sides[side_index] - my_sides[my_index])
                            # this platform has the new closest side (top/bottom)
                            self.priority_y -= 1 # create a new highest priority value
                            p.priority[1] = self.priority_y

                        # ONLY for top of platforms - if more than one platform are at the same vertical distance
                        elif abs(p_sides[side_index] - my_sides[my_index]) == closest_side_vertical and side_index == 0:
                            # if its a stationary platform, the player must be fully contained by it (not half on, half off)
                            if not p_moving and my_left > p_left and my_right < p_right:
                                # This surface takes priority
                                full_contact = True
                                self.priority_y -= 1 # create a new highest priority value
                                p.priority[1] = self.priority_y
                            # its a moving platform and the player is not completely secured on a stationary platform
                            elif p_moving and not full_contact:
                                self.priority_y -= 1 # create a new highest priority value
                                p.priority[1] = self.priority_y

            # LEFT and RIGHT
            for side_index in range(2,4):
                if my_top < p_bottom and my_bottom > p_top: # y-axis intercept

                    if closest_side_horizontal == None:
                        closest_side_horizontal = p_sides[side_index]
                    else:
                        if side_index == 2: # to get the opposite side (ex. left gets right, right gets left)
                            my_index = 3
                        elif side_index == 3:
                            my_index = 2
                        else:
                            print('ERROR-123123')

                        if abs(p_sides[side_index] - my_sides[my_index]) < closest_side_horizontal:
                            closest_side_horizontal = abs(p_sides[side_index] - my_sides[my_index])
                            # this platform has the new closest side (left/right)
                            self.priority_x -= 1 # create a new highest priority value
                            p.priority[0] = self.priority_x

    def check_platform(self,plat): # when touching platform (all sides but bottom):
        # this is where the SPECIAL ATTRIBUTES of a platform goes
        if hasattr(plat,'dark'): # DARK platform
            if plat.dark:
                self.diminish_speed = plat.drain
        else:
            self.diminish_speed = self.default_diminish_speed #
        if hasattr(plat,'fall_speed'): # FALLING platform
            plat.triggered = True # activate the falling platform
        if hasattr(plat,'slippery'): # wall jump?
            if plat.slippery:
                self.slipping = True

    def update_clipsize(self,previous_size,new_size):
        # clip sizes cannot be less than 0 (absolute), a clip size of 0 indicates NO adjustments must be made
        # always keep the smaller clip size, because that platform must be closest to the player
        # the closer the object, the more of a priority it is

        # the most critical value is a number as close to zero as possible, without reaching 0
        previous_size_abs = abs(previous_size)
        new_size_abs = abs(new_size)
        if previous_size == 0:
            clipsize = new_size
        elif new_size_abs < previous_size_abs:
            clipsize = new_size
        elif new_size_abs >= previous_size_abs:
            clipsize = previous_size
        else:
            print('ERROR-CLIP SIZE')
        return clipsize

    def detect_surfaces(self,blocks): # for platforms/walls
        # define bounds of player's hitbox
        my_height = self.hitbox.height
        my_width = self.hitbox.width
        my_left = self.hitbox.x
        my_right = self.hitbox.x + my_width
        my_top = self.hitbox.y
        my_bottom = self.hitbox.y + my_height

        has_ground = False # determines whether the player resting on a surface or is falling
        full_contact_ground = False # if the player is fully contained by a surface (NOT half-on, half-off)
        riding_platform = None # the platform that the player is riding (if any)
        self.has_wall = 0 # determines if a vertical surface is right next to a player
        self.slipping = False # determines if the player cannot hold on to a wall
        # changes made to the player's coordinates (none by default)
        x_change = 0
        y_change = 0
        # determines whether the player can move in each direction
        x_vel = self.vel[0]
        y_vel = self.vel[1]

        # check if player is interacting with an impassable object, and adjust their position accordingly
        for b in blocks: # check for all blocks
            block_height = b.height
            block_width = b.width
            block_top = b.y
            block_bottom = b.y + b.height
            block_left = b.x
            block_right = b.x + b.width
            passable_block = b.passable
            if hasattr(b,'path'): # is an entity riding this platform, default is no
                b.rider = None

            # SPACIAL POSITIONING relative to block
            above = False
            below = False
            east = False
            west = False

            if my_left < block_right and my_right > block_left and my_bottom <= block_top:
                above = True
            elif my_left < block_right and my_right > block_left and my_top >= block_bottom:
                below = True
            elif my_top < block_bottom and my_bottom > block_top and my_right <= block_left:
                west = True
            elif my_top < block_bottom and my_bottom > block_top and my_left >= block_right:
                east = True

            # COLLISION - will next movement cause intersection
            # Vertical
            if my_bottom + self.vel[1] >= block_top and above: # above the platform collision
                # current pos + Δx = # correct pos
                # Δx = correct pos - current pos
                clip = (block_top - my_height) - my_top # correct - current pos
                y_change = self.update_clipsize(y_change,clip) # always keep the lowest (absolute) value 
                y_vel = 0
                has_ground = True
                # check for complete contact
                if my_left > block_left and my_right < block_right and b != riding_platform: # full contact on surfaces other than the riding platform
                    full_contact_ground = True
                # - SPECIAL Surface Attributes -
                self.check_platform(b)
                if hasattr(b,'path'): # if this is a moving platform, move with the platform
                    riding_platform = b
                    if riding_platform.vel[0] != 0:
                        riding_platform.rider_x = True # moving along the x-axis
                    b.rider = self

            elif my_top + self.vel[1] <= block_bottom and below and not passable_block: # below the platform collision
                clip = (block_bottom) - my_top
                y_change = self.update_clipsize(y_change,clip)
                y_vel = 0
            
            if not passable_block: # all sides are impassable
            # Horizontal
                if my_right + x_vel >= block_left and west: # left collision
                    clip = (block_left - my_width) - my_left
                    x_change = self.update_clipsize(x_change,clip)
                    x_vel = 0
                    self.has_wall = -1 # player can perform a wall-jump now
                    self.check_platform(b)
                elif my_left + x_vel <= block_right and east: # right collision
                    clip = (block_right) - my_left
                    x_change = self.update_clipsize(x_change,clip)
                    x_vel = 0
                    self.has_wall = 1 # player can perform a wall-jump now
                    self.check_platform(b)

                # Diagonal Collision
                if x_vel != 0 and y_vel != 0:
                    # where the corner will end up next frame
                    my_topleft = (self.hitbox.x, self.hitbox.y)
                    my_topright = (self.hitbox.x + my_width, self.hitbox.y)
                    my_bottomleft = (self.hitbox.x, self.hitbox.y + my_height)
                    my_bottomright = (self.hitbox.x + my_width, self.hitbox.y + my_height)
                    for corner in [my_topleft,my_topright,my_bottomleft,my_bottomright]:
                        corner = list(corner)
                        corner[0] += self.vel[0]
                        corner[1] += self.vel[1]
                        corner = tuple(corner)

                        if corner[0] >= block_left and corner[0] <= block_right and corner[1] >= block_top and corner[1] <= block_bottom:
                            # decide which side to clip to (only continue motion towards that side)
                            if self.vel[0] >= self.vel[1]:
                                # clip to horizontal edge
                                y_vel = 0
                            else:
                                # clip to vertical edge
                                x_vel = 0

        # update player's position
        self.x += x_change
        self.hitbox.x += x_change
        self.y += y_change
        self.hitbox.y += y_change
        # Overide the player's velocity
        self.vel = [x_vel,y_vel]

        # check if the player is in a state of falling or jumping
        if has_ground:
            self.falling = False # falling stops when you hit the ground
            self.jumping = False # jumping stops when yout hit the ground
            self.wall_jumping = False
        else:
            if self.vel[1] < 0: # going up
                self.falling = False
            else:
                self.falling = True # going down or stationary [y]

        if self.has_wall == 0:
            self.wall_slide = False
        elif not self.slipping: # all slipping does is prevent this from occuring
            if self.falling: # can only slide on the way down
                self.wall_slide = True
            else:
                self.wall_slide = False

        # Moving Platform that is being riden
        if riding_platform != None:
            if full_contact_ground:
                riding_platform.rider_x = False # cannot move horizontally with the platform any longer


    def adjust_pos(self,block_list):
        intersect_change = [0,0]
        my_left = self.hitbox.x
        my_right = self.hitbox.x + self.hitbox.width
        my_top = self.hitbox.y
        my_bottom = self.hitbox.y + self.hitbox.height
        for block in block_list:
            block_top = block.y
            block_bottom = block.y + block.height
            block_left = block.x
            block_right = block.x + block.width
            passable_block = block.passable
            if not passable_block: # physical boundaries
                # Check if block moved into the player
                if my_top < block_bottom and my_bottom > block_top:
                    if my_left < block_right and my_right > block_left:
                        # determine which side of the block to clip the player to (side with smallest intersection)
                        intersect_left = abs(my_right - block_left)
                        intersect_right = abs(my_left - block_right)
                        intersect_top = abs(my_bottom - block_top)
                        intersect_bottom = abs(my_top - block_bottom)
                        intersections = [intersect_left,intersect_right]
                        smallest_intersect = min(intersections)

                        if smallest_intersect == intersect_left: # left intersection
                            intersect_change[0] = block_left - my_right # amount the 2 squares are overlapped
                        elif smallest_intersect == intersect_right: # right intersection
                            intersect_change[0] = block_right - my_left
                        elif smallest_intersect == intersect_top: # top
                            intersect_change[1] = block_top - my_bottom
                        elif smallest_intersect == intersect_bottom: # bottom
                            intersect_change[1] = block_bottom - my_top
        # adjust position
        self.x += intersect_change[0]
        self.hitbox.x += intersect_change[0]
        self.y += intersect_change[1]
        self.hitbox.y += intersect_change[1]

    def detect_collision(self,blocks): #*
        collision = False
        # define bounds of player's hitbox
        my_left = self.hitbox.x
        my_right = self.hitbox.x + self.hitbox.width
        my_top = self.hitbox.y
        my_bottom = self.hitbox.y + self.hitbox.height
        # Touching any of these obstacles will kill the player
        for b in blocks:
            block_height = b.hitbox.height
            block_width = b.hitbox.width
            block_top = b.hitbox.y
            block_bottom = b.hitbox.y + b.hitbox.height
            block_left = b.hitbox.x
            block_right = b.hitbox.x + b.hitbox.width

            # check for collision
            if my_left < block_right and my_right > block_left:
                if my_top < block_bottom and my_bottom > block_top:
                    #print(b.x,b.hitbox.x) # check if hitbox is aligned with container
                    #print(b.y,b.hitbox.y)
                    #print()
                    collision = True
                    if hasattr(b,'invincible'): # exceptions - reverse of the state inspected
                        collision = not b.invincible
                    if hasattr(b,'dying'):
                        collision = not b.dying
                    if hasattr(b,'passable'):
                        collision = not b.passable

        # what happens when collision occurs
        if collision == True:
            self.die() # dies

    def detect_orbs(self,orb_list):
        # define bounds of player
        my_left = self.hitbox.x
        my_right = self.hitbox.x + self.hitbox.width
        my_top = self.hitbox.y
        my_bottom = self.hitbox.y + self.hitbox.height
        # all orbs on-screen
        for orb in orb_list:
            orb_height = orb.height
            orb_width = orb.width
            orb_top = orb.y
            orb_bottom = orb.y + orb.height
            orb_left = orb.x
            orb_right = orb.x + orb.width
            # check if the player makes contact with an orb
            if my_left < orb_right and my_right > orb_left:
                if my_top < orb_bottom and my_bottom > orb_top:
                    # collect the orb
                    self.orbs_collected += 1
                    self.absorb_light()
                    orb.has_light = False

    def detect_screen(self):
        x_change = 0
        if self.hitbox.x + self.vel[0] < 0: # left side
            x_change = -self.hitbox.x
            self.vel[0] = 0
        elif self.hitbox.x + self.hitbox.width + self.vel[0] >= display_width: # right side
            x_change = (display_width - self.hitbox.width) - self.hitbox.x
            self.vel[0] = 0
        self.x += x_change
        self.hitbox.x += x_change

        if self.hitbox.y > display_height: # fell off-screen (down)
            # print('fell down')
            self.die()

    def absorb_light(self):
        self.light_filled += self.orb_light # fill the light bar
        if self.light_filled > 100:
            self.light_filled = 100

    def update_vision(self):
        # current field of view = percent light bar is filled * maximum field of view
        self.visible_radius = int(self.light_filled/100 * self.max_visibility)
        # prevent overshooting max/min bounds
        if self.visible_radius > self.max_visibility:
            self.visible_radius = self.max_visibility
        elif self.visible_radius < self.min_visibility:
            self.visible_radius = self.min_visibility

    def diminish_light(self): # slowly lose light over time
        if self.light_filled > 0:
            self.light_filled -= self.diminish_speed / fps
        if self.light_filled < 0:
            self.light_filled = 0

    def update_ammo(self): # *
        x = self.x + self.width/2
        y = self.y + self.height/2
        ammo_width = 23
        ammo_height = 9
        # remove depleted ammunition from the list
        for ammo in self.light_beams:
            if ammo.depleted: # used up (delete)
                self.light_beams.remove(ammo) # delete that projectile from existence

        # add new ammunition to the list
        new_charges = self.charges - len(self.light_beams) # amount of ammo that must be added
        for ammo in range(new_charges):
            new_projectile = Projectile((x,y),self,ammo_width,ammo_height,img=lightbeam_sprite,glow=True) # default light beam
            self.light_beams.append(new_projectile)

    def reload(self):
        if self.reload_counter > 0: 
            self.reload_counter -= 1 # decrease the time it takes to shoot another beam
            if self.reload_counter <= 0: # just finished reloading
                self.hold_shot = True
        else:
            self.hold_shot = False

    def check_death(self):
        if self.hp <= 0:
            self.die()

    def die(self):
        if self.alive:
            print('You Died.')
        self.alive = False # indicates player is dead
        self.animation_index = 0 # start from the beginning of the death animation cycle


class Projectile(Entity):
    def __init__(self,pos,user,w=0,h=0,img=None,glow=False):
        super(Projectile,self).__init__(pos,w,h,img)
        self.vel = [0,0]
        self.speed = 16 # default
        self.dir = [1,0] # default - (left to right)
        self.damage = 1
        self.launched = False # is it released yet (if not then it's hidden)
        self.depleted = False # indicated the projectile is ready to be deleted (hits an object, enemy or goes off-screen)
        self.user = user
        self.glow = glow # emits light
        self.glow_radius = 50 #!
        self.color = white # DP!
    def update_position(self): # the projectile is stationary and follows its user until launched
        if not self.launched:
            # the resting position of the projectile is the center of the user
            x = self.user.x + self.user.width/2
            y = self.user.y + self.user.height/2
            # proper_position = current_position + change
            x_change = x - self.x 
            y_change = y - self.y
            # update position of projectiles
            self.x += x_change
            self.hitbox.x += x_change
            self.y += y_change
            self.hitbox.y += y_change
            # update orientation
            if self.user.face_right:
                self.dir[0] = 1
            elif not self.user.face_right:
                self.dir[0] = -1
            else:
                print('ERROR!-PROJECTILE DIRECTION')
    def update_vel(self):
        self.vel[0] = self.speed * self.dir[0]
        self.vel[1] = self.speed * self.dir[1]
    def move(self):
        if self.launched:
            self.x += self.vel[0]
            self.hitbox.x += self.vel[0]
            self.y += self.vel[1]
            self.hitbox.y += self.vel[1]

    def detect_targets(self,target_list):
        target = None # the thing being hit (if there is something)
        if self.launched:
            collision = False
            # define bounds of projectile's hitbox
            projectile_left = self.hitbox.x
            projectile_right = self.hitbox.x + self.hitbox.width
            projectile_top = self.hitbox.y
            projectile_bottom = self.hitbox.y + self.hitbox.height
            # Touching any of these obstacles will kill the player
            for t in target_list:
                target_height = t.height
                target_width = t.width
                target_top = t.y
                target_bottom = t.y + t.height
                target_left = t.x
                target_right = t.x + t.width

                # check for collision
                if projectile_left < target_right and projectile_right > target_left:
                    if projectile_top < target_bottom and projectile_bottom > target_top:
                        collision = True
                        target = t

            # what happens when the projetile hits a target
            if target:
                pass_through = False
                if hasattr(target,'passable'):
                    pass_through = target.passable # does the projectile go through the object
                if collision == True and not pass_through:
                    self.depleted = True
                    hit = True # if target will take damage
                    if hasattr(target,'invincible'):
                        hit = not target.invincible
                    if hasattr(target,'hp') and hit: # if the target has hp
                        target.hp -= self.damage # target loses a hitpoint

    def detect_boundaries(self):
        if self.launched:
            if self.hitbox.x < 0 or self.hitbox.x + self.hitbox.width > display_width: # X
                self.depleted = True
            elif self.hitbox.y < 0 or self.hitbox.y + self.hitbox.height > display_height: # Y
                self.depleted = True

    def draw(self):
        if self.launched: # must be launched to be visible
            if not self.image:
                pygame.draw.rect(gameDisplay,self.color,(self.x,self.y,self.width,self.height))
            else:
                gameDisplay.blit(self.image,(self.x,self.y))

class Light_Orb(Entity):
    def __init__(self,pos,w=44,h=44):
        img = orb_sprites[0]
        super(Light_Orb,self).__init__(pos,w,h,img)
        self.color = white
        self.has_light = True # can be eaten by darkness
        self.glow_radius = 80 #!
        self.animation_frames = 1.0*fps/5
        self.animation_index = 0
        self.animation_counter = 0
        self.glow_pause = 0 # times the glowing sprite has been displayed once this cycle
    def choose_image(self): # 5 animation frames, but 3 images (pauses on index 1 for an extra count)  - 0 1 1 2 / 0(3) 1 1 2
        self.animation_counter += 1
        if self.animation_counter >= self.animation_frames:
            self.animation_counter = 0
            if self.animation_index != 1 or self.glow_pause == 2: # 2 extra glow frames (first glow is free) +
                self.animation_index += 1
            elif self.animation_index == 1:
                self.glow_pause += 1
            if self.animation_index == 3: # completed full cycle
                self.animation_index = 0
                self.glow_pause = 0
        self.image = orb_sprites[self.animation_index] # update image

class Platform(Entity):
    def __init__(self,pos,w=50,h=50,passable=False,spawnable=True,dark=False,slippery=False):
        # set initial block (for building the platform)
        if pos[1] >= 500:
            img = brown_block # dirt
        elif passable:
            img = passable_platform
        elif slippery:
            img = slippery_platform
        else: # (default)
            img = main_platform_block # static
        super(Platform,self).__init__(pos,w,h,img)
        self.passable = passable # can player jump through its bottom (only top of this platform is detected)
        self.slippery = slippery # cannot wall jump on it
        self.spawnable = spawnable # can enemies be placed on top of this platform
        self.dark = dark # dark platforms drain light when touched
        if self.dark:
            self.drain = 15 #! percent/second (6~7s)
    def choose_image(self):
        # do this once, since the image will not change
        if self.passable:
            self.image = passable_platform
        elif self.width != 50 or self.height != 50: # irregular shape - BUILD PLATFORM (custom size)
            source_image = self.image.copy() # block used to build platform
            # all paltform tiles (except ground) are 50x50
            # new platform is anchored topleft - builds right and down ##
            x_blocks = math.ceil(self.width/50)
            y_blocks = math.ceil(self.height/50)
            new_surface = pygame.Surface((self.width,self.height))
            for y in range(y_blocks):
                for x in range(x_blocks): # partial block is considered another block
                    if x + 1 == x_blocks: # last column
                        block_width = 50 - (self.width % 50) # excess
                    else:
                        block_width = 50
                    if y + 1 == y_blocks: # last row
                        block_height = 50 - (self.height % 50) # excess
                    else:
                        block_height = 50
                    new_surface.blit(source_image,(x*50,y*50),area=(0,0,block_width,block_height))
            del source_image # s.m
            self.image = new_surface
        else:
            pass # keep static image

class Falling_Platform(Entity):
    def __init__(self,pos,w=50,h=50,img=None,spawnable=True):
        self.image = falling_platform_block
        super(Falling_Platform,self).__init__(pos,w,h,self.image)
        self.passable = False # full contact
        self.slippery = True #!!
        self.spawnable = spawnable
        self.triggered = False # starts to fall once triggered
        self.fall_speed = 0
        fall_screen = 2.0
        n = fall_screen * fps
        self.acc = math.sqrt(display_height / (n*(n-1)))
        #self.acc = gravity # acceleration in the y-axis
        self.color = blue

        self.falling = False
        self.activation_time = 0.50 # time before platform falls, after being triggered
        self.activation_counter = 0
        self.terminate = False # platform is no longer on screen, delete it

    def fall(self):
        if self.falling: # activated
            self.fall_speed += self.acc # increase speed
            self.y += self.fall_speed
            self.hitbox.y += self.fall_speed
            self.check_bounds() # check off-screen

        elif self.triggered: # going to fall soon
            self.activation_counter += 1
            if self.activation_counter >= self.activation_time * fps:
                self.falling = True # ready to fall

    def check_bounds(self):
        # if the platform fell off-screen, it is no longer useful - delete it
        if self.y > display_height:
            self.terminate = True

class Moving_Platform(Entity):
    def __init__(self,path,closed=False,w=50,h=50,img=None,spawnable=True):
        self.image = moving_platform_block
        self.path = path # list of points the platform moves to (in order)
        self.path_index = 1 # what part of the path its currently going to
        pos = self.path[0] # starts at first point (default)
        super(Moving_Platform,self).__init__(pos,w,h,self.image)

        self.passable = False # full contact
        self.spawnable = spawnable
        self.speed = 3 # default
        self.dir = 1 # forwards order
        self.vel = [0,0]
        self.closed_path = closed # make True if the path is a closed shape (square, circle, line, ect.) that can be looped
        self.rider = None # entities on this platform
        self.rider_x = True # can the entity move with the platform in the x-direction (friction)
        self.color = green

    def update_vel(self): #**
        destination = self.path[self.path_index]
        # check if the platformed REACHED its next destination:
        if abs(self.x - destination[0]) < self.speed:
            if abs(self.y - destination[1]) < self.speed:
                # cannot get closer to destination (endpoint)
                if self.closed_path and self.path_index == len(self.path)-1: # CLOSED PATH - completed a cycle
                    self.path_index = -1
                elif not self.closed_path: # OPEN PATH - check if platformed reached an end:
                    if self.path_index == len(self.path)-1: # reached final destination (now go back)
                        self.dir = -1
                        #print('hit left') #DP!
                    elif self.path_index == 0: # reached initial position (go forwards)
                        self.dir = 1
                        #print('hit right') #DP!
                # start to move to the next destination
                self.path_index += self.dir

        # Now head towards the next destination:
        destination = self.path[self.path_index] # update destination
        x_change = 0 
        y_change = 0
        if abs(self.x - destination[0]) >= self.speed: # can get closer to destination, distance from destination is not smaller than speed
            if self.x < destination[0]: # going right
                x_direction = 1
            elif self.x > destination[0]: # going left
                x_direction = -1
            else:
                print('ERROR-MOVING PLATFORMS X-DIR')
            x_change = self.speed * x_direction
        if abs(self.y - destination[1]) >= self.speed:
            if self.y > destination[1]:
                y_direction = -1
            elif self.y < destination[1]:
                y_direction = 1
            else:
                print('ERROR-MOVING PLATFORMS Y-DIR')
            y_change = self.speed * y_direction
        self.vel = [x_change,y_change] # update velocity

    def move(self):
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]
        if self.rider != None:
            if self.rider_x:
                self.rider.x += self.vel[0]
                self.rider.hitbox.x += self.vel[0]
            self.rider.y += self.vel[1]
            self.rider.hitbox.y += self.vel[1]


class Spikes(Entity):
    def __init__(self,pos,w=50,h=50):
        img = spike_sprite
        super(Spikes,self).__init__(pos,w,h,img)
        self.color = magenta

class Moving_Spikes(Entity):
    def __init__(self,path,w=50,h=50,closed=False):
        img = spike_sprite
        self.path = path # list of points the spike moves to (in order)
        self.path_index = 1 # what part of the path its currently going to
        pos = self.path[0] # starts at first point (default)
        super(Moving_Spikes,self).__init__(pos,w,h,img)

        self.speed = 4 # default
        self.dir = 1 # forwards order
        self.vel = [0,0]
        self.closed_path = closed # make True if the path is a closed shape (square, circle, line, ect.)

    def update_vel(self):
        destination = self.path[self.path_index]
        # check if the platformed REACHED its next destination:
        if abs(self.x - destination[0]) < self.speed:
            if abs(self.y - destination[1]) < self.speed:
                # cannot get closer to destination (endpoint)
                if self.closed_path and self.path_index == len(self.path)-1: # CLOSED PATH - completed a cycle
                    self.path_index = -1
                elif not self.closed_path: # OPEN PATH - check if platformed reached an end:
                    if self.path_index == len(self.path)-1: # reached final destination (now go back)
                        self.dir = -1
                        #print('hit left') #DP!
                    elif self.path_index == 0: # reached initial position (go forwards)
                        self.dir = 1
                        #print('hit right') #DP!
                # start to move to the next destination
                self.path_index += self.dir

        # Now head towards the next destination:
        destination = self.path[self.path_index] # update destination
        x_change = 0 
        y_change = 0
        if abs(self.x - destination[0]) >= self.speed: # can get closer to destination, distance from destination is not smaller than speed
            if self.x < destination[0]: # going right
                x_direction = 1
            elif self.x > destination[0]: # going left
                x_direction = -1
            else:
                print('ERROR-MOVING PLATFORMS X-DIR')
            x_change = self.speed * x_direction
        if abs(self.y - destination[1]) >= self.speed:
            if self.y > destination[1]:
                y_direction = -1
            elif self.y < destination[1]:
                y_direction = 1
            else:
                print('ERROR-MOVING PLATFORMS Y-DIR')
            y_change = self.speed * y_direction
        self.vel = [x_change,y_change] # update velocity

    def move(self):
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]


class Static_Enemy(Entity): # does not move, (a hazard that can be killed)
    def __init__(self,pos,w=0,h=0,img=None):
        super(Static_Enemy,self).__init__(pos,w,h,img)
        self.name = 'static' # to differentiate between enemies
        self.color = dark_red # DP!

class Tormentor(Entity):
    def __init__(self,pos=(0,0),img=tormentor_sprites[0]):
        w = 140
        h = 61 # static
        super(Tormentor,self).__init__(pos,w,h,img)
        # update hitbox
        self.hitbox.width = 94
        self.hitbox.height = 45
        self.offset = self.width - self.hitbox.width

        self.name = 'tormentor'
        self.alive = True
        self.anchored = False # doesn't scroll with screen
        self.hp = 2 #!
        self.float_speed = 8 #! speed in (x,y) axis
        self.float_counter = 0

        self.dir = -1 # to the LEFT
        self.vel = [0,0]
        self.face_left = True

        self.amplitude = 6 # distance moved up/down from origin
        self.modulation_speed = 0.5 # speed of [y] modulation
        self.modulation_counter = 0 # tracks progress of modulation
        self.modulation_dir = -1 # starts by going down

        self.animation_counter = 0
        self.animation_index = 0
        self.animation_frames = 1.5*fps // 5

    def spawn(self,spawn_left_chance=35):
        # WHEN SPAWNING AN ENEMY, the enemy must be AT LEAST 1 PIXEL on the HORIZONTAL and VERTICAL SCREEN, or else it will be deleted immediately
        # choose a position for the ghost
        spawn_left = random.randint(1,100) #! 35% chance to spawn left
        if spawn_left <= spawn_left_chance:
            x = 1 # starts from the very LEFT (on-screen)
            self.face_left = False # face right instead
            self.dir = 1
        else:
            x = display_width - 1# starts from the very RIGHT (on-screen)
            self.face_left = True # face left
            self.dir = -1
        y = random.randint(50,int(display_height-self.height-100)) # on-screen, top and bottom
        self.x = x
        self.hitbox.x = x
        if not self.face_left: # hitbox adjustment
            self.hitbox.x += self.offset
        self.y = y
        self.hitbox.y = y

    def update_vel(self):         
        # Missile Movement - fast horizontally, at one height
        x = self.float_speed * self.dir
        # Float up and down
        y = self.modulation_speed * self.modulation_dir
        self.modulation_counter += y
        #print(self.modulation_counter) # DP!
        # check modulation
        if self.amplitude - abs(self.modulation_counter) < self.modulation_speed: # half-cycle complete
            self.modulation_dir *= -1 # flip the direction
        self.vel = [x,y] # update vel

    def move(self):
        # x-direction
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        if self.hitbox.x + self.hitbox.width < 0 or self.hitbox.x > display_width: # ghost made it off-screen
            self.alive = False
        elif self.hitbox.y + self.hitbox.height < 0 or self.hitbox.y > display_height:
            self.alive = False
        # y-direction
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]

    def check_life(self):
        if self.hp <= 0:
            self.alive = False

    def choose_image(self):
        animation_set = []
        # choose an animation set
        if self.face_left:
            animation_set = tormentor_sprites
        elif not self.face_left:
            animation_set = tormentor_sprites_rev
        else:
            print('ERROR-TORMENTOR-FACEDIR')
        self.image = animation_set[self.animation_index] # choose animation sprite

        self.animation_counter += 1
        if self.animation_counter >= self.animation_frames:
            self.animation_index += 1
            self.animation_counter = 0 # reset counter
            if self.animation_index == 5:
                self.animation_index = 0 # reset animation

class Purple_Ghost(Entity):
    def __init__(self, pos = (0,0), img = None):
        w = 78
        h = 42
        super(Purple_Ghost,self).__init__(pos,w,h,img)
        self.name = 'purple ghost'
        self.alive = True
        self.transformed = False
        self.hp = 3 # hits before death

        self.old_hp = self.hp
        self.anchored = False # doesn't scroll with screen
        self.invincible = False
        self.invincibility_time = 0.75 # time before it can take damage again
        self.invincibility_counter = 0

        self.despawn = False # despawns after a while
        self.despawn_time = 6.0 # seconds
        self.despawn_counter = 0
        self.despawn_dir = [0,0] # which way the ghost will leave the screen

        self.dir = [-1,0] # to the LEFT, 0= no motion
        self.vel = [0,0]
        self.face_left = True

        self.float_speed = (4,2) # speed in (x,y) axis
        self.float_counter = 0

        self.amplitude = self.height # distance moved up/down from origin
        self.modulation_speed = 2 # speed of [y] modulation
        self.modulation_counter = 0 # tracks progress of modulation
        self.modulation_dir = 1 # starts by going down (-1 is up)

        self.animation_counter = 0
        self.animation_index = 0
        self.animation_frames = 1*fps // 4
        self.animation_dir = 1 # forwards
        self.animation_delay = 2 # seconds spent on outter animation frames
        self.animation_delay_timer = self.animation_delay*fps # countdown in frames (delay ends when this reaches 0)

    def spawn(self):
        # WHEN SPAWNING AN ENEMY, the enemy must be AT LEAST 1 PIXEL on the HORIZONTAL and VERTICAL SCREEN, or else it will be deleted immediately
        # choose a position for the ghost
        x = display_width - 1 # always starts from the right
        y = random.randint(0,int(display_height-self.height)) # on-screen, top and bottom
        self.x = x
        self.hitbox.x = x
        self.y = y
        self.hitbox.y = y

    def update_vel(self,player_center): #***
        x = 0; y = 0 # will be the velocity in each axis
        my_center = (self.x+self.width//2, self.y+self.height//2) # center of the enemy
        escaping = False # leaving the screen

        # Float up and down
        if not self.transformed:
            y = self.modulation_speed * self.modulation_dir
            self.modulation_counter += y
            # check modulation
            if abs(self.amplitude - abs(self.modulation_counter)) < self.modulation_speed: # half-cycle complete
                self.modulation_dir *= -1 # flip the direction
                
        # Transformed
        if self.transformed:
            awareness = random.randint(0,fps//2) # will the ghost move towards player (0 is target)
            # determine speed - acc. towards player
            new_speed = 12 - (0.5 * abs(my_center[0]-player_center[0]) // 50)
            if new_speed < 3:
                new_speed = 3
            self.float_speed[0] = new_speed
        else:
            awareness = 0
            
        # Check Despawn
        if self.despawn and not self.transformed:
            if self.despawn_counter >= self.despawn_time * fps: # time is up - leave screen
                escaping = True
                # choose a route off the screen
                if self.despawn_dir == [0,0]:
                    escape_x = self.dir[0]
                    escape_y = self.dir[1]
                    if escape_x == 0:
                        escape_x = random.randrange(-1,2,2)
                    self.despawn_dir = [escape_x,escape_y]
                # make your way off-screen
                x = self.despawn_dir[0] * self.float_speed[0]
                y = self.despawn_dir[1] * self.float_speed[1]
            else:
                self.despawn_counter += 1

        # Following Movement - always towards the player
        # Rage Movement (when transformed) - faster, more in [x]        
        if not escaping and awareness == 0:
            # Height Change
            y_change = player_center[1] - my_center[1] # object related to me
            if y_change < 0 and abs(y_change) >= 2*self.float_speed[1]: # player above
                self.dir[1] = -1
            elif y_change > 0 and abs(y_change) >= 2*self.float_speed[1]: # player below
                self.dir[1] = 1
            else:
                self.dir[1] = 0 # same height
            # update [y]
            y += self.float_speed[1] * self.dir[1]

            # Horizontal Change
            x_change = player_center[0] - my_center[0] # object related to me
            if x_change < 0 and abs(x_change) >= 2*self.float_speed[0]: # player left
                self.dir[0] = -1
            elif x_change > 0 and abs(x_change) >= 2*self.float_speed[0]: # player right
                self.dir[0] = 1
            else:
                self.dir[1] = 0 # same height
            # Set [x]
            x = self.float_speed[0] * self.dir[0]
            if x == 0: #DP!!!
                x = random.randint(-5,5) # cannot be compeltely still
        self.vel = [x,y] # update vel
        self.update_dir() # update direction based on velocity

    def update_dir(self):
        if self.vel[0] < 0:
            self.face_left = True
        elif self.vel[0] > 0:
            self.face_left = False
        else:
            pass # keep previous direction

    def move(self):
        # x-direction
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        if self.hitbox.x + self.hitbox.width < 0 or self.hitbox.x > display_width: # ghost made it off-screen
            self.alive = False
        elif self.hitbox.y + self.hitbox.height < 0 or self.hitbox.y > display_height:
            self.alive = False
        # y-direction
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]

    def cool_down(self):
        # invulnerability wears off after some time
        if self.invincible:
            self.invincibility_counter -= 1
            if self.invincibility_counter <= 0:
                self.invincible = False

    def check_life(self):
        # check for damage
        if self.old_hp != self.hp and self.hp >= 1: # must have been hit
            self.invincible = True
            self.invincibility_counter = 0.75*fps # time before it can take damage
        if self.hp == 1 and not self.invincible: # only becomes transformed after invincibility ends
            self.transformed = True
            # change attributes
            self.float_speed = [6,1]  #!
            self.animation_frames = self.invincibility_time*fps // 2
        elif self.hp <= 0:
            self.alive = False
        self.old_hp = self.hp # update previous health

    def choose_image(self):
        # choose an animation set
        if self.face_left:
            animation_set = purple_ghost_sprites
        else:
            animation_set = purple_ghost_sprites_rev

        # Ordinary Animation Cycle
        if not self.invincible: 
            # countdown until next animation
            if self.animation_delay_timer > 0:
                self.animation_delay_timer -= 1
                self.animation_counter += 1 # to skip first frame wait time (already delayed on it)
            else: # delay finished - CONTINUE ANIMATION
                self.animation_counter += 1
                if self.animation_counter >= self.animation_frames: # move to next sprite
                    self.animation_counter = 0 # reset counter
                    self.animation_index += self.animation_dir # 1 or -1
                    # Cycle Completion
                    if self.animation_index == 3: # end of animation (start delay timer again)
                        self.animation_delay_timer = self.animation_delay * fps
                        self.animation_dir = -1 # backwards
                    elif self.animation_index == 0: # start of cycle (start delay)
                        self.animation_delay_timer = self.animation_delay * fps
                        self.animation_dir = 1 # forwards

        # Invincibility Animation (took damage)
        else:
            # Taking damage resets the ordinary animation cycle
            self.animation_dir = 1
            self.animation_counter = 0
            self.animation_delay_timer = self.animation_delay * fps
            self.animation_index = 4 # damaged sprite (static)
            if self.invincibility_counter == 1: # last frame of invincibility, regular animation cycle continues
                self.animation_index = 0
        # choose current image
        self.image = animation_set[self.animation_index]

    def choose_image_transformed(self):
        # when ghost is transformed ONLY
        if self.transformed: # make sure of it
            # choose animation set
            if self.face_left:
                animation_set = transformed_ghost_sprites
            else:
                animation_set = transformed_ghost_sprites_rev
            self.animation_counter += 1
            if self.animation_counter >= self.animation_frames:
                self.animation_counter = 0 # reset counter
                self.animation_index = abs(self.animation_index - 1) # produces the opposite of whats given (either 0 or 1)
                print(self.animation_index) ######
        else:
            print('ERROR-TRANSFORMED-1')
        # choose image
        self.image = animation_set[self.animation_index]

class Pink_Ghost(Entity):
    def __init__(self, pos = (0,0), img = None):
        w = 78
        h = 42
        super(Pink_Ghost,self).__init__(pos,w,h,img)
        self.name = 'pink ghost'
        self.alive = True
        self.dying = False
        self.hp = 2 # hits before death

        self.old_hp = self.hp
        self.anchored = False # doesn't scroll with screen
        self.invincible = False
        self.invincibility_time = 0.75
        self.invincibility_counter = 0

        self.despawn = True # despawns after a while
        self.despawn_time = 8.0 # seconds
        self.despawn_counter = 0
        self.despawn_dir = [0,0] # which way the ghost will leave the screen

        self.dir = [-1,0] # to the LEFT, 0= no motion
        self.vel = [0,0]
        self.face_left = True

        self.float_speed = (4,4) # speed in (x,y) axis
        self.float_counter = 0

        self.animation_counter = 0
        self.animation_index = 0
        self.animation_frames = 1*fps // 2 # normal cycle
        self.death_animation_frames = self.invincibility_time*fps // 6 # for full death animation !(round)
        self.animation_dir = 1 # forwards

    def spawn(self):
        # WHEN SPAWNING AN ENEMY, the enemy must be AT LEAST 1 PIXEL on the HORIZONTAL and VERTICAL SCREEN, or else it will be deleted immediately
        # choose a position for the ghost
        spawn_left = random.randint(1,2) #! 50% chance to spawn left
        if spawn_left == 1:
            x = 1 # starts from the very LEFT (on-screen)
            self.face_left = False # face right instead
        else:
            x = display_width - 1# starts from the very RIGHT (on-screen)
        y = random.randint(0,int(display_height-self.height)) # on-screen, top and bottom
        self.x = x
        self.hitbox.x = x
        self.y = y
        self.hitbox.y = y

    def update_vel(self,player_center):
        x = 0; y = 0 # will be the velocity in each axis
        my_center = (self.x+self.width//2, self.y+self.height//2) # center of the enemy
        escaping = False # leaving the screen
        attack_chance = random.randint(0,int(2*fps)) # every 2 seconds
       
        # Check Despawn
        if self.despawn:
            if self.despawn_counter >= self.despawn_time * fps: # time is up - leave screen
                escaping = True
                # choose a route off the screen
                if self.despawn_dir == [0,0]:
                    escape_x = self.dir[0]
                    escape_y = self.dir[1]
                    if escape_x == 0:
                        escape_x = random.randrange(-1,2,2)
                    self.despawn_dir = [escape_x,escape_y]
                # make your way off-screen
                x = self.despawn_dir[0] * self.float_speed[0]
                y = self.despawn_dir[1] * self.float_speed[1]
            else:
                self.despawn_counter += 1

        # Attack Movement - go towards player
        if not escaping and attack_chance == 0:
            # Height Change
            if self.level >= 1:
                y_change = player_center[1] - my_center[1] # object related to me
                if y_change <= 0: # player above
                    self.dir[1] = -1
                elif y_change > 0: # player below
                    self.dir[1] = 1
                else:
                    self.dir[1] = 0 # same height
                # update [y]
                y += self.float_speed[1] * self.dir[1]

            # Horizontal Change
            if self.level >= 2:
                x_change = player_center[0] - my_center[0] # object related to me
                if x_change <= 0: # player left
                    self.dir[0] = -1
                elif x_change > 0: # player right
                    self.dir[1] = 1
                # Set [x]
                x = self.float_speed[0] * self.dir[0]

        # Wander Movement - random motion (default)
        else:
            change_dir_x = random.randint(1,int(5*fps)) #! every 5 seconds
            if change_dir_x == 1:
                self.dir[0] *= -1 # changes direction
            change_dir_y = random.randint(1,int(5*fps)) #! every 5 seconds
            if change_dir_y == 1:
                self.dir[1] *= -1 # flip direction
            # update [x] and [y]
            x = random.randint(1,self.float_speed[0]) * self.dir[0]
            y = random.randint(0,self.float_speed[1]) * self.dir[1]

        self.vel = [x,y] # update vel
        self.update_dir() # update direction based on velocity 

    def update_dir(self):
        if self.vel[0] < 0:
            self.face_left = True
        elif self.vel[0] > 0:
            self.face_left = False
        else:
            pass # keep previous direction

    def move(self):
        # x-direction
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        if self.hitbox.x + self.hitbox.width < 0 or self.hitbox.x > display_width: # ghost made it off-screen
            self.alive = False
        elif self.hitbox.y + self.hitbox.height < 0 or self.hitbox.y > display_height:
            self.alive = False
        # y-direction
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]

    def cool_down(self):
        # invulnerability wears off after some time
        if self.invincible:
            self.invincibility_counter -= 1
            if self.invincibility_counter <= 0:
                self.invincible = False
                self.animation_dir = 1

    def check_life(self):
        # check for damage
        if self.old_hp != self.hp and self.hp >= 1: # must have been hit
            self.invincible = True
            self.invincibility_counter = self.invincibility_time*fps # time before it can take damage
            self.animation_index = 0 # reset the animation (before damage sprites progress)
            self.animation_dir = 1
        elif self.hp <= 0:
            self.dying = True
        self.old_hp = self.hp # update previous health (1 frame behind)

    def choose_image(self):
        # choose an animation set
        if self.face_left:
            animation_set = pink_ghost_sprites
        else:
            animation_set = pink_ghost_sprites_rev

        # increase counter
        self.animation_counter += 1
        # Ordinary Animation Cycle
        if not self.invincible and not self.dying: 
            if self.animation_counter >= self.animation_frames: # move to next sprite
                self.animation_counter = 0 # reset counter
                self.animation_index += animation_dir # 1 or -1
                # Cycle Completion - 2 sprites in animation
                if self.animation_index == 1: # 2 end
                    self.animation_dir = -1 # backwards
                elif self.animation_index == 0: # start
                    self.animation_dir = 1 # forwards
        # Damage Animation Cycle
        elif self.invincible and not self.dying:
            if self.animation_counter >= self.death_animation_frames: # move to next sprite
                self.animation_counter = 0 # reset counter
                self.animation_index += animation_dir # 1 or -1
                # Cycle completion - ends at index [3]
                if self.animation_index == 3:
                    self.animation_dir = -1
                elif self.animation_index == 0: # rest here
                    self.animation_dir = 0

        # Death Animation - (full)
        elif self.dying:
            if self.animation_counter >= self.death_animation_frames: # move to next sprite
                self.animation_counter = 0 # reset counter
                self.animation_index += animation_dir # 1 or -1
                # Animation completion - at index [5]
                if self.animation_index == 5:
                    self.animation_dir = 0 # cannot go any further
                elif self.animation_index == 6: # last death animation just finished
                    self.alive = False # now it can die
        else:
            print('ERROR-PINK-ANIMATION')
        # choose current image
        self.image = animation_set[self.animation_index]


class Abyss(Entity):
    def __init__(self,pos=(0,0),img=None):
        w = 50
        h = 59
        super(Abyss,self).__init__(pos,w,h,img)
        self.name = 'abyss'
        self.alive = True
        self.hp = 1
        self.anchored = True
        self.riding = None # riding a paltform?
        self.animation_frames = 1.0 * fps
        self.animation_counter = 0
        self.animation_index = 0
        self.animation_dir = 1

    def spawn(self,open_platforms):
        # Where will Abyss start - he is atached to a platform
        chosen_platform = random.choice(open_platforms) # these platforms must be free on top
        chosen_platform.spawnable = False # cannot be used to spawn another enemy
        if chosen_platform.width == 50:
            x = chosen_platform.x
        elif chosen_platform.width > 50:
            x = random.randint(int(chosen_platform.x),int(chosen_platform.x+chosen_platform.width-self.width))
        else:
            print('ERROR-SPAWN-PLATFORM-SIZE')
        y = chosen_platform.y - self.height # (static) always on top of platform
        # Update Position
        self.x = x
        self.hitbox.x = x
        self.y = y
        self.hitbox.y = y
        # Moving Platform
        if hasattr(chosen_platform,'path'): # move with this paltform
            self.riding = chosen_platform
        return chosen_platform # send back the platform used

    def move(self):
        if self.riding != None: # is on a moving surface
            self.x = self.x + self.riding.vel[0]
            self.hitbox.x = self.hitbox.x + self.riding.vel[0]
            self.y = self.y + self.riding.vel[1]
            self.hitbox.y = self.hitbox.y + self.riding.vel[1]

    def check_life(self):
        if self.hp <= 0:
            self.alive = False

    def choose_image(self):
        self.image = abyss_sprites[self.animation_index] # select new image
        self.animation_counter += 1
        if self.animation_counter >= self.animation_frames:
            self.animation_counter = 0 # reset counter
            self.animation_index += self.animation_dir # advance to next sprite
            if self.animation_index == 4: # reached end, go back after this
                self.animation_dir = -1
            elif self.animation_index == 0:
                self.animation_dir = 1

class Shadow_Ball(Entity):
    def __init__(self,pos=(0,0)):
        w = 12
        h = 12 # static
        img = shadow_orb_small
        super(Shadow_Ball,self).__init__(pos,w,h,img)
        self.vel = [0,0]
        self.speed = [5,2] # default
        self.dir = [-1,0] # default - (right to left)
        self.damage = 1
        self.depleted = False # indicated the projectile is ready to be deleted (hits an object, player or goes off-screen)
        self.color = black # DP!

        self.amplitude = self.height # distance moved up/down from origin
        self.modulation_speed = 0.20 # speed of [y] modulation
        self.modulation_counter = 0 # tracks progress of modulation
        self.modulation_dir = 1 # starts by going down (-1 is up)

    def spawn(self,player_center):
        # WHEN SPAWNING AN ENEMY, the enemy must be AT LEAST 1 PIXEL ON-SCREEN (X & Y), or else it will be deleted immediately
        # choose a position for the shadow ball to start from
        x = display_width - 1 # always starts from the right
        y = random.randint(int(-self.height)+1,display_height-1) # just on-screen, top and bottom
        self.x = x
        self.hitbox.x = x
        self.y = y
        self.hitbox.y = y

        # determine flight path now
        my_center = (self.x + self.width//2, self.y + self.height//2) # shadow center
        if abs(player_center[1] - my_center[1]) <= 10: # tolerance of 20 pixel radius
            y_dir = 0 # straight
        elif player_center[1] > my_center[1]:
            y_dir = 1 # down
        elif player_center[1] < my_center[1]:
            y_dir = -1 # up

    def update_vel(self):
        # Float up and down
        y = self.modulation_speed * self.modulation_dir
        self.modulation_counter += y
        # check modulation
        if  self.amplitude - abs(self.modulation_counter) < self.modulation_speed: # half-cycle complete
            self.modulation_dir *= -1 # flip the direction    
        self.vel[0] = self.speed[0] * self.dir[0]
        self.vel[1] = self.speed[1] * self.dir[1] + y

    def move(self):
        self.x += self.vel[0]
        self.hitbox.x += self.vel[0]
        self.y += self.vel[1]
        self.hitbox.y += self.vel[1]

    def detect_targets(self,target_list):
        collision = False
        # define bounds of projectile's hitbox
        projectile_left = self.hitbox.x
        projectile_right = self.hitbox.x + self.hitbox.width
        projectile_top = self.hitbox.y
        projectile_bottom = self.hitbox.y + self.hitbox.height
        # Touching any of these obstacles will kill the player
        for t in target_list:
            target_height = t.height
            target_width = t.width
            target_top = t.y
            target_bottom = t.y + t.height
            target_left = t.x
            target_right = t.x + t.width

            # check for collision
            if projectile_left < target_right and projectile_right > target_left:
                if projectile_top < target_bottom and projectile_bottom > target_top:
                    collision = True
                    target = t

        # what happens when the projetile hits a target
        if collision == True:
            self.depleted = True
            hit = True # if target will take damage
            if hasattr(target,'invincible'):
                hit = not target.invincible
            if hasattr(target,'hp') and hit: #! if the target has hp
                target.hp -= self.damage # target loses a hitpoint
            if hasattr(target,'has_light'):
                target.has_light = False

    def detect_boundaries(self):
        if self.hitbox.x < 0: # X - left only
            self.depleted = True
        elif self.hitbox.y < 0 or self.hitbox.y + self.hitbox.height > display_height: # Y
            self.depleted = True


class Darkness_Overlay():
    def __init__(self):
        self.width = display_width
        self.height = display_height
        self.center = (self.width//2, self.height//2)
        self.color = black
        self.layer = pygame.Surface((self.width,self.height))
        self.layer.convert_alpha(self.layer)
        self.colorkey = white
        self.layer.set_colorkey(self.colorkey) # white pixels will not be blitted!
        self.layer.set_alpha(240) # static

    def update_layer(self,fields):
        # basic black screen
        self.layer.fill(self.color)
        # regions of the screen where light is emitted - size and bounds
        for radius, rect in fields:
            if radius > 0:
                # rect is the bounds of a target - x,y,width,height
                x = int(rect[0] + rect[2]/2)
                y = int(rect[1] + rect[3]/2)
                pos = (x,y)
                # Add a white circle (cut-out) where the target is located
                pygame.draw.circle(self.layer,self.colorkey,pos,radius)
                fields.remove((radius,rect)) # remove from the list, its glow field has been set

        # the remaining fields are NEGATIVE - they override light, make darkness
        for radius, rect in fields:
                # rect is the bounds of a target - x,y,width,height
                x = int(rect[0] + rect[2]/2)
                y = int(rect[1] + rect[3]/2)
                pos = (x,y)
                # Add a black circle (override darkness) where the target is located
                pygame.draw.circle(self.layer,self.color,pos,radius)

    def draw(self):
        gameDisplay.blit(self.layer,(0,0)) # pastes the translucent, black surface onto the screen


class Frame(Entity): # a chunk of the background
    def __init__(self,pos,w=0,h=0,img=None):
        super(Frame,self).__init__(pos,w,h,img)
        del self.hitbox # useless
        self.passed_screen = False
        self.color = dark_blue # default

class Background():
    # Background consists of 2 copies (joined seamlessly) - when one moves off screen (left), it will be placed behind the other image (right)
    def __init__(self,frames,bg=None,w=display_width,h=display_height,speed=None):
        self.background_image = bg
        self.width = w
        self.height = h
        self.frames = []
        self.passed_screen = False
        if speed:
            self.speed = speed
        else:
            self.speed = screen_speed
        y = 0
        for i in range(frames):
            x = self.width * i
            pos = (x,y) # starts at topleft
            new_frame = Frame(pos,w=self.width,h=self.height,img=self.background_image)
            self.frames.append(new_frame) # add these 2 frames to a collection

    def scroll(self):
        for current_frame in self.frames:
            current_frame.x -= self.speed # move to the left
            if current_frame.x + current_frame.width <= 0: # frame went off the screen
                current_frame.passed_screen = True

        # now reset frame positions if necessary
        for current_frame in self.frames:
            if current_frame.passed_screen:
                frame_index = self.frames.index(current_frame)
                last_frame = self.frames[frame_index-1] # the last frame in the order (rightmost) must have be at position (frame_index-1)
                current_frame.x = last_frame.x + last_frame.width # move current frame behind the other
                # print(current_frame.x) ++
                self.update(current_frame) # update its image (if it has a new one pending)
                current_frame.passed_screen = False # its position has been reset ++

    def update(self,new_frame):
        new_frame.image = self.background_image # change the frame's background image

    def draw(self):
        for current_frame in self.frames:
            new_pos = (current_frame.x,current_frame.y)
            width = current_frame.width
            height = current_frame.height
            if not current_frame.image:
                pygame.draw.rect(gameDisplay,current_frame.color,(new_pos[0],new_pos[1],current_frame.width,current_frame.height))
            else:
                gameDisplay.blit(current_frame.image,new_pos)

class Button(): # buttons for menus
    def __init__(self,pos,act_img,inact_img,):
        self.active_image = act_img
        self.inactive_image = inact_img
        self.active = False # is the button being activated (hovered)
        self.action = None # what effect happens once the button is clicked
        self.name = None # give buttons names to specifically control what they do when clicked
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.active_image.get_width()
        self.height = self.active_image.get_height()

    def click(self):
        # common button functionalities
        if self.name == 'quit':
            quit_game()
        elif self.name == 'start':
            start_game()
        elif self.name == 'controls':
            display_controls()
        else:
            if self.action: # specific button function
                try:
                    self.action()
                except:
                    print('This button does not have an executable action!\n')

    def contains(self,point):
        # check if a point lies within the bounds of the button
        inside = False
        if point[0] < self.x + self.width and point[0] > self.x:
            if point[1] < self.y + self.height and point[1] > self.y:
                inside = True
        return inside

    def draw(self):
        if self.active:
            current_image = self.active_image
        else:
            current_image = self.inactive_image
        gameDisplay.blit(current_image,(self.x,self.y))

class Animation_Event():
    def __init__(self,t,dur,r,type,img=None):
        self.start_time = t
        self.original_start = self.start_time
        self.duration = dur # time till completion
        self.end_time = 0 
        self.repeat_time = r 
        self.active = False # active or not
        self.pos = (0,0)
        self.image = img
        self.type = type
        self.side = 0

#  --- SECTIONS --- 
#      sections will encompass EVERYTHING (all platforms, obstacles and orbs)
#      empty lists are passed by defualt, to indicate that the specified object is not present in the section
class Section(Entity):
    def __init__(self,s_platforms=[],f_platforms=[],m_platforms=[],hazards=[],orbs=[],ground=False,ceiling=True):
        pos = (0,0) # overide [x] later
        super(Section,self).__init__(pos,w=display_width,h=display_height,img=None)
        del self.image
        del self.hitbox 
        
        self.starting_x = 0 # OVERRIDE this - the leftmost coordinate of where the section is loaded
        self.active = False # on-screen
        self.discard = False # ready to be deleted

        self.ground = ground
        self.ceiling = ceiling
        if self.ground:
            self.ground_platform = Platform((0,500),w=800,h=100) #big long bottom platform
            self.ground_platform.image = ground_tile
        if self.ceiling:
            self.ceiling_platform = Platform((0,-150), 800, 50) #thin roof to keep player on screen   
            self.ceiling_platform.image = None #

        # ALL values passed are LISTS (except x)
        # f = falling platforms
        # m = moving platforms
        # s = stationary (regular) platforms
    
        self.stationary_platforms = s_platforms.copy()
        self.falling_platforms = f_platforms.copy()
        self.moving_platforms = m_platforms.copy()
        self.all_platforms = s_platforms.copy() # list of all surfaces you can touch - MAKE A COPY++
        self.all_platforms.extend(self.falling_platforms)
        self.all_platforms.extend(self.moving_platforms)

        self.hazards = hazards # list of all hazards that can kill you (moving or not)
        self.all_obstacles = []
        self.all_obstacles.extend(self.hazards)
        self.all_obstacles.extend(self.all_platforms)

        self.orbs = orbs.copy()

        self.all_entities = [] # list of all things you can see on the screen (except background)
        self.all_entities.extend(self.all_obstacles)
        self.all_entities.extend(self.orbs)

    def scroll(self):
        # first move the imaginary frame of the section
        self.x -= screen_speed
        # move all contents (only if the frame is on-screen)
        if self.active:
            for target in self.all_entities:
                target.x -= screen_speed
                target.hitbox.x -= screen_speed
                if hasattr(target,'path'): # Moving objects must have their path moved as well
                    for point in target.path:
                        x = point[0]
                        y = point[1]
                        x -= screen_speed
                        index = target.path.index(point)
                        target.path[index] = (x,y) # update the point in the path

        # Check Discard
        if self.x + self.width < 0: # gone off-screen LEFT, never coming back - put up a sign that says delete this section
            self.discard = True

    def refresh_contents(self): # This happens once per activation++
        # to save computational memory, only an imaginary box will move each frame of the game
        # once the box is on screen, all the objects in that section will be updated to travel the same distance the box travelled
        if self.ground:
            self.all_platforms.append(self.ground_platform)
            self.all_entities.append(self.ground_platform) # add to complete list
        if self.ceiling:
            self.all_platforms.append(self.ceiling_platform)
            self.all_entities.append(self.ceiling_platform) # add to complete list
        # Frame Shift
        x_change = self.x - self.starting_x
        for target in self.all_entities:
            target.x += x_change
            target.hitbox.x += x_change

    def check_active(self):
        # is this section on screen
        left_onscreen = False
        right_onscreen = False
        if self.x < display_width and self.x >= 0: # between borders, or on left border
            left_onscreen = True
        elif self.x + self.width < display_width and self.x + self.width > 0: # between borders
            right_onscreen = True
        # make section active
        if left_onscreen or right_onscreen:
            if not self.active:
                self.refresh_contents() # if this section is just becoming active, refresh its contents (saves memory)
            self.active = True
        else:
            self.active = False #@
    
    # Draw Order: Background - Platforms - Hazards - Player - Enemies - Projectiles - Orbs
    def draw_platforms(self):
        for new_platform in self.all_platforms: # Platforms
            if new_platform.image: # platforms may need to be invisible
                gameDisplay.blit(new_platform.image,(new_platform.x,new_platform.y))
    def draw_hazards(self):
        for new_hazard in self.hazards: # Hazards
            gameDisplay.blit(new_hazard.image,(new_hazard.x,new_hazard.y))
    def draw_orbs(self):
        for new_orb in self.orbs: # Orbs
            gameDisplay.blit(new_orb.image,(new_orb.x,new_orb.y))


# --- GLOBAL VARIABLES (continued) ---
# Sections/enemies are loaded here because they are permanent and should only be created ONCE, after the program is run

# Enemy Spawn Rates: chance (%) for enemy to spawn once triggered
# - These values will be overriden when the game starts
abyss_spawn_rate = 0
tormentor_spawn_rate = 0
purple_ghost_spawn_rate = 0
pink_ghost_spawn_rate = 0

# SECTION BUILDER (construct preset sections here)
# (build here)

# WORLD 1
# WORLD 2
# WORLD 3
# WORLD 4
# WORLD 5
# WORLD 6
# BASIC SET


# TRASH BELOW:
#Starting Sections
orb_0_1 = Light_Orb((center_screen[0]-75,display_height-50))
orb_0_2 = Light_Orb((center_screen[0],display_height-100))
orb_0_3 = Light_Orb((center_screen[0]+75,display_height-50))
orbs_0 = [orb_0_1,orb_0_2,orb_0_3]
p_0 = Platform((0,500),w=300,h=100)
p_01 = Platform((500,500),w=300,h=100)
p_0 = [p_0,p_01]
section_0_a = Section(orbs=orbs_0,s_platforms=p_0) # A-type (hole learning)

orb_0_1 = Light_Orb((center_screen[0]-150,225))
orb_0_2 = Light_Orb((center_screen[0]-25,375))
orb_0_3 = Light_Orb((center_screen[0]+100,225))
orbs_0_b = [orb_0_1,orb_0_2,orb_0_3]
fp_0_1 = Falling_Platform((center_screen[0]-25,300))
fp_0 = [fp_0_1]
pp_0_1 = Platform((center_screen[0]-100,425),passable=True)
pp_0_2 = Platform((center_screen[0]-25,325),passable=True)
pp_0_3 = Platform((center_screen[0]+50,425),passable=True)
pp_0 = [pp_0_1,pp_0_2,pp_0_3]

section_0_b = Section(orbs=orbs_0_b,ground=True,s_platforms=pp_0,f_platforms=fp_0) # B-type (passable/falling platform learning)

orb_0_1 = Light_Orb((375,250))
orb_0_2 = Light_Orb((428,100))
orb_0_3 = Light_Orb((425,450))
orbs_0_c = [orb_0_1,orb_0_2,orb_0_3]
p_0 = Platform((200,450),w=150)
p_01 = Platform((425,200),h=250)
p_02 = Platform((550,450),w=150)
p_0 = [p_0,p_01,p_02]
for p in p_0:
    p.choose_image()
section_0_c = Section(orbs=orbs_0_c,ground=True,s_platforms=p_0) # C-type (wall-jump learning)

#section_0_d = Section(orbs=orbs_0_c,ground=True,s_platforms=p_0) # D-type (slippery block learning)

#Easy Sections 1-4
#section 1
platform_1_1 = Platform((200, 400), 50, 50)
platform_1_2 = Platform((250, 400), 50, 50)
platform_1_3 = Platform((450, 300), 50, 200)
platforms_1 = [platform_1_1, platform_1_2, platform_1_3]
for p in platforms_1:
    p.choose_image()

orb_1_1 = Light_Orb((250, 350), 50, 50)
orb_1_2 = Light_Orb((450, 250), 50, 50)
orbs_1 = [orb_1_1, orb_1_2]

section_1 = Section(s_platforms=platforms_1, orbs=orbs_1,ground=True)

#section 2
platform_2_1 = Platform((100, 400), 50, 50)
platform_2_2 = Platform((250, 300), 50, 50)
platform_2_3 = Platform((400, 200), 50, 50)
platform_2_4 = Platform((550, 100), 50, 50)
platform_2_5 = Platform((750, 100), 50, 400) # extra long platform
platforms_2 = [platform_2_1, platform_2_2, platform_2_3, platform_2_4, platform_2_5]
for p in platforms_2:
    p.choose_image()

orb_2_1 = Light_Orb((400, 150), 50, 50)
orb_2_2 = Light_Orb((750, 50), 50, 50)
orbs_2 = [orb_2_1, orb_2_2]

section_2 = Section(s_platforms=platforms_2,orbs=orbs_2,ground=True)

#section 3
spike_3_1 = Spikes((center_screen[0] -200, 450), 50, 50)
spike_3_2 = Spikes((center_screen[0], 450), 50, 50)
spike_3_3 = Spikes((center_screen[0] +200, 450), 50, 50)
spikes_3 = [spike_3_1, spike_3_2, spike_3_3]

orbs_3_1 = Light_Orb((250, 450), 50, 50)
orbs_3_2 = Light_Orb((450, 450), 50, 50)
orbs_3_3 = Light_Orb((650, 450), 50, 50)
orbs_3 = [orbs_3_1, orbs_3_2, orbs_3_3]

section_3 = Section(hazards=spikes_3, orbs=orbs_3,ground=True)

#section_4
platform_4_1 = Platform((center_screen[0] -200, 400), 50, 50)
platform_4_2 = Platform((400, 300), 50, 200)

platforms_4 = [platform_4_1, platform_4_2]
for p in platforms_4:
    p.choose_image()

spike_4_1 = Spikes((center_screen[0] + 50, 450), 50, 50)
spike_4_2 = Spikes((center_screen[0] + 100, 450), 50, 50)
spike_4_3 = Spikes((center_screen[0] + 150, 450), 50, 50)
spike_4_4 = Spikes((center_screen[0] + 200, 450), 50, 50)
spikes_4 = [spike_4_1, spike_4_2, spike_4_3, spike_4_4]

orb_4_1 = Light_Orb((200, 350), 50, 50)
orb_4_2 = Light_Orb((450, 250), 50, 50)
orbs_4 = [orb_4_1, orb_4_2]

section_4 = Section(s_platforms=platforms_4, hazards=spikes_4, orbs=orbs_4,ground=True)

#Medium Sections 5-10:
#section 5
platform_5_1 = Platform((200, 400), 50, 50)
platform_5_2 = Platform((400, 400), 50, 50)
platform_5_3 = Platform((600, 400), 50, 50)
platforms_5 = [platform_5_1, platform_5_2, platform_5_3]
for p in platforms_5:
    p.choose_image()

spike_5_1 = Spikes((center_screen[0] -200, 450), 50, 50)
spike_5_2 = Spikes((center_screen[0] -150, 450), 50, 50)
spike_5_3 = Spikes((center_screen[0] -100, 450), 50, 50)
spike_5_4 = Spikes((center_screen[0] -50, 450), 50, 50)
spike_5_5 = Spikes((center_screen[0], 450), 50, 50)
spike_5_6 = Spikes((center_screen[0] +50, 450), 50, 50)
spike_5_7 = Spikes((center_screen[0] +100, 450), 50, 50)
spike_5_8 = Spikes((center_screen[0] +150, 450), 50, 50)
spike_5_9 = Spikes((center_screen[0] +200, 450), 50, 50)
spikes_5 = [spike_5_1, spike_5_2, spike_5_3, spike_5_4, spike_5_5, spike_5_6, spike_5_7, spike_5_8, spike_5_9]

orb_5_1 = Light_Orb((400, 350), 50, 50)
orb_5_2 = Light_Orb((700, 550), 50, 50)
orbs_5 = [orb_5_1, orb_5_2]

section_5 = Section(s_platforms=platforms_5, hazards=spikes_5, orbs=orbs_5,ground=True)

#section 6
platform_6_1 = Platform((200, 400), 50, 50)
platform_6_2 = Platform((400, 400), 50, 50)
platform_6_3 = Platform((600, 300), 50, 200)
platforms_6 = [platform_6_1, platform_6_2, platform_6_3]
for p in platforms_6:
    p.choose_image()



spike_6_1 = Spikes((center_screen[0] -200, 450), 50, 50)
spike_6_2 = Spikes((center_screen[0] -150, 450), 50, 50)
spike_6_3 = Spikes((center_screen[0] -100, 450), 50, 50)
spike_6_4 = Spikes((center_screen[0] -50, 450), 50, 50)
spike_6_5 = Spikes((center_screen[0], 450), 50, 50)
spike_6_6 = Spikes((center_screen[0] +50, 450), 50, 50)
spike_6_7 = Spikes((center_screen[0] +100, 450), 50, 50)
spike_6_8 = Spikes((center_screen[0] +150, 450), 50, 50)
spikes_6 = [spike_6_1, spike_6_2, spike_6_3, spike_6_4, spike_6_5, spike_6_6, spike_6_7, spike_6_8]

orb_6_1 = Light_Orb((400, 350), 50, 50)
orb_6_2 = Light_Orb((700, 450), 50, 50)
orbs_6 = [orb_6_1, orb_6_2]

section_6 = Section(s_platforms=platforms_6, hazards=spikes_6, orbs=orbs_6,ground=True)

#section 7
platform_7_1 = Platform((center_screen[0]+ 150, center_screen[1] + 100), 50, 50)
platform_7_2 = Platform((center_screen[0] + 50, center_screen[1]), 50, 50)
platform_7_3 = Platform((center_screen[0]+ 150, center_screen[1]- 100), 50, 50)
platform_7_4 = Platform((750, 100), 50, 400) #extra long platform
platforms_7 = [platform_7_1, platform_7_2, platform_7_3, platform_7_4, platform_7_4]
for p in platforms_7:
    p.choose_image()

spike_7_1 = Spikes((800, 450), 50, 50)
spikes_7 = [spike_7_1]

orb_7_1 = Light_Orb((450, 250), 50, 50)
orb_7_2 = Light_Orb((550, 150), 50, 50)
orb_7_3 = Light_Orb((750, 50), 50, 50)
orbs_7 = [orb_7_1, orb_7_2, orb_7_3]

section_7 = Section(s_platforms=platforms_7, hazards=spikes_7, orbs=orbs_7,ground=True)

#section 8
platform_8_1 = Platform((200, 400), 50, 50)
platform_8_2 = Platform((300, 300), 50, 50)
platform_8_3 = Platform((400, 300), 50, 200)
platform_8_4 = Platform((550, 0), 50, 250)
platforms_8 = [platform_8_1, platform_8_2, platform_8_3, platform_8_4]
for p in platforms_8:
    p.choose_image()

spike_8_1 = Spikes((400, 250), 50, 50)
spike_8_2 = Spikes((550, 250), 50, 50)
spike_8_3 = Spikes((600, 450), 50, 50)
spikes_8 = [spike_8_1, spike_8_2, spike_8_3]

orb_8_1 = Light_Orb((200, 350), 50, 50)
orb_8_2 = Light_Orb((450, 300), 50, 50)
orb_8_3 = Light_Orb((650, 450), 50, 50)
orbs_8 =[orb_8_1, orb_8_2, orb_8_3]

section_8 = Section(s_platforms=platforms_8, hazards=spikes_8, orbs=orbs_8,ground=True)

#section 9
platform_9_1 = Platform((300, 100), 50, 400, spawnable=False) #extra long platform
platform_9_2 = Platform((400,0), 50, 350) #extra long platform
platform_9_3 = Platform((700, 250), 50, 350, spawnable=False) #extra long platform
platforms_9 = [platform_9_1, platform_9_2, platform_9_3]
for p in platforms_9:
    p.choose_image()

spike_9_1 = Spikes((650, 450), 50, 50)
spikes_9 = [spike_9_1]

orb_9_1 = Light_Orb((350, 150), 50, 50)
orb_9_2 = Light_Orb((350, 200), 50, 50)
orb_9_3 = Light_Orb((350, 250), 50, 50)
orbs_9 =[orb_9_1, orb_9_2, orb_9_3]

section_9 = Section(s_platforms=platforms_9, hazards=spikes_9, orbs=orbs_9,ground=True)

#section 10
platform_10_1 = Platform((200, 400), 50, 50)
platform_10_2 = Platform((350, 400), 50, 50)
platform_10_3 = Platform((550, 100), 50, 400, spawnable=False)
platform_10_4 = Platform((700, 100), 100, 50)
platforms_10 = [platform_10_1, platform_10_2, platform_10_3, platform_10_4]
for p in platforms_10:
    p.choose_image()

spike_10_1 = Spikes((200, 450), 50,50)
spike_10_2 = Spikes((250, 450), 50,50)
spike_10_3 = Spikes((300, 450), 50,50)
spike_10_4 = Spikes((350, 450), 50,50)
spike_10_5 = Spikes((400, 450), 50,50)
spike_10_6 = Spikes((450, 450), 50,50)
spike_10_7 = Spikes((500, 450), 50,50)
spike_10_8 = Spikes((650, 100), 50, 50)
spikes_10 = [spike_10_1, spike_10_2, spike_10_3, spike_10_4, spike_10_5, spike_10_6, spike_10_7, spike_10_8]

orb_10_1 = Light_Orb((500, 200), 50, 50)
orb_10_2 = Light_Orb((500, 300), 50, 50)
orb_10_3 = Light_Orb((500, 400), 50, 50)
orbs_10 = [orb_10_1, orb_10_2, orb_10_3]

section_10 = Section(s_platforms=platforms_10, hazards=spikes_10, orbs=orbs_10,ground=True)

#section 11
platform_11_1 = Platform((200, 450), 50, 50)
platform_11_2 = Platform((100, 350), 50, 50)
platform_11_3 = Platform((200, 250), 50, 50)
platform_11_4 = Platform((100, 150), 50, 50)
platform_11_5 = Platform((300, 100), 50, 500)
platform_11_6 = Platform((550, 0), 50, 300)
platform_11_7 = Platform((350, 300), 100, 50)
platforms_11 = [platform_11_1, platform_11_2, platform_11_3, platform_11_4, platform_11_5, platform_11_6, platform_11_7]
for p in platforms_11:
    p.choose_image()

spike_11_1 = Spikes((350, 450), 50, 50)
spike_11_2 = Spikes((400, 450), 50, 50)
spike_11_3 = Spikes((450, 450), 50, 50)
spikes_11 = [spike_11_1, spike_11_2, spike_11_3]

orb_11_1 = Light_Orb((150, 250), 50, 50)
orb_11_2 = Light_Orb((300, 50), 50, 50)
orb_11_3 = Light_Orb((600, 300), 50, 50)
orbs_11 = [orb_11_1, orb_11_2, orb_11_3]

section_11 = Section(s_platforms=platforms_11, hazards=spikes_11, orbs=orbs_11,ground=True)

#section 12
platform_12_1 = Platform((0, 0), 50, 400)
platform_12_2 = Platform((50, 350), 150, 50)
platform_12_3 = Platform((300, 250), 50, 250)
platform_12_4 = Platform((650, 350), 50, 50)
platforms_12 = [platform_12_1, platform_12_2, platform_12_3, platform_12_4]
for p in platforms_12:
    p.choose_image()

spike_12_1 = Spikes((50,300),50, 50)
spike_12_2 = Spikes((350, 450), 50, 50)
spike_12_3 = Spikes((400, 450), 50, 50)
spike_12_4 = Spikes((450, 450), 50, 50)
spike_12_5 = Spikes((600, 450), 50, 50)
spike_12_6 = Spikes((650, 450), 50, 50)
spike_12_7 = Spikes((700, 450), 50, 50)
spikes_12 = [spike_12_1, spike_12_2, spike_12_3, spike_12_4, spike_12_5, spike_12_6, spike_12_7]

orb_12_1 = Light_Orb((50, 200), 50, 50)
orb_12_2 = Light_Orb((350, 300), 50, 50)
orb_12_3 = Light_Orb((600, 350), 50, 50)

section_12 = Section(s_platforms=platforms_12, hazards=spikes_12, orbs= orbs_1,ground=True)

#section 13 
platform_13_1 = Platform((200, 350), 50, 150)
platform_13_2 = Platform((400, 350), 50, 150)
platform_13_3 = Platform((600, 350), 50, 150)
platforms_13 = [platform_13_1, platform_13_2, platform_13_3]
for p in platforms_13:
    p.choose_image()

moving_spike_13_1 = Moving_Spikes([(200,300), (600, 300)], 50, 50)
spikes_13 = [moving_spike_13_1]

orb_13_1 = Light_Orb((250, 350), 50, 50)
orb_13_2 = Light_Orb((450, 350), 50, 50)
orb_13_3 = Light_Orb((650, 350), 50, 50)
orbs_13 = [orb_13_1, orb_13_2, orb_13_3]

section_13 = Section(s_platforms=platforms_13, hazards=spikes_13, orbs=orbs_13,ground=True)

#section 14 #######################################################UNFINISHED DP!DP!
#platform_14_1 =

#spike_14_1 = 
spikes_14 = []

#section_14 = Section(s_platforms=platforms_14, hazards=spikes_14, orbs=orbs_14)

#section 15
platform_15_1 = Platform((200, 400), 50, 50)
platform_15_2 = Platform((350, 300), 50, 50)
platform_15_3 = Platform((500, 250), 50, 50)
platform_15_4 = Platform((550, 0), 50, 100)
platform_15_5 = Platform((550, 400), 50, 100)
platforms_15 = [platform_15_1, platform_15_2, platform_15_3, platform_15_4, platform_15_5]
for p in platforms_15:
    p.choose_image()

spike_15_1 = Spikes((550, 100), 50, 50)
spike_15_2 = Spikes((550, 350), 50, 50)
spike_15_3 = Spikes((600, 450), 50, 50)
spikes_15 = [spike_15_1, spike_15_2, spike_15_3]

orb_15_1 = Light_Orb((200, 350), 50, 50)
orb_15_2 = Light_Orb((400, 300), 50, 50)
orb_15_3 = Light_Orb((700, 450), 50, 50)
orbs_15 = [orb_15_1,orb_15_2,orb_15_3]

section_15 = Section(s_platforms=platforms_15, hazards=spikes_15, orbs=orbs_15,ground=True)

#section 16
platform_16_1 = Platform((200, 300), 50, 50, spawnable=False)
platform_16_2 = Platform((350, 300), 50, 50, spawnable=False)
platform_16_3 = Platform((500, 300), 50, 50, spawnable=False)
platform_16_4 = Platform((650, 300), 50, 50, spawnable=False)
platforms_16 = [platform_16_1, platform_16_2, platform_16_3, platform_16_4]
for p in platforms_16:
    p.choose_image()

spike_16_1 = Spikes((250, 250), 50, 50)
spike_16_2 = Spikes((400, 250), 50, 50)
spike_16_3 = Spikes((550, 250), 50, 50)
spike_16_4 = Spikes((700, 250), 50, 50)
spike_16_5 = Spikes((200, 450), 50, 50)
spike_16_6 = Spikes((250, 450), 50, 50)
spike_16_7 = Spikes((300, 450), 50, 50)
spike_16_8 = Spikes((350, 450), 50, 50)
spike_16_9 = Spikes((400, 450), 50, 50)
spike_16_10 = Spikes((450, 450), 50, 50)
spike_16_11 = Spikes((500, 450), 50, 50)
spikes_16 = [spike_16_1, spike_16_2, spike_16_3, spike_16_4, spike_16_5, spike_16_6, spike_16_7, spike_16_8, spike_16_9, spike_16_10, spike_16_11]

orb_16_1 = Light_Orb((550, 450), 50, 50)
orb_16_2 = Light_Orb((600, 450), 50, 50)
orb_16_3 = Light_Orb((650, 450), 50, 50)
orbs_16 = [orb_16_1,orb_16_2,orb_16_3]

section_16 = Section(s_platforms=platforms_16, hazards=spikes_16, orbs=orbs_16,ground=True)

# SECTION POOLS *
spawn_sections = [section_0_a,section_0_b,section_0_c] # sections the player starts here
easy_sections = [section_1,section_2,section_3,section_4] # all easy sections here
medium_sections = [section_5,section_6,section_7,section_8,section_9,section_10] # all medium sections here
hard_sections = [] # all hard sections here
very_hard_sections = [section_11,section_12,section_13,section_15,section_16] # all very hard sections here


# --- FUNCTIONS ---
def choose_background(subworld): # select bg based on current subworld
    global worlds # access to all world names
    bg = None #***

    return bg

def create_text(msg,s,f,fc,bc):
    font = pygame.font.SysFont(f,size=s) # create new font
    text = font.render(msg,True,fc,bc)
    text_rect = text.get_rect()
    return text, text_rect # surface, bounds

def choose_entrace():
    chosen_entrace = None
    x = random.randint(1,6)
    chosen_entrace = purple_entrance
    if not chosen_entrace:
        print('ERROR-CHOOSING-ENTRANCE')
    return chosen_entrace

def run_menu(): # Main Menu will go here - (for now it just runs game immediately)
    local_fps = 20
    debug_mode = False
    invincible_mode = False # hidden modes
    variation = 0 # index of entrance/background, will drawing be shiny
    variation = random.randint(0,1) # @

    skip_frame = False
    animation_activated = False # when the screen can start animating
    animation_counter = 0
    animation_end = 96 # time the animation ends (193 seconds is entire song) - offset 0.5 sec
    animation_reset = False

    starting = False # starting game
    start_delay = 0.50 # seconds
    start_counter = 0

    entrance_layer = choose_entrace() # select a new entrance

    black_screen = pygame.Surface((display_width,display_height))
    black_screen.convert(black_screen)
    black_screen.fill(black)

    fade_counter = 0
    fade_time = 9.0 # seconds
    final_transparency = 255 # how dark the screen will eventually get
    value = final_transparency / (fade_time*local_fps) # the amount the screen should get darker each frame
    fade_dir = 1 # darkening

    black_title = pygame.Surface((528,176)).convert() # static
    black_title.convert(black_title)
    black_title.fill(black)
    black_title.set_alpha(0)
    black_title_pos = (138,13) # static

    title_fading = False
    title_fade_time = 16.0 # seconds
    title_fade_counter = -1 # disable
    title_fade_start = 30
    title_fade_end = 75 # complete end
    title_fade_dir = 1 # dark
    title_value = final_transparency / (title_fade_time*local_fps)

    turn_count = 0
    hyper = False
    hyper_duration = 2
    hyper_cooldown = 0
    terrified = False
    terrified_counter = 0
    terrified_duration = 1.25 # seconds
    fear_counter = 0
    face_dir = -1 # left (or right)
    direction_counter = 0 # chance to change directions twice per second

    # additional layers
    dark_clouds = cloud_background
    dark_clouds.set_alpha(0)
    clouds_fade_time = 26
    clouds_fade_counter = 0
    clouds_fade_dir = 1
    clouds_value = 180 / (clouds_fade_time*local_fps)
    clouds_alpha = 0
    fog_overlay = Background(2,dark_clouds) # overlay
    #for f in range(len(fog_overlay.frames)): # both frames start off-screen - not if they fade
    #    fog_overlay.frames[f].x = 800 + f*fog_overlay.frames[f].width
    wink = pygame.Surface((2,4)).convert()
    wink.fill(cb_yellow)
    wink_right_pos = (404,272)
    wink_left_pos = (396,272)
    winking = False

    # Animation Events
    event_1 = Animation_Event(fade_time,3,7,1,scary_face_red)
    event_2 = Animation_Event(6+fade_time,5,9,2,scary_face_purple)
    event_3 = Animation_Event(14+fade_time,7,20,3,large_ghost_img) #10
    event_4 = Animation_Event(4+fade_time,1.5,16,4)
    event_list = [event_1,event_2,event_3,event_4]

    # Spcial attributes
    event_1.side = 0 # left, right or 0-non-existent
    event_1.animation_delay = 0
    event_1.animation_counter = 0
    event_1.path_range = 12 #!
    event_1.speed = 3 #!
    event_1.width = event_1.image.get_width()
    event_1.height = event_1.image.get_height()
    event_1.path_counter = [0,0] # (x,y)
    event_2.side = 0
    event_2.image = scary_face_purple.convert_alpha()
    event_2.width = event_2.image.get_width()
    event_2.height = event_2.image.get_height()
    event_2.alpha_increase = 180 // (event_2.duration * local_fps) #! final alpha (180)
    event_3.image = large_ghost_img
    event_3.width = event_3.image.get_width()
    event_3.height = event_3.image.get_height()
    event_3.mod_counter = 0
    event_3.mod_dir = -1
    event_3.amplitude = int(event_3.height*0.25)
    event_3.mod_speed = 4
    event_4.strike = 0
    event_4.strike_chance = 10 # chance for lightning to strike, while active

    left_zone = (32,186,224,414)
    right_zone = (544,186,224,414)
    top_zone = (0,0,800,479) # old 392
    side_taken = 0 # 1-left, 2-right, 0-none

    # Buttons
    spacing = 13
    start_button = Button((0,0),active_start,inactive_start) # BUTTON
    start_button.name = 'start'
    start_button.active = True
    x = center_screen[0] - start_button.width*0.5
    y = display_height*0.7033 - start_button.height*0.5 #! 422
    start_button.x = x
    start_button.y = y
    y += start_button.height + spacing

    controls = Button((0,0),active_controls,inactive_controls) # BUTTON
    controls.name = 'controls'
    x = center_screen[0] - controls.width*0.5
    controls.x = x
    controls.y = y
    y += controls.height + spacing

    spacing = 4

    quit_btn = Button((0,0),active_quit,inactive_quit) # BUTTON
    quit_btn.name = 'quit'
    x = center_screen[0] - quit_btn.width*0.5
    quit_btn.x = x
    quit_btn.y = y

    button_list = [start_button,controls,quit_btn] # list of buttons

    button_pressed = [False,False] # (up,down)
    active_index = 0 # which button is current selected, -1 is nothing selected
    mouse_moved = False # did the mouse move THIS FRAME
    cursor_pos = (0,0)

    running = True

    while running:
        # LIST OF EVENTS TRIGGERED:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION: # cursor moved
                mouse_moved = True
                cursor_pos = pygame.mouse.get_pos() # update the cursor's location
            else:
                mouse_moved = False
            if event.type == pygame.QUIT: # X-button
                quit_game()

        animation_counter += 1 # always adding
        # CHECK ANIMATION CYCLE
        if animation_counter >= animation_end * local_fps: # complete animation has ran through
            animation_reset = True
        # RESET ANIMATION
        if animation_reset:
            animation_activated = False
            entrance_layer = choose_entrace()
            # counters
            animation_counter = 0 # main counter
            fear_counter = 0 # player state counter
            direction_counter = 0 # player direction counter
            terrified_counter = 0 # state duration counter
            # reset states
            terrified = False
            hyper = False
            hyper_cooldown = 0 # unnecessary
            turn_count = 0
            face_dir = -1 # face left to start
            # reset fades
            black_screen.set_alpha(0)
            fade_dir = 1 # starts by getting darker
            fade_counter = 0 # reset counter
            title_fade_dir = 0
            title_fade_counter = -1 # disable
            black_title.set_alpha(0)
            for f in fog_overlay.frames:
                f.image.set_alpha(0)
            clouds_fade_counter = 0
            clouds_fade_dir = 1
            # end current events
            for event in event_list:
                event.active = False
            # reset events
            event_1.start_time = event_1.original_start
            event_2.start_time = event_2.original_start
            event_3.start_time = event_3.original_start
            event_4.start_time = event_4.original_start
            # finished the reset - wait for another call
            animation_reset = False


        # SCREEN FADE
        # determine if fading, and direction
        if animation_counter >= (animation_end - fade_time) * local_fps and fade_dir != -1: # unfade
            fade_dir = -1
            fade_counter = 0 # reset counter

        # set alpha
        if fade_counter < fade_time * local_fps:
            fade_counter += 1
            if fade_dir == 1: # FADING (set value)
                alpha = value * fade_counter # getting darker
            elif fade_dir == -1:
                alpha = 255 - (value*fade_counter) # getting lighter
            black_screen.set_alpha(alpha) # set level of darkness to the layer
        else:
            animation_activated = True # static alpha 255 (do not set)


        # TITLE FADE
        # determine if fading, and direction
        title_fading = False
        if title_fade_counter < (title_fade_time * local_fps) and title_fade_counter > -1: # -1 is disabled
            title_fading = True

        if animation_counter == int((title_fade_end - title_fade_time) * local_fps):
            title_fade_dir = -1 # get lighter
            title_fade_counter = 0 # reset counter to fade again
        elif animation_counter == int(title_fade_start * local_fps):
            title_fade_dir = 1 # darker
            title_fade_counter = 0

        # TITLE FADING
        if title_fading:
            title_fade_counter += 1 # increment
            if title_fade_dir == 1:
                title_alpha = title_value * title_fade_counter # darker
            elif title_fade_dir == -1:
                title_alpha = 255 - (title_value*title_fade_counter) # lighter
            black_title.set_alpha(title_alpha) # darkness level


        # CHOOSE ANIMATION
        direction_counter += 1
        if direction_counter >= 0.5 * local_fps and not hyper: # twice per second ~ 1 flip every 3 seconds
            direction_counter = 0 # reset counter
            change_dir = random.randint(1,100)
            change_chance = 17
            if change_dir <= change_chance:
                face_dir *= -1 # flip direction
            else:
                pass # keep the same dir

        elif direction_counter >= 0.25 * local_fps and hyper: # 4 per second ~ 3-5 flips over 2 seconds
            direction_counter = 0
            change_dir = random.randint(1,100)
            change_chance = 45
            if change_dir <= change_chance:
                face_dir *= -1 # flip direction
                turn_count += 1
            hyper_cooldown -= 1
            if turn_count >= 5: # hyper results in a max of 5 turns
                hyper_cooldown = 0
            if hyper_cooldown == 0:
                hyper = False
                turn_count = 0

        # fear
        fear_counter += 1
        if fear_counter >= 0.5 * local_fps and terrified_counter == 0: # twice per second
            fear_counter = 0
            new_terror = 10 # default chance ~ 1/7secs
            t_target = 0 # represents a new level of fear
            for event in event_list:
                if event.active and (event.type == 1 or event.type == 2): # takes priority, scariest
                    if event.side == 1 and face_dir == -1 and not terrified: # left
                        t_target = 100 # must become terrified when first seeing it
                    elif event.side == 2 and face_dir == 1 and not terrified: # right
                        t_target = 100
                    # same set, already terrified
                    if event.side == 1 and face_dir == -1: # left
                        t_target = 75 
                    elif event.side == 2 and face_dir == 1: # right
                        t_target = 75
                elif event.active and event.type == 3:
                    t_target = 35
                # update chance to be terrified
                if t_target > new_terror:
                    new_terror = t_target

            # decide, terror
            terror_chance = random.randint(1,100)
            if terror_chance <= new_terror:
                terrified = True
                terrified_counter = int(terrified_duration * local_fps)
            else:
                terrified = False

        # Terrified cooldown
        if terrified_counter > 0:
            if not hyper and terrified_counter % 20 == 0: # < once/10seconds
                hyper_chance = random.randint(1,10) # 10%
                if hyper_chance == 1:
                    hyper = True
                    hyper_cooldown = hyper_duration*local_fps #! 2 second hyper
            terrified_counter -= 1 # countdown

        # choose image
        if face_dir == -1:
            animation_set = title_screen_set_rev
        else:
            animation_set = title_screen_set
        if terrified:
            cb_overlay = animation_set[2]
        else:
            cb_overlay = animation_set[1]

        # Animation Events Triggered:
        for event in event_list:
            if animation_counter >= event.start_time * local_fps and event.start_time: # event 1 triggered
                event.active = True
                event.end_time = event.start_time + event.duration
                if event.repeat_time != 0:
                    event.start_time = event.end_time + event.repeat_time # set a new time to start
                else:
                    event.start_time = None
                # position
                if event.type == 1 or event.type == 2:
                    if event.type == 1:
                        side_taken = event_2.side
                    elif event.type == 2:
                        side_taken = event_1.side
                    else:
                        print('ANIMATION-SIDE-ERROR')

                    if side_taken == 0:
                        new_side = random.randint(1,2)
                    else:
                        new_side = side_taken - 1
                        if new_side == 0:
                            new_side = 2
                    event.side = new_side # hold side
                    if new_side == 1: # left
                        zone = left_zone
                        if event.type == 1:
                            event.image = pygame.transform.flip(scary_face_red,True,False)
                        elif event.type == 2:
                            event.image = pygame.transform.flip(scary_face_purple,True,False)
                    else: # right
                        zone = right_zone
                        if event.type == 1:
                            event.image = scary_face_red
                        elif event.type == 2:
                            event.image = scary_face_purple

                    # choose position
                    x = random.randint(zone[0],int(zone[0]+zone[2]-event.width))
                    y = random.randint(zone[1],int(zone[1]+zone[3]-event.height))
                    event.pos = [x,y]
                    if event.type == 1:
                        event_1.animation_delay = random.randint(0,200)/100 # up to 2 seconds
                        new_alpha = random.randint(125,255) # give him a new level of closeness
                        event.image.set_alpha(new_alpha)
                    elif event.type == 2:
                        event.alpha = 0 # reset alpha

                elif event.type == 3: # large ghost
                    new_side = random.randint(1,2)
                    if new_side == 1: # left
                        event.dir = 1
                        x = -event.image.get_width()
                        event.image = pygame.transform.flip(large_ghost_img,True,False)
                    else: # right
                        event.dir = -1
                        x = display_width
                        event.image = large_ghost_img
                    y = random.randint(top_zone[1],int(top_zone[1]+top_zone[3]-event.height))
                    event.pos = [x,y]
                    event.speed = (display_width + event.width) // (event.duration * local_fps)

                elif event.type == 4: # lightning
                    # randomize duration and repeat time
                    event.duration = random.randint(5,25)/10 # from 0.5 to 2.5 seconds
                    event.repeat_time = random.randint(8,20) # from 8 to 20 seconds

        # Enemies or not
        enemies_appeared = False
        for event in event_list:
            if event.active:
                enemies_appeared = True
        if enemies_appeared:
            enemy_overlay = pygame.Surface((800,600),pygame.SRCALPHA,32).convert_alpha()
        else:
            enemy_overlay = None # default

        # ACTIONS - draw ghosts
        if event_1.active: # shake
            if event_1.animation_counter >= event_1.animation_delay * local_fps:
                # check path - boundaries (radius)
                if event_1.path_range - abs(event_1.path_counter[0]) < event_1.speed: # [x]
                    add_x = random.randint(-event_1.speed,0)
                    if event_1.path_counter[0] < 0:
                        add_x *= -1
                else:
                    add_x = random.randint(-event_1.speed,event_1.speed)

                if event_1.path_range - abs(event_1.path_counter[1]) < event_1.speed: # [y]
                    add_y = random.randint(-event_1.speed,0)
                    if event_1.path_counter[0] < 0:
                        add_y *= -1
                else:
                    add_y = random.randint(-event_1.speed,event_1.speed)
                # increase counters
                event_1.path_counter[0] += add_x
                event_1.path_counter[1] += add_y
                # update position
                event_1.pos[0] += add_x
                event_1.pos[1] += add_y
            else:
                event_1.animation_counter += 1
            event_1.image.set_colorkey(black)
            enemy_overlay.blit(event_1.image,(event_1.pos[0],event_1.pos[1]))

        if event_2.active: # transparency
            event_2.image.set_alpha(event_2.alpha)
            event_2.alpha += event_2.alpha_increase
            event_2.image.set_colorkey(black)
            enemy_overlay.blit(event_2.image,(event_2.pos[0],event_2.pos[1]))
        if event_3.active: # move
            event_3.pos[0] += event_3.speed * event_3.dir # update x
            y = event_3.mod_speed * event_3.mod_dir
            event_3.mod_counter += y
            event_3.pos[1] += y
            # check modulation
            if abs(event_3.amplitude - abs(event_3.mod_counter)) < event_3.mod_speed: # half-cycle complete
                event_3.mod_dir *= -1 # flip the direction
            event_3.image.set_colorkey(black)
            enemy_overlay.blit(event_3.image,(event_3.pos[0],event_3.pos[1]))
        if event_4.active: # lightning effect
            event_4.strike = random.randint(1,100) # generate chance for lightning to srike during its activity
            if face_dir == -1:
                lightning_screen = title_screen_set_rev[4] # choose the right layer position
            else:
                lightning_screen = title_screen_set[4]

        # End Events
        for event in event_list:
            if animation_counter >= event.end_time * local_fps: # >= (safetly, for non-integers)
                event.active = False
                if event.type == 1 or event.type == 2:
                    event.side = 0 # nowhere
                    if event.type == 1:
                        event.animation_counter = 0
                elif event.type == 3:
                    event.mod_dir = -1

        # START MENU*
        keys_pressed = pygame.key.get_pressed() # boolean list of all keys currently pressed
        button_select = False
        # KEYDOWNS
        if not mouse_moved:
            # nothing selected right now
            if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and not button_pressed[0]: # move up
                button_select = True
                button_pressed[0] = True
                if active_index == -1:
                    active_index = 0 # start from the first option
                else: # UP
                    if active_index == 0: # reset loop
                        active_index = len(button_list) -1
                    else:
                        active_index -= 1
            elif not keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_w]:
                button_pressed[0] = False # unpressed button

            if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and not button_pressed[1]: # move down
                button_select = True
                button_pressed[1] = True
                if active_index == -1:
                    active_index = 0 # start from the first option
                else: # DOWN
                    if active_index == len(button_list)-1: # reset loop
                        active_index = 0
                    else:
                        active_index += 1
            elif not keys_pressed[pygame.K_DOWN] and not keys_pressed[pygame.K_s]:
                button_pressed[1] = False

            # Unactivate all buttons
            if button_select:
                for new_button in button_list:
                    new_button.active = False
                    # Find the active button, and activate it!
                    if active_index != -1: # something is activated
                        button_list[active_index].active = True

        # ACTIVATE BY CURSOR
        elif mouse_moved:
            active_index = -1 # temporarily disable the index
            for new_button in button_list:
                if new_button.contains(cursor_pos):
                    new_button.active = True
                else:
                    new_button.active = False

        # CLICK BUTTON - enter, space, or leftclick triggers this event
        if keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            for new_button in button_list:
                if new_button.active: # if the button is highlighted, click it
                    new_button.active = False # deactivate, so this menu continues normally
                    if new_button.name == 'start':
                        starting = True # initiate the delay
                    else: # controls button/quit
                        new_button.click()
                        animation_reset = True
                        skip_frame = True # do not display the rest of this animation, reset it first

        if skip_frame:
            skip_frame = False # switch off
            continue # skip the rest of this menu, go to next loop where it resets

        # STARTING - delayed
        if starting:
            # override player overlay
            cb_overlay = animation_set[3] # ready position
            if start_counter >= start_delay * local_fps: # ready to start now
                starting = False # turn start condition on, so player can choose to start next time
                start_counter = 0
                winking = False
                start_game()
                animation_reset = True
                continue # dont draw this frame (old)
            else:
                start_counter += 1
                if start_counter >= (start_delay * local_fps) / 2:
                    # wink for half of the delay
                    winking = True
                    # set wink position
                    if face_dir == -1:
                        new_wink_pos = wink_left_pos
                    else:
                        new_wink_pos = wink_right_pos
                else:
                    winking = False
        
        # move overlay
        if animation_activated and clouds_fade_counter != -1: # ongoing process
            fog_overlay.scroll()
            clouds_fade_counter += 1 # increment
            if clouds_fade_counter >= clouds_fade_time * local_fps: # CHANGE directions
                clouds_fade_counter = 0 # reset
                clouds_fade_dir *= -1 # flip direction
                if clouds_fade_dir == -1 and (clouds_fade_time * 2) * local_fps < animation_counter - (animation_end*local_fps):
                    # about to start darkening again to repeat the cycle,
                    # if another cycle of fading in and back out cannot complete before the animation finishes, do not start another cycle
                    clouds_fade_counter = -1
            if clouds_fade_dir == 1: # darken
                clouds_alpha = clouds_value * clouds_fade_counter # set new alpha
            elif clouds_fade_dir == -1: # lighten
                clouds_alpha = 180 - (clouds_value * clouds_fade_counter) # set new alpha
            for f in fog_overlay.frames: # SET new alpha
                f.image.set_alpha(clouds_alpha)

        # DRAW
        #gameDisplay.fill(black) # background here $
        if not animation_activated: # s.m
            gameDisplay.blit(entrance_layer,(0,0)) # static - entrance (2 variants)
        gameDisplay.blit(black_screen,(0,0)) # darken the screen
        gameDisplay.blit(cb_overlay,(0,0),area=(0,0,800,195)) # title overlay
        gameDisplay.blit(black_title,black_title_pos) # darken title only
        if enemy_overlay:
            gameDisplay.blit(enemy_overlay,(0,0))
        gameDisplay.blit(cb_overlay,(0,195),area=(0,195,800,195)) # player overlay
        if winking:
            gameDisplay.blit(wink,new_wink_pos) # winking (start)
        if event_4.active and event_4.strike <= event_4.strike_chance:
            gameDisplay.blit(lightning_screen,(0,0)) # lightning effect
        if animation_activated:
            fog_overlay.draw()
        for new_button in button_list:
            new_button.draw()

        pygame.display.update()
        clock.tick(local_fps)

def display_controls(): # the controls menu
    local_fps = 20

    # Buttons
    back_button = Button((0,0),active_back,inactive_back) # BUTTON
    x = center_screen[0] - back_button.width*0.5
    y = 541
    back_button.x = x
    back_button.y = y

    mouse_moved = False
    active_index = -1 # only 1 option

    running = True

    while running:
        # LIST OF EVENTS TRIGGERED:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION: # cursor moved
                mouse_moved = True
                cursor_pos = pygame.mouse.get_pos() # update the cursor's location
            else:
                mouse_moved = False
            if event.type == pygame.QUIT: # X-button
                quit_game()

        # MENU
        keys_pressed = pygame.key.get_pressed() # boolean list of all keys currently pressed
        # KEYDOWNS
        if not mouse_moved:
            # nothing selected right now
            if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]: # move up
                active_index = 0

        # ACTIVATE BY CURSOR
        elif mouse_moved:
            active_index = -1 # temporarily disable the index
            if back_button.contains(cursor_pos):
                back_button.active = True
            else:
                back_button.active = False

        # ACTIVE BY BUTTON
        # Find the active button, and activate it!
        if active_index != -1:
            back_button.active = True

        # CLICK BUTTON - enter, space, or leftclick triggers this event
        if keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            if back_button.active: # if the button is highlighted, click it
                return # go back to previous menu

        # DRAW
        #gameDisplay.fill(black) # background here (unnecesary)~
        gameDisplay.blit(controls_menu_img,(0,0))
        back_button.draw()

        pygame.display.update()
        clock.tick(local_fps)

def move_screen(all_entities):# DP! (now for entities that exist outside sections)
    for target in all_entities:
        can_move = True
        if hasattr(target,'anchored'):
            can_move = target.anchored
        if can_move: # must be an entity bound by the screen
            target.x -= screen_speed
            target.hitbox.x -= screen_speed
            if hasattr(target,'path'): # Moving objects must have their path moved as well
                for point in target.path:
                    x = point[0]
                    y = point[1]
                    x -= screen_speed
                    index = target.path.index(point)
                    target.path[index] = (x,y) # update the point in the path

def find_leading_projectile(projectile_list,index):
    # recurse through each projectile in reverse order(recently added first), to find the first projectile that can be shot
    if index < 0: # search ends when the first projectile in the list is reached and cannot be shot
        return None # indicate none can be shot
    elif not projectile_list[index].launched: # can be shot
        return index # send back the index of the projectile that can be shot
    elif projectile_list[index].launched: # cannot be shot
        return find_leading_projectile(projectile_list,index-1)
    else:
        print('ERROR-CHOOSING PROJECTILE')

def clone_sections(master_list): # Generate COPIES of sections so the original is not overwritten+++
    copy_list = [] # new list
    for template in master_list: # @ width/height
        # COPY ALL aspects of the section - COPY ALL objects within that section, including platforms,hazards,and orbs
        # STATIONARY PLATFORMS
        s_plat_list = []
        for s in template.stationary_platforms:
            x = s.x; y = s.y
            pos = (x,y)
            width = s.width; height = s.height
            is_passable = s.passable
            is_spawnable = s.spawnable
            is_dark = s.dark
            is_slippery = s.slippery
            new_image = s.image # for overriding images
            new_plat = Platform(pos,w=width,h=height,passable=is_passable,spawnable=is_spawnable,dark=is_dark,slippery=is_slippery) # create a NEW platform
            new_plat.image = new_image
            new_plat.choose_image() # set graphics
            s_plat_list.append(new_plat) # add to a set

        # MOVING PLATFORMS
        m_plat_list = []
        for m in template.moving_platforms:
            new_path = m.path.copy()
            width = m.width; height = m.height
            is_closed = m.closed_path
            set_speed = m.speed
            new_plat = Moving_Platform(new_path,closed=is_closed,w=width,h=height)
            new_plat.speed = set_speed
            m_plat_list.append(new_plat) # add to a set

        # FALLING PLATFORMS
        f_plat_list = []
        for f in template.falling_platforms:
            x = f.x; y = f.y
            pos = (x,y)
            width = f.width; height = f.height
            new_plat = Falling_Platform(pos,w=width,h=height)
            f_plat_list.append(new_plat) # add to a set

        # HAZARDS - spikes/moving spikes
        hazard_list = []
        for h in template.hazards:
            moveable = False
            if hasattr(h,'path'): # Moving
                new_path = h.path.copy()
                is_closed = h.closed_path
                set_speed = h.speed
                moveable = True
            else:# Not Moving
                x = h.x; y = h.y
                pos = (x,y)
            width = h.width; height = h.height
            if moveable:
                new_hazard = Moving_Spikes(new_path,w=width,h=height,closed=is_closed)
                new_hazard.speed = set_speed
            else:
                new_hazard = Spikes(pos,w=width,h=height)
            hazard_list.append(new_hazard) # add to a set

        # ORBS
        orb_list = []
        for o in template.orbs:
            x = o.x; y = o.y
            pos = (x,y)
            width = o.width; height = o.height
            new_orb = Light_Orb(pos,w=width,h=height)
            orb_list.append(new_orb)

        # BOOLEANS
        has_ground = template.ground
        has_ceiling = template.ceiling

        # now create a NEW COPY of a section
        new_section = Section(s_platforms=s_plat_list,f_platforms=f_plat_list,m_platforms=m_plat_list,hazards=hazard_list,orbs=orb_list,ground=has_ground,ceiling=has_ceiling)
        # add that copy to a new collection
        copy_list.append(new_section)
    return copy_list

def generate_map(easy_sections,medium_sections,hard_sections,very_hard_sections): # pass - None - if you dont want any of a specific section
    arrangement = []
    quantity = 0 # number of sections to be pulled from a specific pool

    if easy_sections:
        quantity = easy_sections[1] # update quantity
        if quantity == -1:
            quantity = len(easy_sections[0])
        easy_set = random.sample(easy_sections[0], quantity) # arrange EASY sections
        easy_clones = clone_sections(easy_set) # clones of original section designs - can be manipulated now
        arrangement.extend(easy_clones) # now add the clones      
    if medium_sections:
        quantity = medium_sections[1]
        if quantity == -1:
            quantity = len(medium_sections[0])
        medium_set = random.sample(medium_sections[0], quantity) # arrange MEDIUM sections
        medium_clones = clone_sections(medium_set) # clones of original section designs - can be manipulated now
        arrangement.extend(medium_clones) # now add the clones
    if hard_sections:
        quantity = hard_sections[1]
        if quantity == -1:
            quantity = len(hard_sections[0])
        hard_set = random.sample(hard_sections[0], quantity) # arrange HARD sections
        hard_clones = clone_sections(hard_set) # clones of original section designs - can be manipulated now
        arrangement.extend(hard_clones) # now add the clones
    if very_hard_sections:
        quantity = very_hard_sections[1]
        if quantity == -1:
            quantity = len(very_hard_sections[0])
        very_hard_set = random.sample(very_hard_sections[0], quantity) # arrange VERY HARD sections
        very_hard_clones = clone_sections(very_hard_set) # clones of original section designs - can be manipulated now
        arrangement.extend(very_hard_clones) # now add the clones

    return arrangement # send back the complete arrangement of sections

def position_sections(sections_list,leading_pos=0):
    # take a list of sections (in an order) and move them, along with all their contents,
    #  so that the first section in the list fits the screen and the rest are placed one-by-one to the right of the first section
    #  All sections will form one seamless map for the player to progress through
    width = display_width
    for index in range(len(sections_list)):
        current_section = sections_list[index]
        x_change = index * width + (leading_pos*display_width) # 0, 800, 1600, ...

        current_section.x = x_change # move the frame of the section
        current_section.starting_x = x_change # save the starting position

        # x_change = the amount the frame of the section was shifted over
        # current_pos + x_change = correct_position
        # move all contents (including ground/ceiling) +
        for current_object in current_section.all_entities:
            current_object.x += x_change
            current_object.hitbox.x += x_change
        if current_section.ground:
            current_section.ground_platform.x += x_change
            current_section.ground_platform.hitbox.x += x_change
        if current_section.ceiling:
            current_section.ceiling_platform.x += x_change
            current_section.ceiling_platform.hitbox.x += x_change

def update_spawn_rates(difficulty): # This function changes global data, based on difficulty
    global abyss_spawn_rate
    global tormentor_spawn_rate
    global purple_ghost_spawn_rate
    global pink_ghost_spawn_rate
    if difficulty == 0: # defaults
        abyss_spawn_rate = 30
        tormentor_spawn_rate = 0 # FIX THIS
        purple_ghost_spawn_rate = 100
        pink_ghost_spawn_rate = 0
    else: # constant increase (to a max) !!
        if abyss_spawn_rate < 70:
            abyss_spawn_rate += 5
        if tormentor_spawn_rate < 45:
            tormentor_spawn_rate += 5
        if purple_ghost_spawn_rate < 35:
            purple_ghost_spawn_rate += 3
        if pink_ghost_spawn_rate < 35:
            pink_ghost_spawn_rate == 5

def count_enemies(enemy_list): # counts enemies on screen
    abyss_total = 0
    tormentor_total = 0
    purple_ghost_total = 0  
    pink_ghost_total = 0
    others = 0 # unaccounted for
    for enemy in enemy_list:
        if enemy.name == 'abyss':
            abyss_total += 1
        elif enemy.name == 'tormentor':
            tormentor_total += 1
        elif enemy.name == 'purple ghost':
            purple_ghost_total += 1
        elif enemy.name == 'pink ghost':
            pink_ghost_total += 1
        else:
            others += 1
    # Organize this info
    enemy_totals = {'abyss': abyss_total, 'tormentor': tormentor_total, 'purple ghost': purple_ghost_total, 'pink ghost': pink_ghost_total,\
        'others': others, 'total': len(enemy_list)}
    return enemy_totals

def spawn_platform_enemies(enemy_list,platform_list,difficulty): # enemies that need to be on a platform - occurs when a new section is entered
    enemy_tally = count_enemies(enemy_list) # totals of each type of enemy
    max_abyss = 1 # total allowed on screen
    if difficulty >= 4:
        max_abyss = 3
    elif difficulty >= 1:
        max_abyss = 2
    free_platforms = [] # open for enemies to spawn

    for p in platform_list:
        if p.spawnable:
            free_platforms.append(p)

    for _ in range(max_abyss): # potential for all to spawn this instance, since platform enemies have only 1 chance to spawn
        if len(free_platforms) > 0 and enemy_tally['abyss'] < max_abyss: # room to spawn
            spawn_chance = random.randint(1,100)
            if spawn_chance <= abyss_spawn_rate:
                new_enemy = Abyss() # no attributes
                plat = new_enemy.spawn(free_platforms)
                enemy_list.append(new_enemy)
                free_platforms.remove(plat) # platform is no longer free

def spawn_ghosts(enemy_list,difficulty): # enemies that can enter/leave the screen freely - occurs every 4! seconds
    enemy_tally = count_enemies(enemy_list) # totals of each type of enemy
    max_tormentor = 2 #! max possible on-screen
    max_purple = 1
    max_pink = 2
    if difficulty >= 4:
        max_total = 5
        max_pink = 4
    elif difficulty >= 3:
        max_total = 4
        max_tormentor = 2
    elif difficulty >= 2:
        max_total = 3
    elif difficulty <= 1:
        max_total = 2
    else:
        print('ERROR-DIFFICULTY')

    if enemy_tally['total'] <= max_total: # room on screen for more
        if enemy_tally['tormentor'] < max_tormentor: # MAX of 2 on screen
            spawn_chance = random.randint(1,100)
            if spawn_chance <= tormentor_spawn_rate:
                new_tormentor = Tormentor()
                # - ADD ATTRIBUTES -
                speed_increase = difficulty * 0.5 # half a pixel / difficulty
                if speed_increase >= 5: # cap at 5
                    speed_increase = 5
                new_tormentor.float_speed += speed_increase
                # Spawn-in
                if enemy_tally['tormentor'] == 1: # second one will likely come from the left
                    new_tormentor.spawn(spawn_left_chance=70)
                else:
                    new_tormentor.spawn() # must select a starting position
                enemy_list.append(new_tormentor)
        if enemy_tally['purple ghost'] < max_purple: # MAX 1 on screen
            spawn_chance = random.randint(1,100)
            if spawn_chance <= purple_ghost_spawn_rate:
                new_ghost = Purple_Ghost()
                # - ADD ATTRIBUTES -
                if difficulty >= 5:
                    new_ghost.despawn = False
                elif difficulty >= 4:
                    new_ghost.despawn_time = 15.0
                elif difficulty >= 3:
                    new_ghost.depsawn_time = 9.0
                elif difficulty >= 2:
                    new_ghost.depsawn_time = 6.0
                new_ghost.spawn()
                enemy_list.append(new_ghost)
        if enemy_tally['pink ghost'] < max_pink: # Max 2 on screen
            spawn_chance = random.randint(1,100)
            if spawn_chance <= pink_ghost_spawn_rate:
                new_ghost = Pink_Ghost()
                # - ADD ATTRIBUTES -
                if difficulty >= 5:
                    new_ghost.despawn_time = 16.0
                elif difficulty >= 3:
                    new_ghost.despawn_time = 12.0
                new_ghost.spawn()
                enemy_list.append(new_ghost)


def draw_status_bar(score,light_filled):
    # this is the bar at the top of the game screen, where the LIGHTBAR and SCORE will go
    bar = status_bar.copy()
    bar_width = bar.get_width()
    bar_height = bar.get_height()

    margin = 20 # pixels from edge of bar

    # Light Bar
    light_height = lightbar.get_height()
    light_total_width = lightbar.get_width()
    light_width = int(light_filled/100 * light_total_width)
    light_rect = (0,0,light_height,light_width) # portion of light that will be copied
    light_pos = (127,9) # static

    # Add the light to the bar
    bar.blit(lightbar,light_pos,(0,0,light_width,light_height))

    # Score Bar
    score_str = str(score)
    digits = len(score_str) # how many numbers make up the score (cap at 6 digits)
    if digits > 6:
        digits = 6

    # Determine which number sprites to copy
    score_list = [] # list of digit sprites that make up the score
    new_digit = number_0 # the current digit in the set
    for n in score_str:
        # Each digit occupies a unique section of the spritesheet - there is no pattern
        if n == '0':
            new_digit = number_0
        elif n == '1':
            new_digit = number_1
        elif n == '2':
            new_digit = number_2
        elif n == '3':
            new_digit = number_3
        elif n == '4':
            new_digit = number_4
        elif n == '5':
            new_digit = number_5
        elif n == '6':
            new_digit = number_6
        elif n == '7':
            new_digit = number_7
        elif n == '8':
            new_digit = number_8
        elif n == '9':
            new_digit = number_9
        else:
            print('ERROR-UNRECOGNIZED-DIGIT')
            print(n)
        # add the new surface to the list
        score_list.append(new_digit)

    # Add comma, if in thousands
    if digits >= 4:
        location = digits - 3
        score_list.insert(location,comma)

    # Add the score to the bar
    total_digit_width = 0
    for x in reversed(score_list): # x will represent the current digit surface
        digit_width = x.get_width()
        digit_height = x.get_height()       

        digit_pos = (bar_width - margin - total_digit_width - digit_width, bar_height//2 - digit_height//2) # position of next last digit
        total_digit_width += digit_width # update distance taken by digits
        # Adds HERE
        bar.blit(x,digit_pos)


    score_title_space = 9 # pixels away from actual score
    score_title_width = score_title.get_width()
    score_title_height = score_title.get_height()
    x = bar_width - score_title_width - total_digit_width - margin - score_title_space
    y = bar_height//2 - score_title_height//2
    score_title_pos = (x,y)
    # Adds HERE
    bar.blit(score_title,score_title_pos)

    # Now add the Status Bar to the actual screen
    gameDisplay.blit(bar,(0,0))


def game_over(score):
    local_fps = 20
    lose_screen = gameDisplay.copy() # copy the current state of the display
    black_screen = pygame.Surface((display_width,display_height))
    black_screen.convert(black_screen)
    black_screen.fill(black)

    fade_counter = 0
    fade_time = 1.0 # seconds
    final_transparency = 225 # how dark the screen will eventually get
    value = final_transparency / (fade_time*local_fps) # the amount the screen should get darker each frame

    menu_activated = False # when the menu be seen

    title = game_over_title
    title_width = title.get_width()
    title_height = title.get_height()
    x = center_screen[0] - title_width*0.5 # center screen
    y = display_height*0.15 - title_height*0.15 # 15% down
    title_pos = (x,y)

    score_text = big_score_title.convert()
    score_text_width = score_text.get_width()
    score_text_height = score_text.get_height()

    # Buttons
    spacing = 7
    restart = Button((0,0),active_retry,inactive_retry) # BUTTON
    restart.name = 'start'
    restart.active = True # first button starts active
    x = center_screen[0] - restart.width*0.5
    y = display_height*0.6833 - restart.height*0.5 #! leading height (*0.7033)
    restart.x = x
    restart.y = y
    y += restart.height + spacing # prepare for next button^

    main_menu = Button((0,0),active_main_menu,inactive_main_menu) # BUTTON
    main_menu.name = 'main menu'
    x = center_screen[0] - main_menu.width*0.5
    main_menu.x = x
    main_menu.y = y
    y += main_menu.height + spacing #^

    spacing = 4

    quit_btn = Button((0,0),active_quit,inactive_quit) # BUTTON
    quit_btn.name = 'quit'
    x = center_screen[0] - quit_btn.width*0.5
    quit_btn.x = x
    quit_btn.y = y

    button_pressed = [False,False]
    button_list = [restart,main_menu,quit_btn] # list of buttons

    # Final Score
    score_str = str(score)
    digits = len(score_str) # how many numbers make up the score (cap at 6 digits)
    if digits > 6:
        digits = 6

    # Determine which number sprites to copy
    score_list = [] # list of digit sprites that make up the score
    new_digit = big_number_0
    for n in score_str:
        # Each digit occupies a unique section of the spritesheet - there is no pattern
        if n == '0':
            new_digit = big_number_0
        elif n == '1':
            new_digit = big_number_1
        elif n == '2':
            new_digit = big_number_2
        elif n == '3':
            new_digit = big_number_3
        elif n == '4':
            new_digit = big_number_4
        elif n == '5':
            new_digit = big_number_5
        elif n == '6':
            new_digit = big_number_6
        elif n == '7':
            new_digit = big_number_7
        elif n == '8':
            new_digit = big_number_8
        elif n == '9':
            new_digit = big_number_9
        else:
            print('ERROR-UNRECOGNIZED-DIGIT')
        # add the new surface to the list
        score_list.append(new_digit)

    # Add comma, if in thousands
    if digits >= 4:
        location = digits - 3
        score_list.insert(location,big_comma)

    score_surface = pygame.Surface((300,44)) # crop later (excess size

    # Add the score together
    total_digit_width = 0
    for new_number in score_list: # the current digit surface - forwards order
        digit_width = new_number.get_width()
        digit_height = new_number.get_height()       

        total_digit_width += digit_width # total distance taken by digits
        digit_pos = (total_digit_width-digit_width, 0) # position of next last digit
        # Adds HERE
        score_surface.blit(new_number,digit_pos)

    score_surface = score_surface.subsurface((0,0,total_digit_width,44)) # crop surface

    # Combine the score text and numbers
    spacing = 42
    combined_width = score_text_width + total_digit_width + spacing
    greater_height = max(score_text_height,44)

    combined_score = pygame.Surface((combined_width,greater_height),pygame.SRCALPHA,32)
    y = (greater_height - score_text_height) // 2 # cant be bigger than surface
    combined_score.blit(score_text,(0,y)) # part 1
    x = spacing + score_text_width
    y = (greater_height - 44) // 2
    combined_score.blit(score_surface,(x,y)) # part 2
    # position of score
    x = center_screen[0] - combined_score.get_width()*0.5 # centered
    y = display_height*0.45 - combined_score.get_height()*0.5 #! 45% down
    score_pos = (x,y)

    active_index = 0 # which button is current selected, -1 is nothing selected
    mouse_moved = False # did the mouse move THIS FRAME
    cursor_pos = (0,0)

    running = True

    while running:

        # LIST OF EVENTS TRIGGERED:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION: # cursor moved
                mouse_moved = True
                cursor_pos = pygame.mouse.get_pos() # update the cursor's location
            else:
                mouse_moved = False
            if event.type == pygame.QUIT: # X-button
                quit_game()

        # DRAW
        gameDisplay.blit(lose_screen,(0,0)) # initial lose screen
        # SCREEN FADE
        alpha = value * fade_counter
        if fade_counter <= fade_time * local_fps:
            black_screen.set_alpha(alpha) # set level of darkness
            fade_counter += 1
        else:
            menu_activated = True

        gameDisplay.blit(black_screen,(0,0)) # darken the screen

        # GAMEOVER MENU
        if menu_activated:
            keys_pressed = pygame.key.get_pressed() # boolean list of all keys currently pressed
            button_select = False
            # KEYDOWNS
            if not mouse_moved:
                # nothing selected right now
                if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and not button_pressed[0]: # move up
                    button_select = True
                    button_pressed[0] = True
                    if active_index == -1:
                        active_index = 0 # start from the first option
                    else: # UP
                        if active_index == 0: # reset loop
                            active_index = len(button_list) -1
                        else:
                            active_index -= 1
                elif not keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_w]:
                    button_pressed[0] = False # unpressed button

                if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and not button_pressed[1]: # move down
                    button_select = True
                    button_pressed[1] = True
                    if active_index == -1:
                        active_index = 0 # start from the first option
                    else: # DOWN
                        if active_index == len(button_list)-1: # reset loop
                            active_index = 0
                        else:
                            active_index += 1
                elif not keys_pressed[pygame.K_DOWN] and not keys_pressed[pygame.K_s]:
                    button_pressed[1] = False

                # Unactivate all buttons
                if button_select:
                    for new_button in button_list:
                        new_button.active = False
                        # Find the active button, and activate it!
                        if active_index != -1: # something is activated
                            button_list[active_index].active = True

            # ACTIVATE BY CURSOR
            elif mouse_moved:
                active_index = -1 # temporarily disable the index
                for new_button in button_list:
                    if new_button.contains(cursor_pos):
                        new_button.active = True
                    else:
                        new_button.active = False


            # CLICK BUTTON - enter, space, or leftclick triggers this event
            if keys_pressed[pygame.K_RETURN] or keys_pressed[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                for new_button in button_list:
                    if new_button.active: # if the button is highlighted, click it
                        if new_button.name == 'main menu': # main button specifically
                            return # simply exit the loop
                        else:
                            new_button.click()
                            return # this menu has served its purpose

            # DRAW
            gameDisplay.blit(title,(title_pos))
            gameDisplay.blit(combined_score,(score_pos))
            for new_button in button_list:
                new_button.draw()

        pygame.display.update()
        clock.tick(local_fps)

def quit_game():
    # quit pygame, then quit the program
    pygame.quit()
    quit()

def start_game(): # Main Gameloop
    # game modes
    debug_mode = False # display hitboxes and debugging stats
    switch_1 = False
    switch_2 = False

    dark_cloud = Darkness_Overlay() # the shroud of darkness overlay
    character_width = 38
    character_height = 58
    candleboy = Player(center_screen,character_width,character_height) # reference to playable character

    enemies = [] # list of current screen enemies
    update_spawn_rates(candleboy.difficulty) # reset enemy spawn rates
    shadow_orbs = []
    spawn_time = 4.0 # seconds until enemies have a chance to spawn, loops
    spawn_counter = 0

    # MAP - arrangement of sections for THIS run
    # - 6 worlds
    # RULES
    # - 6th! world always last
    # - other worlds in random order
    # - each world has 3 variations (subworlds)
    # - each subworld has a pool for EASY, MEDIUM and HARD levels
    # CONSTRUCTION
    # - each world will consist of 1 easy/spawn level, 2-3 medium levels, 3-2 hard levels, and 1 boss stage
    # - after each world there will be 3-5 basic levels, difficulty based on worlds cleared

    first_section = [random.choice(spawn_sections)] # the section the player starts in
    first_section = clone_sections(first_section) # always clone any sections added to the game +
    map = first_section; del first_section # s.m
    map.extend(generate_map((easy_sections,4),(medium_sections,-1),None,(very_hard_sections,-1)))
    position_sections(map) # always call this after generating a map - moves them into a linear arrangement (left to right)

    current_sections = [] # the two sections that are on screen at any given time -@
    current_sections = map[:2] # take the 2 leftmost sections from the arrangement

    current_background = background_set[0] # backdrop image for the current world
    screen_background = Background(2,bg=current_background,w=1600) # the controllable background

    running = True

    while running:

        # LIST OF EVENTS TRIGGERED:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # X-button
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print(True)
                    if event.mod == pygame.KMOD_LCTRL: #DP! - shortcut for restarting
                        print('starting new run...')
                        start_game()
                        return

        # GAME LOGIC - game mechanics are stopped if the player is dead
        if candleboy.alive:

            # GENERATE MORE SECTIONS:
            if len(map) <= 3: # 1 for safety
                new_sections = generate_map(None,(medium_sections,-1),(hard_sections,-1),(very_hard_sections,-1)) # right now, only hard sections added
                position_sections(new_sections,leading_pos=len(map))
                map.extend(new_sections)

            # UPDATE CURRENT SECTIONS
            for sec in map:    
                #sec.scroll() # move all sections
                sec.check_active() # activate sections on-screen
                if sec.discard: # delete cleared sections
                    map.remove(sec)
                    candleboy.sections_cleared += 1
                    update_spawn_rates(candleboy.difficulty)
            previous_sections = current_sections.copy() # 1 frame behind
            current_sections = map[:2] # take the 2 leftmost sections from the arrangement

            # --- Define Screen Elements ---
            # COPY lists to avoid reference - the copy is the temporary variable
            moving_platforms = current_sections[0].moving_platforms.copy() # make a copy
            falling_platforms = current_sections[0].falling_platforms.copy() # copy
            platforms = current_sections[0].all_platforms.copy() # copy, list with all the screen's platforms (any type)
            hazards = current_sections[0].hazards.copy() # copy
            orbs = current_sections[0].orbs.copy() # copy, list of all the screen's orbs

            # only add elements from the second section if it's active, also on-screen
            if current_sections[1].active:
                moving_platforms.extend(current_sections[1].moving_platforms)
                falling_platforms.extend(current_sections[1].falling_platforms)
                platforms.extend(current_sections[1].all_platforms)            
                hazards.extend(current_sections[1].hazards)
                orbs.extend(current_sections[1].orbs)

            # collect elements
            obstacles = hazards # list with all the screen's obstacles (hazards/enemies hurt you and paltforms squish you)
            obstacles.extend(platforms)
            obstacles.extend(enemies)
            # not bound by sections
            projectiles = candleboy.light_beams # list of screen's projectiles
            projectiles.extend(shadow_orbs)
            player_targets = obstacles.copy()
            player_targets.extend(enemies)
            enemy_targets = [candleboy] # things enemy projectiles can hit
            for o in orbs:
                enemy_targets.append(o)


            # PLAYER BOUNDS
            candleboy_rect = (candleboy.x,candleboy.y,candleboy.width,candleboy.height)
            candleboy_center = (candleboy.x+candleboy.width//2,candleboy.y+candleboy.height//2)

            # REMOVE ENEMIES
            for e in enemies:
                if e.alive == False:
                    enemies.remove(e)

            # SPAWN ENEMIES
            spawn_counter += 1 # DISABLED ***
            if previous_sections != current_sections: # a new section must have made it on screen
                spawn_platform_enemies(enemies,current_sections[1].all_platforms,candleboy.difficulty) # PLATFORM ENEMIES
            if spawn_counter >= spawn_time * fps: # its spawn time
                spawn_counter = 0 # reset counter
                spawn_ghosts(enemies,candleboy.difficulty) # GHOSTS
                if candleboy.difficulty >= 1: #! SHADOW ORBS can now spawn
                    for _ in range(2):
                        if len(shadow_orbs) < 2: # max. of 2
                            shadow_chance = random.randint(1,100)
                            if shadow_chance <= 20:
                                new_shadow_orb = Shadow_Ball()
                                new_shadow_orb.spawn(candleboy_center) # set starting position
                                shadow_orbs.append(new_shadow_orb)

            # KEYDOWNS:
            # --- moving ---
            controlled_motion = True
            keys_pressed = pygame.key.get_pressed() # list of keys pressed
            if keys_pressed[pygame.K_LEFT]: # left arrow
                candleboy.dir = -1
            if keys_pressed[pygame.K_RIGHT]: # right arrow
                candleboy.dir = 1
            # neither left or right pressed
            if (not keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_a]) and (not keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_d]):
                candleboy.dir = 0
                controlled_motion = False

            # --- jumping ---
            if keys_pressed[pygame.K_z]: # Z-Key
                if candleboy.can_jump:
                    if not candleboy.falling and not candleboy.jumping and not candleboy.wall_jumping: # NORMAL JUMP
                        candleboy.jumping = True # jump
                    elif candleboy.has_wall != 0: # WALL JUMP
                        candleboy.wall_jumping = True # jump
                        candleboy.fall_speed = 0 # WALL JUMP ONLY (make sure player experiences no gravity right before they jump again)
                        candleboy.wall_slide = False
                        candleboy.x += 1 * candleboy.run_speed * candleboy.has_wall # pushback !!
                        candleboy.hitbox.x += 1 * candleboy.run_speed * candleboy.has_wall

                if candleboy.jumping or candleboy.wall_jumping: # IS jumping, (if)
                    candleboy.jump_time += 1/fps # increment time jumping

                candleboy.can_jump = False # release before jumping again

            else: # not pressing Z
                if (candleboy.jumping or candleboy.wall_jumping) and candleboy.vel[1] < 0: # Jumping UP$ 
                    if not candleboy.jump_release: # SET gravity, once per release
                        # recalculate a new gravity for the path
                        candleboy.fast_gravity = candleboy.calc_gravity()
                        candleboy.jump_release = True # JUMP RELEASE
                else: # on the way down (up path complete), reset jump stats
                    candleboy.jump_time = 0
                    candleboy.jump_release = False

                candleboy.can_jump = True # let go of Z, can jump again


            # --- shooting---
            if keys_pressed[pygame.K_x]: # spacebar
                if candleboy.light_filled >= candleboy.beam_cost and candleboy.light_beams: # must have available light to shoot, ammo must have been created +
                    if candleboy.reload_counter <= 0:
                        max_index = candleboy.charges - 1
                        beam_index = find_leading_projectile(candleboy.light_beams,max_index)
                        # print(beam_index) # DP!
                        if beam_index != None: # if a beam exists and can be shot
                            candleboy.light_beams[beam_index].launched = True # shoot that beam (sends into motion)
                            if candleboy.hold_shot and candleboy.consecutive_shots < candleboy.max_burst:
                                candleboy.consecutive_shots += 1 # this starts increasing when the second beam is shot
                            else:
                                candleboy.consecutive_shots = 1 # reset if already reached max or shooting individually
                            # set reload speed
                            if candleboy.consecutive_shots >= candleboy.max_burst: # 2
                                candleboy.reload_time = candleboy.reload_2
                            else:
                                candleboy.reload_time = candleboy.reload_1 # (default)
                            candleboy.reload_counter = candleboy.reload_time * fps # reset counter - integer
                            candleboy.shooting = True # for animation!
                            candleboy.light_filled -= candleboy.beam_cost # lose light +


            # --- Game Mechanics ---
            if hasattr(candleboy,'temporary_radius'): # game must have just beugn, quickly grow radius
                glow_fields = [(candleboy.temporary_radius,candleboy_rect)]
                candleboy.temporary_radius += int(candleboy.radius_growth) # grow radius
                if abs(candleboy.temporary_radius - candleboy.visible_radius) < candleboy.radius_growth: # the full radius has been set
                    del candleboy.temporary_radius
                    del candleboy.radius_growth
            else:
                glow_fields = [(candleboy.visible_radius,candleboy_rect)] # areas that emit light - TUPLE: field radius, rectangular bounds - size and pos
            for p in candleboy.light_beams:
                if p.launched and p.glow:
                    glow_fields.append((p.glow_radius,(p.x,p.y,p.width,p.height)))
            for o in orbs:
                if o.x - o.glow_radius < display_width:
                    glow_fields.append((o.glow_radius,(o.x,o.y,o.width,o.height)))
            dark_cloud.update_layer(glow_fields)
            #Scroll Specific
            screen_background.scroll()
            # - Sections have scrolled above!
            #move_screen([candleboy]) # @
            #move_screen(enemies) 
               
            # Light Specific
            candleboy.diminish_light() # lose some light/second
            candleboy.update_vision() # set the field of view
            # Platform Specific
            for mp in moving_platforms:
                mp.update_vel()
                mp.move()
            for fp in falling_platforms:
                fp.fall()
            for sec in current_sections: #*
                for fp in sec.falling_platforms:
                    if fp.terminate:
                        sec.falling_platforms.remove(fp)
            # Hazard Specific
            for h in hazards:
                if hasattr(h,'path'):
                    h.update_vel()
                    h.move()
            # Player Specific
            candleboy.update_time()
            candleboy.update_direction() # set orientation [x-axis]
            candleboy.update_ammo()
            candleboy.reload()
            candleboy.enforce_gravity() # determines fall speed
            candleboy.adjust_pos(platforms)
            candleboy.update_vel()
            candleboy.detect_screen()
            candleboy.detect_surfaces(platforms) # handles surface contact (things you can walk on or bump into)
            candleboy.move()
            candleboy.detect_collision(obstacles) # handles intersection (things that kill you when it touches you)
            candleboy.detect_orbs(orbs)
            candleboy.choose_image(controlled_motion) # select animation
            # Enemy Specific
            for e in enemies:
                if e.name == 'abyss':
                    e.move()
                    e.choose_image()
                    e.check_life()
                elif e.name == 'tormentor':
                    e.update_vel()
                    e.move()
                    e.choose_image()
                    e.check_life()
                elif 'ghost' in e.name:
                    e.update_vel(candleboy_center)
                    e.move()
                    e.cool_down() # for invincibility
                    alternate_draw = False
                    if hasattr(e,'transformed'):
                        if e.transformed:
                            alternate_draw = True
                    if alternate_draw:
                        e.choose_image_transformed()
                    else:
                        e.choose_image()
                    e.check_life() # damage

            # Projectile Specific
            for bullet in projectiles:
                bullet.update_position()
                bullet.update_vel()
                bullet.move()
                bullet.detect_boundaries() # checks off-screen
            for beam in candleboy.light_beams:
                beam.detect_targets(player_targets) # checks for collision (enemies or blocks)
            for sh in shadow_orbs:
                sh.detect_targets(enemy_targets) # candleboy
                if sh.depleted:
                    shadow_orbs.remove(sh) # terminate the orb
            # Orb Specific
            for sec in current_sections:
                for o in sec.orbs:
                    o.choose_image() # animate
                    if o.has_light == False:
                        sec.orbs.remove(o) # Remove Orbs

        # Game Logic - after death
        else:
            candleboy.choose_image(False) # death animation only

        # --- Graphics ---
        screen_background.draw() # pastes background
        for sec in current_sections:
            #for q in sec.all_platforms:
            #    q.hitbox.draw() # DP!! - see platform hitboxes
            sec.draw_platforms()
        for sec in current_sections:
            sec.draw_hazards()
        for sec in current_sections:
           sec.draw_orbs()
        for b in candleboy.light_beams:
            b.draw()
        for e in enemies:
            e.draw()
            e.hitbox.draw() # DP! - see enemy hitboxes
        candleboy.hitbox.draw() # DP! - see player hitbox
        candleboy.draw()
        for sh in shadow_orbs:
            sh.draw()
        # Overlay
        #dark_cloud.draw() # finally draw the dark overlay layer **
        # Status bar
        draw_status_bar(candleboy.calculate_score(),candleboy.light_filled) # over EVERYTHING

        pygame.display.update() # UPDATE the DISPLAY (everthing is drawn here)
        clock.tick(fps) # how often this loop will repreat

        # --- Check Alive ---
        candleboy.check_death()
        if candleboy.dead: 
            game_over(candleboy.calculate_score())
            return


# --- End of Code ---
#run_menu() # nothing else should be here
start_game()