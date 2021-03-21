import pygame
import random

pygame.init() #Start pygame

###Global vars
#Screen and colour settings
WIDTH, HEIGHT = 500, 800
RED = (200, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BACKROUND = (20, 20, 40)
TIME_FONT = pygame.font.SysFont("Arial", 40, True, False)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 60, True, False)

#Game settings
TICKS_SEC = 60

#Player settings
X_FORCE = 120
X_SLOW = 0.13
BOOST = 50
BOOST_LIMIT = 9
MAX_X_SPEED = 300
PLAYER_SIZE = 30
Lives = 5
Hit_shade = 0
HIT_EFFECT = 80
HIT_SHADE_DECREASE = 50
DEATH_ANIMATION = 3 

#Meteor settings
SPAWN_LOCATION = -30
SPAWN_CYCLE = int(0.1 * TICKS_SEC)
SPAWN_CHANCE = 10
M_X_SPEED = 30 #random value between X_SPEED and - X_SPEED
BASE_Y_SPEED = 210
M_MIN_SIZE = 15
M_MAX_SIZE = 30

Player_list = list()
Meteor_list = list()

#functions
def spawn_meteor():
    if Time % SPAWN_CYCLE == 0:
        extra = int((Time / TICKS_SEC)**(1/2))
        if extra >= SPAWN_CHANCE:
            extra = SPAWN_CHANCE - 1
        if random.randint(0, SPAWN_CHANCE - extra) == 0:
            Meteor_list.append(Meteor())
    
    for i in range(len(Meteor_list) -1, -1, -1):
        if Meteor_list[i].y > HEIGHT - SPAWN_LOCATION:
            del Meteor_list[i]

#classes
class Player():
    x = WIDTH // 2
    y = HEIGHT - 30
    x_speed = 0
    size = PLAYER_SIZE
    score = 0

    def __init__(self, colour, left, right):
        self.colour = colour
        self.left = left
        self.right = right

    def move(self):
        if keys[self.left]:
            self.x_speed = self.x_speed - (X_FORCE / TICKS_SEC)
            if self.x_speed > -BOOST_LIMIT:
                self.x_speed = self.x_speed - (BOOST / TICKS_SEC) 
        if keys[self.right]:
            self.x_speed = self.x_speed + (X_FORCE / TICKS_SEC)
            if self.x_speed < BOOST_LIMIT:
                self.x_speed = self.x_speed + (BOOST / TICKS_SEC)

        self.x_speed = self.x_speed - self.x_speed * X_SLOW
        
        if self.x < 20:
            self.x = 20
            self.x_speed = 0
        elif self.x > WIDTH - 20:
            self.x = WIDTH - 20
            self.x_speed = 0

        self.x = self.x + self. x_speed
            
    def draw(self):
        points = ((self.x, self.y - (self.size / 1.2)), (self.x - (self.size / 2), self.y + (self.size / 3)), (self.x, self.y), (self.x + (self.size / 2), self.y + (self.size / 3)))
        pygame.draw.polygon(screen, self.colour, points)
        
    def collision(self):
        slim = PLAYER_SIZE / 2 + 5 #makes the x len of the hitbox smaller
        for i in range(len(Meteor_list) -1, -1, -1):
            if Meteor_list[i].x > self.x:
                distance = (self.x - Meteor_list[i].x - slim)**2 + (self.y - Meteor_list[i].y)**2
            else:
                distance = (self.x - Meteor_list[i].x + slim)**2 + (self.y - Meteor_list[i].y)**2
            if (self.size + Meteor_list[i].size)**2 > distance:
                del Meteor_list[i]
                global Lives, Hit_shade
                Lives = Lives - 1
                Hit_shade = Hit_shade + HIT_EFFECT
                

class Meteor():
    def __init__(self):
        self.x = random.randint(10, WIDTH - 10)
        self.y = SPAWN_LOCATION
        self.x_speed = random.randint(-M_X_SPEED, M_X_SPEED)
        self.y_speed = BASE_Y_SPEED + (((Time / TICKS_SEC)**(4/5)) * 15)
        self.size = random.randint(M_MIN_SIZE, M_MAX_SIZE)
        shade = random.randint(-20, 25)
        self.colour = (GREY[0] + shade, GREY[1] + shade, GREY[2] + shade)

    def move(self):
        self.x = self.x + (self.x_speed / TICKS_SEC)
        self.y = self.y + (self.y_speed / TICKS_SEC)

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size, 0)


################################################################################

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKROUND)

Player_list.append(Player(RED, pygame.K_a, pygame.K_d))

Time = 0
#Main game loop
while(Lives > 0):
    clock.tick(TICKS_SEC)
    pygame.event.pump()
    keys = pygame.key.get_pressed()

    if Hit_shade > 0:
        screen.fill((int(BACKROUND[0] + Hit_shade), int(BACKROUND[1] + Hit_shade), int(BACKROUND[2] + Hit_shade)))
        Hit_shade = Hit_shade - ((1 / TICKS_SEC) * HIT_SHADE_DECREASE)
    else:
        Hit_shade = 0
        screen.fill(BACKROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    spawn_meteor()
    
    for meteor in Meteor_list:
        meteor.move()
        meteor.draw()
        
    for player in Player_list:
        player.move()
        player.draw()
        player.collision()

    pygame.draw.rect(screen, RED, ((10, 10),(20*Lives, 10)))
    time_text = TIME_FONT.render(str(int(Time / TICKS_SEC)), 1, (250, 250, 250))
    screen.blit(time_text, (10, 20))
    
    Time = Time + 1
    pygame.display.flip()

#Death animation
animation_time = 1
for i in range(DEATH_ANIMATION * TICKS_SEC):
    clock.tick(TICKS_SEC)
    pygame.event.pump()

    screen.fill(BACKROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for meteor in Meteor_list:
        meteor.move()
        meteor.draw()
        
    for player in Player_list:
        pygame.draw.circle(screen, RED, (player.x, player.y), (animation_time / (DEATH_ANIMATION * TICKS_SEC)) * HEIGHT * 5, 30)
        pygame.draw.circle(screen, WHITE, (player.x, player.y), (animation_time / (DEATH_ANIMATION * TICKS_SEC)) * HEIGHT * 5 - 25, 50)

    time_text = TIME_FONT.render(str(int(Time / TICKS_SEC)), 1, (250, 250, 250))
    screen.blit(time_text, (10, 20))
    Game_over_text = GAME_OVER_FONT.render("GAME OVER", 1, (BACKROUND[0] + 200 * (animation_time / (DEATH_ANIMATION * TICKS_SEC)), BACKROUND[1], BACKROUND[2]))
    screen.blit(Game_over_text, (WIDTH/2 - 145, HEIGHT/2 - 200))

    
    animation_time = animation_time + 1
    pygame.display.flip()

#Wait unitil user closses game
while(True):
    clock.tick(TICKS_SEC)
    pygame.event.pump()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    

    
    
    
