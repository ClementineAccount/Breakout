# Example file showing a basic pygame "game loop"
import pygame
import pygame.font
import pygame.mixer
import math

import os

class breakbleBlock:    
    def __init__(self, inputRect : pygame.Rect, startValue = 2):
        self.rect = inputRect
        self.breakValue = startValue
    
    def draw(self):
        if self.breakValue == 1:
            pygame.draw.rect(screen, "red", self.rect)                    
        elif self.breakValue == 2:
            pygame.draw.rect(screen, "pink", self.rect)
        elif self.breakValue == 3:
            pygame.draw.rect(screen, "green", self.rect)
            
    def damage(self):
        if self.breakValue > 0:
            self.breakValue -= 1
            
    def check_damage_collide(self, rect):
        if self.breakValue > 0 and self.rect.colliderect(rect):
            self.damage()
            return True
        return False


class Ball:
    def __init__(self, inputRect: pygame.Rect, velocityX, velocityY):
        self.rect = inputRect
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.prevMove = 0
    
    def draw(self):
        pygame.draw.rect(screen, "yellow", self.rect)
        
    def draw_as_circle(self):
        pygame.draw.circle(screen, "yellow", self.rect.center, self.rect.width)
    
    def update(self, dt):
        
        #Possible To Do: Use 'sub-movement' concept so that I can tie things to dt properly
        
        #Have to convert to integer when calling move function but dt tends to be small value near -1 to 1
        velocityX_dt = self.velocityX * dt;
        velocityY_dt = self.velocityY * dt;
        
        if (velocityX_dt > 0):
            velocityX_dt = math.ceil(velocityX_dt)
        else:
            velocityX_dt = math.floor(velocityX_dt);
        
        if (velocityY_dt > 0 ):
            velocityY_dt = math.ceil(velocityY_dt)
        else:
            velocityY_dt = math.floor(velocityY_dt)
        
        #The Rect functions that change the position or size of a Rect return a new copy of the Rect with the affected changes
        #I think these bugs are caused by not using move. The rect's angles didn't get updated properly? I don't get it honestly
        #self.rect.centerx += dt * self.velocityX
        #self.rect.centery += dt * self.velocityY
        #print(math.ceil(self.velocityX * dt))
        self.rect.move_ip(velocityX_dt, velocityY_dt)
        
    #This definitely will be a bit off but whatever
    #def opposite_reaction(self):
    #    if abs(self.velocityX) > abs(self.velocityY):
    #        self.velocityX = self.velocityX * -1;
    #    else:
    #        self.velocityY = self.velocityY * -1;
    
    def opposite_reaction(self, fromWhere):
        
        if self.prevMove == fromWhere:
            return
        
        #To Do: Define it as constants somewhere
        # 1: From bottom to top
        # 2: From top to bottom
        # 3: From left to right
        # 4: From right to left
        if (fromWhere == 1 or fromWhere == 2):
            self.velocityY = self.velocityY * -1;
        if (fromWhere == 3 or fromWhere == 4):
            self.velocityX = self.velocityX * -1;
        if (fromWhere == 5):
            #self.velocityX = self.velocityX * -1;
            self.velocityY = self.velocityY * -1;
        self.prevMove = fromWhere


class Paddle:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
    
    def update_position(self, mouseX, mouseY):
        #Set to top left
        posX = mouseX - self.rect.width / 2
        posY = mouseY - self.rect.height / 2
        
        #Set the new position using update command
        self.rect.update(posX, posY, self.rect.width, self.rect.height)
    
    def draw(self):
        pygame.draw.rect(screen, "green", self.rect)
        

#To Do: Can name this as 'check vertical/horizontal'
def check_ball_collision(ball, otherRect, hitSound):
    
    #Early rejection if no collision
    if (not otherRect.colliderect(ball.rect)):
        return False
    
    #Also ignore inside edge cases (to avoid being trapped)
    #if (otherRect.contains(ball.rect)):
        #return False
    
    #Check if it is a vertical or horizontal collison
    #Vertical collision: Both tops are hit or both bottoms are hit
    #If it is not vertical, we can assume it is horizontal
    
    #To Do: Figure out what to return or if the collision response is to be done inside here too
    
    #Top left OR bottom right are always in the collision so that can be checked
    if (otherRect.collidepoint(ball.rect.topleft)):
        #Check if horizontal hit
        if (otherRect.collidepoint(ball.rect.topright)):
            print("Horizontal Hit from bottom to top")
            ball.opposite_reaction(1)
        elif (otherRect.collidepoint(ball.rect.bottomleft)):
            print("Vertical hit from the right to left")
            ball.opposite_reaction(4)
        else:
            print("Corner hit! Invert y-velocity")
            ball.opposite_reaction(5)
        hitSound.play()     
        return True
    elif (otherRect.collidepoint(ball.rect.bottomright)):
        if (otherRect.collidepoint(ball.rect.bottomleft)):
            print("Horizontal hit from top to bottom")
            ball.opposite_reaction(2)
        elif (otherRect.collidepoint(ball.rect.topright)):
            print("Vertical hit from left to right")
            ball.opposite_reaction(3)
        else:
            print("Corner hit! Invert y-velocity")
            ball.opposite_reaction(5)     
        hitSound.play()   
        return True
    return False


