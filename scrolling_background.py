# Imports
import os
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
pygame.display.set_caption("Like a Sapling!")

pygame.mouse.set_visible(False)

click_sound = pygame.mixer.Sound("Click.mp3")  # Replace with your sound effect file
click_sound.set_volume(1.0)  # Set volume (0.0 to 1.0)

gainDrops = pygame.mixer.Sound("GainDrop.mp3")
gainDrops.set_volume(0.1)

def list_mp3_files(directory):
    """Returns a list of .mp3 files from the specified directory."""
    return [file for file in os.listdir(directory) if file.endswith('.mp3')]

# Specify the directory containing your .mp3 files
directory_path = 'G:\My Drive\YEAR 2\Hackathon\HackSheffield9\music'  # Replace with your directory path

# Get the list of .mp3 files
mp3_files = list_mp3_files(directory_path)

print(mp3_files)



# Start Screen
def start_screen():
    pygame.mixer.music.load("StartMusic.mp3")
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play()  # Loop the music indefinitely
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button click
                    pygame.mixer.music.stop()  # Loop the music indefinitely
                    click_sound.play()
                    return  # Start the game loop

        DISPLAYSURF.fill((168, 220, 171)) # Fill the screen with green
        title_text = font_small.render("Like a Sapling!", True, "#4e664f")
        description_text = font_small.render("Collect Raindrops to Grow!", True, BLACK)
        instructions_text = font_small.render("Click to Start", True, BLACK)

        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2 
        title_y = SCREEN_HEIGHT // 5  # Top part of the screen
        DISPLAYSURF.blit(title_text, (title_x, title_y))

        instructions_x = (SCREEN_WIDTH - instructions_text.get_width()) // 2
        instructions_y = SCREEN_HEIGHT // 2  # Center of the screen
        DISPLAYSURF.blit(instructions_text, (instructions_x, instructions_y))

        description_x = (SCREEN_WIDTH - description_text.get_width()) // 2
        description_y = SCREEN_HEIGHT // 3  # Center of the screen
        DISPLAYSURF.blit(description_text, (description_x, description_y))

        pygame.display.update()  # Update the screen



