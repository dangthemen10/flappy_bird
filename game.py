import pygame, sys, random

# Định nghĩa các hằng số
SCREEN_WIDTH = 432
SCREEN_HEIGHT = 768
FLOOR_Y_POS = 650
BIRD_START_POS = (100, 384)
GRAVITY = 0.25
BIRD_FLAP_VELOCITY = -11
PIPE_SPEED = 5
INITIAL_PIPE_GAP = 800
MIN_PIPE_GAP = 300
INITIAL_FPS = 80
MAX_FPS = 120

# Khởi tạo biến điều khiển khó khăn
current_pipe_gap = INITIAL_PIPE_GAP
current_fps = INITIAL_FPS

# Tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor, (floor_x_pos, FLOOR_Y_POS))
    screen.blit(floor, (floor_x_pos + SCREEN_WIDTH, FLOOR_Y_POS))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - current_pipe_gap))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_SPEED
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= FLOOR_Y_POS:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= FLOOR_Y_POS:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(BIRD_START_POS[0], bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(score_surface, score_rect)
    elif game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH / 2, 630))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def increase_difficulty(score):
    global current_pipe_gap, current_fps
    if score < 20:
        current_pipe_gap = INITIAL_PIPE_GAP  # Tăng khoảng cách khi điểm dưới 20
    if score >= 20:
        current_pipe_gap = max(MIN_PIPE_GAP, INITIAL_PIPE_GAP - 100)
        current_fps = min(MAX_FPS, INITIAL_FPS + 10)
    if score >= 50:
        current_pipe_gap = max(MIN_PIPE_GAP, INITIAL_PIPE_GAP - 200)
        current_fps = min(MAX_FPS, INITIAL_FPS + 10)
    if score >= 100:
        current_pipe_gap = max(MIN_PIPE_GAP, INITIAL_PIPE_GAP - 300)
        current_fps = min(MAX_FPS, INITIAL_FPS + 20)

# Khởi tạo Pygame và các thành phần
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('./04B_19.ttf', 35)

# Tạo các biến cho trò chơi
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Chèn background
bg = pygame.image.load('./assests/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# Chèn sàn
floor = pygame.image.load('./assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load('./assests/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('./assests/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('./assests/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=BIRD_START_POS)

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Tạo ống
pipe_surface = pygame.image.load('./assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer cho ống
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('./assests/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound('./sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('./sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('./sound/sfx_point.wav')
score_sound_countdown = 100

# Vòng lặp của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement = BIRD_FLAP_VELOCITY
                    flap_sound.play()
                else:  # Khi game kết thúc
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = BIRD_START_POS
                    bird_movement = 0
                    score = 0
                    current_pipe_gap = INITIAL_PIPE_GAP
                    current_fps = INITIAL_FPS
        if event.type == spawnpipe and game_active:
            pipe_list.extend(create_pipe())
        if event.type == birdflap and game_active:
            bird_index = (bird_index + 1) % len(bird_list)
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))
    if game_active:
        # Chim
        bird_movement += GRAVITY
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        increase_difficulty(score)  # Tăng độ khó dựa trên điểm số
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -SCREEN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(current_fps)