def check_ball_block_collision(block_list, ball, hitSound):
    for i in range(len(block_list)):
        if (block_list[i].breakValue > 0 and check_ball_collision(ball, block_list[i].rect, hitSound)):
            print("Hit!")
            block_list[i].damage()
            return
        
        #if (block_list[i].check_damage_collide(ball.rect)):
        #   ball.opposite_reaction()

            
    


# def check_list_collision(block_list, mouse):
#     for i in range(len(block_list)):
#         block_list[i].check_damage_collide(mouse.getPos().x, mouse.)

def draw_block_list(block_list, screen):
    for i in range(len(block_list)):
        breakbleBlock.draw(block_list[i])


# Setup some functions to help draw rectangles
def create_rect_row(startLeft, y, numRect, size = 20, buffer = 20 / 3):    
    #I need to learn how to set the type of a list and then append after or something?
    #in javascript i think this can just be a var and itd automagically push it in
    #square_list = [(pygame.Rect(0, 0, 10, 10))]
    #square_list.clear()
    square_list = []
    for i in range(numRect):
        square_list.append(pygame.Rect(startLeft + i * (size + buffer), y, size, size))
    return square_list

def draw_rect_row(square_list, color, screen):
    for i in range(len(square_list)):
        pygame.draw.rect(screen, color, square_list[i])
        
def create_breakable_blocks(startLeft, y, numRect, size = 20, buffer = 20 / 3):
    block_list = []
    rect_list = create_rect_row(startLeft, y, numRect, size, buffer)
    for i in range(len(rect_list)):
        block_list.append(breakbleBlock(rect_list[i]))
    return block_list



def check_ball_edge(ball, screen):
    if (ball.rect.centerx < 0 + 10):
        ball.opposite_reaction(4)
    if (ball.rect.centery > screen.get_height() - 10):
        #ball.opposite_reaction(2)
       return False
    if (ball.rect.centerx > screen.get_width() - 10):
        ball.opposite_reaction(3)
    if (ball.rect.centery < 0 + 10):
        ball.opposite_reaction(1)
    return True


# pygame setup
pygame.init()
pygame.mixer.init()
pygame.font.init()

width = 800
screen = pygame.display.set_mode((width, 600), vsync=False, flags=pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


hitSoundPath = os.path.join(data_dir, "hit.wav")
hitSound = pygame.mixer.Sound(hitSoundPath)


dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

pygame.display.set_caption("Hello World")

mouse = pygame.mouse

ballSizeX = 10
ballSizeY = 10

global playerBall
playerBall = Ball(pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 10, 10), 3, 250)


paddleWidth = 60
paddleHeight = 15

#Allows me to clamp it 
paddleY = screen.get_height() -  screen.get_height() / 6

global playerPaddle
playerPaddle = Paddle(paddleWidth, paddleHeight)

global block_list
block_list = create_breakable_blocks(40, 50, 11, 50, 50 /3 )


#print(square_list)

isGameSetup = False

wasRestartKeyDown = False

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 255))

font = pygame.font.Font(None, 32)
text = font.render("Press R to Restart", True, (10, 10, 10))
textpos = text.get_rect(centerx=background.get_width() / 2, y=background.get_height() - background.get_height() / 10)
background.blit(text, textpos)

while running:
    
    #Sets up the game stuff so that we have a way to restart
    if not isGameSetup:
        print("Set up the game!")
        isGameSetup = True
            #Delete the variables first as we are replacing them in the new restart scene
        del playerBall
        del playerPaddle
        del block_list
    
        playerBall = Ball(pygame.Rect(screen.get_width() / 2, screen.get_height() / 2, 10, 10), 3, 250)
        playerPaddle = Paddle(paddleWidth, paddleHeight)
        block_list = create_breakable_blocks(40, 50, 11, 50, 50 /3 )
    
    dt = clock.tick(60) / 1000
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            player_pos.x = mouse.get_pos()[0];
            player_pos.y = mouse.get_pos()[1];
            
    

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")

    keys = pygame.key.get_pressed()
    
    
    

    
    playerPaddle.update_position(player_pos.x, paddleY)
    

    #check_ball_edge(playerBall, screen)
    
    playerBall.update(dt)
    
    check_ball_collision(playerBall, playerPaddle.rect, hitSound)
    check_ball_block_collision(block_list, playerBall, hitSound)
    
    
    #Returns false if hit bottom so auto restarts
    isGameSetup = check_ball_edge(playerBall, screen)
    
    
    #Restart the game (put after so it overrides the boundry check)
    if keys[pygame.K_r] and not wasRestartKeyDown:
        isGameSetup = False
        wasRestartKeyDown = True
    elif not keys[pygame.K_r] and wasRestartKeyDown:
        wasRestartKeyDown = False
        
    screen.blit(background, (0, 0))
    
    playerBall.draw_as_circle()   
    draw_block_list(block_list, screen) 
    playerPaddle.draw()

    # flip() the display to put your work on screen
    # This of this as 'swap buffers' in GLFW
    
    pygame.display.flip()
    

    
    pygame.display.set_caption(str(clock.get_fps()))
    
    if keys[pygame.K_ESCAPE]:
        running = False
    
pygame.quit()