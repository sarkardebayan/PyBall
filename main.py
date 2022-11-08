import pygame,random
pygame.init()
clock = pygame.time.Clock()

# Dimensions of the window
WIDTH , HEIGHT = 1080,700

# Colors
BG = (29,31,33)
ACC_COLOR = (175,175,175)
PLAYER_COLOR = (255,255,255)
counter = 0
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(BG)
player = pygame.Rect(100, HEIGHT/2 - 15, 30,30)
player_vel_y = 8 # Initial velocity of the player
g = 1.5 # Gravity
game_font = pygame.font.Font('freesansbold.ttf', 28)
SCORE = 0
try:
    HIGHSCORE = int(open('.NEVERGONNAGIVEYOUUP','r').read())
except:
    HIGHSCORE = 0
    open('.NEVERGONNAGIVEYOUUP','w').write('0')

# Pipes
pipes = []        
prev_x = WIDTH
pipe_height = 140 # The gap between the two pipes
pipe_vel = 3
pipe_intervals = 1050 # Defining the interval at which new pipes will be generated (in milliseconds)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_intervals) # Generate a pipe at a certain intervals
def generate_pipes(): # This function generates random pipes
    x = random.randint(50,450)
    pipe1 = pygame.Rect(prev_x, 0, 25,x)
    pipe2 = pygame.Rect(prev_x, pipe1.bottom+pipe_height, 25,HEIGHT-pipe_height-x)
    return pipe1,pipe2
def move_player():
    global player_vel_y
    if player.bottom >= HEIGHT or player.top <= 0:
        player.y = HEIGHT - 30
        player_vel_y *= -1 # Change direction if you hit the boundaries
def show_score():
    player_text = game_font.render(f'SCORE : {SCORE}',False,ACC_COLOR)
    screen.blit(player_text,(WIDTH/2 - 90,200))
    high = game_font.render(f'HIGHSCORE : {HIGHSCORE}',False,ACC_COLOR)
    screen.blit(high,(WIDTH/2 - 120,230))
def exit_menu(): # After you hit a pipe
    global SCORE,HIGHSCORE,counter,pipes
    running = True
    while running:
        screen.fill(BG)
        player_text = game_font.render('GAME OVER !',False,ACC_COLOR)
        screen.blit(player_text,(WIDTH/2 - 150, 200))
        if (new_high_score):
            congrats = game_font.render('Congratulations ! You\'ve just set a new high score',False,ACC_COLOR)
            screen.blit(congrats,(WIDTH/2 - 300, 250))
        player_text = game_font.render(f'SCORE : {SCORE}',False,ACC_COLOR)
        screen.blit(player_text,(WIDTH/2 - 200, HEIGHT/2 - 50))
        high = game_font.render(f'HIGHSCORE : {HIGHSCORE}',False,ACC_COLOR)
        screen.blit(high,(WIDTH/2 - 200,HEIGHT/2 - 20))
        enter = game_font.render('Press ENTER to quit',False,ACC_COLOR)
        retry = game_font.render('Press SPACE to retry',False,ACC_COLOR)
        screen.blit(enter,(WIDTH/2 - 200,HEIGHT/2 + 10))
        screen.blit(retry, (WIDTH/2 - 200, HEIGHT/2 + 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(f"SCORE : {SCORE}")
                    print(f"CURRENT HIGH SCORE : {HIGHSCORE}")
                    quit()
                if event.key == pygame.K_SPACE:
                    open('.NEVERGONNAGIVEYOUUP','r+').write(str(HIGHSCORE))
                    counter = 0
                    SCORE = 0
                    # HIGHSCORE = 0
                    pipes.clear()
                    running = False
        pygame.display.update()
        clock.tick(60)
    return

new_high_score = False # Checks if the player has set a new highscore. False by default
while True:
    counter +=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # player_vel_y = 0
                player_vel_y = -10
        if event.type == SPAWNPIPE:
            pipe1,pipe2 = generate_pipes()
            pipes.append([pipe1,pipe2])
    player_vel_y+=0.5*g
    player.y += player_vel_y
    move_player()   
    screen.fill(BG)
    pygame.draw.ellipse(screen,PLAYER_COLOR,player) # Displaying the player on screen
    show_score()
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pygame.draw.rect(screen,ACC_COLOR,pipe)
            pipe.x -= 3
            if pipe.colliderect(player): # If the player hits a pipe
                exit_menu()
        if pipe_pair[0].x < player.x and pipe_pair[1].x < player.x:
            SCORE+=10
        if pipe_pair[0].x < player.x:
            pipes.pop(0)
        if SCORE >= HIGHSCORE:
            new_high_score =True
            HIGHSCORE = SCORE
            open('.NEVERGONNAGIVEYOUUP','r+').write(str(HIGHSCORE))
    pygame.display.update()
    clock.tick(60)
