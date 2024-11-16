import pygame

# project will be Like a Dino! game
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.mixer.music.load("Attack on Titan ⧸ Shingeki no Kyojin Opening - Guren no Yumiya 8-bit and 16-bit Remix.mp3")
pygame.mixer.music.play()

running = True

dt = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

RED = (255,0,0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    pygame.mouse.set_visible(False)

    mouse_x,mouse_y = pygame.mouse.get_pos()
    player_pos.x = float(mouse_x)

    # RENDER YOUR GAME HERE
    pygame.draw.rect(screen, RED, (player_pos.x, screen.get_height() / 2 + 100, 50, 100))
    print(player_pos.x)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

