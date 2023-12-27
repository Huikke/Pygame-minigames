import pygame
import sys
from random import randint

# Set Apple location
def spawn_apple():
    while True:
        apple_x = randint(1,15)
        apple_y = randint(1,15)
        if board[apple_x][apple_y] != 0:
            continue
        else:
            board[apple_x][apple_y] = "a"
            return apple_x, apple_y

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
# Set font for use
# https://www.pygame.org/docs/ref/font.html
font = pygame.font.SysFont(None, 50)
# Window title
pygame.display.set_caption("Snake")

# Load art
wall = pygame.image.load("art/wall.png").convert()
ground = pygame.image.load("art/ground.png").convert()
snake_head = pygame.image.load("art/snake_head.png").convert()
snake_body = pygame.image.load("art/snake_body.png").convert()
apple = pygame.image.load("art/apple.png").convert_alpha()

# Make the board
# 0 = ground, "w" = wall, 1..n = body, n+1 = head
board = [[0 for _ in range(0, 16)] for _ in range(0, 16)]
for i in range(0, 16):
    for j in range(0, 16):
        if i == 0 or j == 0 or i == 15 or j == 15:
            board[i][j] = "w"
board[2][3] = 2
board[2][2] = 1
# debug
for i in board:
    print(i)

# Gameplay related variables
snake_len = 2
direction = (0, 1)
fps_timer = 0
game_over = False

# Ready()
apple_x, apple_y = spawn_apple()

# Process()
while True:
    # Takes care of closing the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game_over:
            pygame.quit()
            sys.exit()

    # Gameplay related variables
    grow = False

    # Observes keys
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
    if fps_timer == 10:
        fps_timer = 0

        # check head location
        for i in range(1,15):
            for j in range(1,15):
                if board[i][j] == snake_len:
                    # Stops snake moving backwards
                    if board[i + direction[0]][j + direction[1]] == snake_len - 1:
                        direction = (-direction[0], -direction[1])
                    
                    next_tile = (i + direction[0], j + direction[1])

                    # Detects if apple is eaten and is game over
                    if board[i + direction[0]][j + direction[1]] == "a":
                        grow = True
                        snake_len += 1
                    elif board[i + direction[0]][j + direction[1]] == "w":
                        game_over = True
                    elif board[i + direction[0]][j + direction[1]] > 1:
                        game_over = True

        # does depending if apple is eaten
        if not grow:
            for i in range(1,15):
                for j in range(1,15):
                    if board[i][j] != 0 and board[i][j] != "a":
                        board[i][j] -= 1
        else:
            apple_x, apple_y = spawn_apple()

        # places head to next tile
        board[next_tile[0]][next_tile[1]] = snake_len

        # debug
        for i in board:
            print(i)
    
    # Blit walls
    for i in range(0,800,50):
        screen.blit(wall,(i,0))
        screen.blit(wall,(0,i))
        screen.blit(wall,(750,i))
        screen.blit(wall,(i,750))

    # Blit grounds
    for i in range(50, 750, 50):
        for j in range(50, 750, 50):
            screen.blit(ground,(i,j))

    # Rotate snake's head
    match direction:
        case (-1, 0):
            angle = 0
        case (0, -1):
            angle = 90
        case (1, 0):
            angle = 180
        case (0, 1):
            angle = 270
    rotated_snake_head = pygame.transform.rotate(snake_head, angle)

    # Blit snake
    for i in range(1,15):
        for j in range(1,15):
            if board[i][j] == 0:
                continue
            elif board[i][j] == snake_len:
                screen.blit(rotated_snake_head,(j*50,i*50))
            elif board[i][j] == "a":
                screen.blit(apple,(apple_y*50,apple_x*50))
            else:
                screen.blit(snake_body,(j*50,i*50))

    else:
        fps_timer += 1


    pygame.display.update()
    clock.tick(60)