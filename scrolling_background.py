# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Start Screen
def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    return  # Start the game loop

        DISPLAYSURF.fill(WHITE)  # Fill the screen with white
        title_text = font.render("Like a Sapling!", True, GREEN)
        instructions_text = font_small.render("Click to Start", True, BLACK)

        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        title_y = SCREEN_HEIGHT // 5  # Top part of the screen
        DISPLAYSURF.blit(title_text, (title_x, title_y))

        instructions_x = (SCREEN_WIDTH - instructions_text.get_width()) // 2
        instructions_y = SCREEN_HEIGHT // 2  # Center of the screen
        DISPLAYSURF.blit(instructions_text, (instructions_x, instructions_y))


    pygame.display.update()  # Update the screen



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("water.png")
        self.image = pygame.transform.scale(self.original_image, (42, 70))
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40)
                                               , 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("tree.png")
        self.width = 42
        self.height = 70
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center=(160, 520))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        # self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        # self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def resize(self, scale_factor):
        """Increase player size by a scale factor."""
        self.width = int(self.width * scale_factor)
        self.height = int(self.height * scale_factor)
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=self.rect.center)


class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('AnimatedStreet.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 5

    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height

    def render(self):
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))


def GameLoop():
    global SCORE, SPEED

# Setting up Sprites
    P1 = Player()
    E1 = Enemy()

    back_ground = Background()

# Creating Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

# Adding a new User event
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    score = 0;
    font = pygame.font.SysFont(None, 36);

    def spawn_enemy():
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)

    def show_score():
        score_surface = font.render("Score: " + str(score), True, BLACK)
        DISPLAYSURF.blit(score_surface, (10, 10))

    # Game Loop
    while True:

    # Cycles through all occurring events
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.0
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        back_ground.update()
        back_ground.render()

        # DISPLAYSURF.blit(background, (0,0))
        scores = font_small.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()


        P1.update()

    # To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollideany(P1, enemies):

            #increase player score
            score+=10

            collided_enemy= pygame.sprite.spritecollideany(P1, enemies)
            if collided_enemy:
                collided_enemy.kill()
                spawn_enemy()  # Spawn a new enemy immediately after collision

            if (P1.width < 300 and P1.height < 500):
                P1.resize(scale_factor=1.05)
            #refresh screen
                show_score()
                pygame.display.update()

        show_score()
        pygame.display.update()
        FramePerSec.tick(FPS)

start_screen()
GameLoop()