class Raindrops(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("water.png")
        self.image = pygame.transform.scale(self.original_image, (42, 70))
        self.collision_rect = self.image.get_rect()
        self.collision_rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Initialize the position
        self.missed = False

    def fall(self):
        self.collision_rect.move_ip(0, SPEED)
        if self.collision_rect.top > 510:
            if not self.missed:
                self.missed = True  # Mark as missed the first time
                self.kill()
                return True
            
            return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("tree_top.png")
        self.top_image = pygame.transform.scale(self.original_image, (150, 150))  # Scale the image
        self.rect = self.top_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT ))
        self.collision_rect = self.top_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        self.segments = []  # To store tree_middle.png images

        self.start_time = None  # To store the time when the move starts
        self.moving_up = False  # Flag to indicate if the movement is active


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

    def grow(self):
        # Load and scale the tree_middle.png image
        segment_image = pygame.image.load('tree_middle.png').convert_alpha()
        segment_image = pygame.transform.scale(segment_image, (150,150))


        if self.segments:
            # Place the new segment below the last segment
            last_segment_rect = self.segments[-1][1]
            new_segment_rect = segment_image.get_rect(midbottom=(SCREEN_WIDTH // 2 , last_segment_rect.bottom + 40))
        else:
            # Place the first segment directly below the tree top
            new_segment_rect = segment_image.get_rect(midbottom=(SCREEN_WIDTH // 2 , SCREEN_HEIGHT))

        self.segments.append((segment_image, new_segment_rect))


    def update(self):
        mouse_x, _ = pygame.mouse.get_pos()
        self.rect.centerx = mouse_x



        # Align all segments to the x-coordinate of the tree top
        for i, (image, segment_rect) in enumerate(self.segments):
            # Move the segment to match the tree top's x-position
            new_x = self.rect.centerx - segment_rect.width // 2
            self.segments[i] = (image, segment_rect.move(new_x - segment_rect.x, 0))



    def checkClick(self):
        return pygame.mouse.get_pressed()[0] == 1  # Check if left mouse button is pressed
    
    def draw_outline(self, surface):
        # Draw the outline for the top tree part (player's main rectangle)
        pygame.draw.rect(surface, RED, self.rect, 3)  # 3 is the thickness of the outline


        # Draw outlines for each tree segment
        for segment_image, segment_rect in self.segments:
            pygame.draw.rect(surface, RED, segment_rect, 3)  # Outline the segment rectangles

    
    def draw(self, surface):
        # Draw all tree segments first
        for segment_image, segment_rect in self.segments:
            surface.blit(segment_image, segment_rect)
        # Draw the tree top
        surface.blit(self.top_image, self.rect)
        self.draw_outline(surface)
        


    def move_up(self,score):
        """ Move the tree upwards, including all segments """
        if self.moving_up:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            

            # Move upwards as long as 5 seconds haven't passed
            if elapsed_time < 5000:
                x = round(score / 10)

                self.rect.y -= x*2 # Move P1 upwards by 2
                for i, (segment_image, segment_rect) in enumerate(self.segments):
                    self.segments[i] = (segment_image, segment_rect.move(0, -x*2))  
            else:
                self.moving_up = False  # Stop moving after 5 seconds

    def start_moving_up(self):
        """Start the upward movement"""
        self.start_time = pygame.time.get_ticks()  # Record the start time
        self.moving_up = True  # Set flag to start moving upwards

    def getSegments(self):
        return self.segments
    
    def insertBottomTree(self):
        segment_image = pygame.image.load('tree_bottom.png').convert_alpha()
        segment_image = pygame.transform.scale(segment_image, (150,150))

        if self.segments:
            # Place the new segment below the last segment
            last_segment_rect = self.segments[-1][1]
            new_segment_rect = segment_image.get_rect(midbottom=(SCREEN_WIDTH // 2 , last_segment_rect.bottom))
        else:
            # Place the first segment directly below the tree top
            new_segment_rect = segment_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 57))

        self.segments.append((segment_image, new_segment_rect))
    








class Background():
    def __init__(self):
        # Load and scale the background image
        self.bgimage = pygame.image.load('Background.png')  # Replace with your image path
        self.bgimage = pygame.transform.scale(self.bgimage, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit screen

        # Get the rect (size) of the background image
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.movingUpSpeed = 0

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
    randSong = random.randint(0, len(mp3_files) - 1)
    chosenSong = mp3_files[randSong]
    print(randSong)
    pygame.mixer.music.load("music/" + chosenSong)
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play()  # Loop the music indefinitely
    global SCORE, SPEED, SPAWN_TIMER

    spawn_interval = 1000  # Start with 1000 ms (1 second)
    spawn_time = 0  # Timer for decrement every 3 seconds

# Setting up Sprites
    P1 = Player()
    #E1 = Raindrops()

    back_ground = Background()

# Creating Sprites Groups
    raindropsCollection = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    #all_sprites.add(E1)

# Adding a new User event
    INC_SPEED = pygame.USEREVENT + 1
    SPAWN_ENEMY = pygame.USEREVENT + 2
    DECREMENT_TIMER = pygame.USEREVENT + 3 # Custom event for timer decrement
    pygame.time.set_timer(INC_SPEED, 3000)  # Increase speed every 3 seconds
    pygame.time.set_timer(DECREMENT_TIMER, 2000)
    pygame.time.set_timer(SPAWN_ENEMY, spawn_interval)  # Spawn enemies every second


    score = 0;
    font = pygame.font.SysFont(None, 36);
    missed = 0

    def show_score():
        score_surface = font.render("Score: " + str(score), True, BLACK)
        DISPLAYSURF.blit(score_surface, (10, 10))

    # Game Loop
    while True:

    # Cycles through all occurring events
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 1
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWN_ENEMY:
                new_raindrop = Raindrops()
                raindropsCollection.add(new_raindrop)
                all_sprites.add(new_raindrop)
            if event.type == DECREMENT_TIMER:
                spawn_interval = max(300, spawn_interval - 100)  # Prevent the interval from going below 200ms
                print(spawn_interval)
                pygame.time.set_timer(SPAWN_ENEMY, spawn_interval)  # Update the spawn interval

        for entity in all_sprites:
            if isinstance(entity, Raindrops):
                if entity.fall():
                    missed += 1  # Increase missed count if collectible goes off-screen
        

        # Define a custom collide function that checks collisions against P1.collision_rect
        def custom_collide(raindrop_sprite, p1_sprite):
        # This assumes raindrop_sprite is a sprite in raindropsCollection and has a rect
            return raindrop_sprite.rect.colliderect(p1_sprite.collision_rect)
        
        
        # Check collisions
        collected = pygame.sprite.spritecollide(P1, raindropsCollection, True, collided=custom_collide)
        if collected:
                gainDrops.play()
                score += len(collected)
                for _ in collected:
                    P1.grow()  # Add a segment for each collected item



        if missed >= 5:
            
            DISPLAYSURF.fill((WHITE))  # Fill the screen with white

            # Place tree_bottom at the end of the stack
            P1.insertBottomTree()
            P1.update()

            # Start moving P1 upwards for 5 seconds
            P1.start_moving_up()

            # Wait for 5 seconds while moving P1 and segments up
            while pygame.time.get_ticks() - P1.start_time < 5000:
                P1.move_up(score)  # Update P1 and its movement upwards
                DISPLAYSURF.fill((255, 255, 255))  # Clear the screen
                back_ground.render()  # Render the background

                game_over_text = font.render("Game Over", True, BLACK)
                score_text = font.render(f"Score: {score}", True, BLACK)
                DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3))
                DISPLAYSURF.blit(score_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

                P1.draw(DISPLAYSURF)  # Draw P1 and its segments
                pygame.display.update()
                pygame.time.Clock().tick(60)  # Cap the frame rate

            break  # Exit the game loop after 5 seconds of movement

            # Update the game display
            pygame.display.update()

            # Control the frame rate
            pygame.time.Clock().tick(60)

            pygame.quit()

        back_ground.update()
        back_ground.render()

        # Display Scores 
        scores = font_small.render(str(SCORE), True, BLACK)
        missed_text = font.render(f"Missed: {missed}", True, BLACK)
        DISPLAYSURF.blit(scores, (10, 10))
        DISPLAYSURF.blit(missed_text, (10, 50))

        P1.update()
        P1.draw(DISPLAYSURF)

        for raindrop in raindropsCollection:
            DISPLAYSURF.blit(raindrop.image, raindrop.collision_rect)

        show_score()
        pygame.display.update()
        FramePerSec.tick(FPS)

start_screen()
GameLoop()