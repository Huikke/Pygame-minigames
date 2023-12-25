import pygame
import sys

# Required
pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
# Set font for use
# https://www.pygame.org/docs/ref/font.html
font = pygame.font.SysFont(None, 50)
# Window title
pygame.display.set_caption("Snake")

# Fill with your own code
wall = pygame.image.load("art/wall.png").convert()
ground = pygame.image.load("art/ground.png").convert()
snake_head = pygame.image.load("art/snake_head.png").convert()
snake_body = pygame.image.load("art/snake_body.png").convert()
text_surface = font.render("My Game", False, "Purple")

# Make the board
# 0 = ground, "w" = wall, 1..n = body, n+1 = head
board = [[0 for _ in range(0, 16)] for _ in range(0, 16)]
for i in range(0, 16):
    for j in range(0, 16):
        if i == 0 or j == 0 or i == 15 or j == 15:
            board[i][j] = "w"
board[2][3] = 2
board[2][2] = 1
for i in board:
    print(i)

snake_len = 2
direction = (0, 1)
fps_timer = 0

while True:
    # Takes care of closing the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for i in range(0,800,50):
        screen.blit(wall,(i,0))
        screen.blit(wall,(0,i))
        screen.blit(wall,(750,i))
        screen.blit(wall,(i,750))

    for i in range(50, 750, 50):
        for j in range(50, 750, 50):
            screen.blit(ground,(i,j))

    for i in range(1,15):
        for j in range(1,15):
            if board[i][j] != 0:
                if board[i][j] == snake_len:
                    screen.blit(snake_head,(j*50,i*50))
                else:
                    screen.blit(snake_body,(j*50,i*50))

    key_down = pygame.key.get_pressed()
    if key_down[pygame.K_LEFT] or key_down[pygame.K_a]:
        direction = (0, -1)
    if key_down[pygame.K_RIGHT] or key_down[pygame.K_d]:
        direction = (0, 1)
    if key_down[pygame.K_DOWN] or key_down[pygame.K_s]:
        direction = (1, 0)
    if key_down[pygame.K_UP] or key_down[pygame.K_w]:
        direction = (-1, 0)

    # Movement
    if fps_timer == 60:
        fps_timer = 0
        for i in range(1,15):
            for j in range(1,15):
                if board[i][j] != 0:
                    board[i][j] -= 1
        for i in range(1,15):
            for j in range(1,15):
                if board[i][j] == snake_len - 1:
                    print(i + direction[0], j + direction[1])
                    board[i + direction[0]][j + direction[1]] = snake_len
        # debug
        for i in board:
            print(i)
    else:
        fps_timer += 1
    # Takes care of updating the game and FPS
    pygame.display.update()
    clock.tick(60)