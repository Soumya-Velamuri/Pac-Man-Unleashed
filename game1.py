import pygame
import sys
import random
import time

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Game window settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man with Levels and Structured Dots")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game settings
clock = pygame.time.Clock()
FPS = 60

# Load sound effects
collect_dot_sound = pygame.mixer.Sound("collect.ogg")
game_over_sound = pygame.mixer.Sound("game_over.wav")

# Pac-Man settings
pacman_size = 30
pacman_speed = 5
pacman_x, pacman_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Ghost settings
ghost_size = 30
ghost_speed = 3
ghost_x, ghost_y = random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)
ghost_direction = random.choice(['left', 'right', 'up', 'down'])
change_direction_timer = random.randint(30, 120)

# Dot settings
dot_radius = 5
dots = []

# Score and level
score = 0
current_level = 1

def initialize_dots():
    global dots
    dots = []
    spacing = 50  # Space between dots
    for x in range(0, SCREEN_WIDTH, spacing):
        for y in range(0, SCREEN_HEIGHT, spacing):
            dots.append((x + spacing // 2, y + spacing // 2))

def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), pacman_size // 2)

def draw_ghost(x, y):
    pygame.draw.circle(screen, RED, (x, y), ghost_size // 2)

def draw_dots():
    for dot in dots:
        pygame.draw.circle(screen, WHITE, dot, dot_radius)

def move_ghost(x, y, speed, direction, timer):
    if timer <= 0:
        direction = random.choice(['left', 'right', 'up', 'down'])
        timer = random.randint(30, 120)
    if direction == 'left':
        x = max(x - speed, ghost_size // 2)
    elif direction == 'right':
        x = min(x + speed, SCREEN_WIDTH - ghost_size // 2)
    elif direction == 'up':
        y = max(y - speed, ghost_size // 2)
    elif direction == 'down':
        y = min(y + speed, SCREEN_HEIGHT - ghost_size // 2)
    timer -= 1
    return x, y, direction, timer

def check_collision(px, py, gx, gy):
    return ((px - gx) ** 2 + (py - gy) ** 2) ** 0.5 < (pacman_size // 2 + ghost_size // 2)

def collect_dots(px, py):
    global score
    pacman_rect = pygame.Rect(px - pacman_size // 2, py - pacman_size // 2, pacman_size, pacman_size)
    for dot in dots[:]:
        dot_rect = pygame.Rect(dot[0] - dot_radius, dot[1] - dot_radius, 2 * dot_radius, 2 * dot_radius)
        if pacman_rect.colliderect(dot_rect):
            dots.remove(dot)
            score += 1
            collect_dot_sound.play()

def display_game_over():
    game_over_sound.play()
    time.sleep(1)  # Let sound play
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  # Show message for 3 seconds
    reset_game()

def reset_game():
    global current_level, score, pacman_x, pacman_y, ghost_x, ghost_y, ghost_speed
    current_level = 1  # Reset to level 1
    score = 0
    pacman_x, pacman_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    ghost_x, ghost_y = random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)
    ghost_speed = 3
    initialize_dots()

def level_up():
    global current_level, ghost_speed
    current_level += 1
    if current_level > 3:
        display_congratulations()
        reset_game()  # Start over after winning
    else:
        ghost_speed += 1  # Increase ghost speed with each level
        initialize_dots()  # Re-initialize dots for the new level

def display_congratulations():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 74)
    congrats_text = font.render("Congratulations!", True, WHITE)
    screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, SCREEN_HEIGHT // 2 - congrats_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(3)  # Show message for 3 seconds

initialize_dots()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x = max(pacman_x - pacman_speed, pacman_size // 2)
    elif keys[pygame.K_RIGHT]:
        pacman_x = min(pacman_x + pacman_speed, SCREEN_WIDTH - pacman_size // 2)
    if keys[pygame.K_UP]:
        pacman_y = max(pacman_y - pacman_speed, pacman_size // 2)
    elif keys[pygame.K_DOWN]:
        pacman_y = min(pacman_y + pacman_speed, SCREEN_HEIGHT - pacman_size // 2)

    ghost_x, ghost_y, ghost_direction, change_direction_timer = move_ghost(ghost_x, ghost_y, ghost_speed, ghost_direction, change_direction_timer)

    collect_dots(pacman_x, pacman_y)

    if not dots:  # Level complete
        level_up()

    if check_collision(pacman_x, pacman_y, ghost_x, ghost_y):
        display_game_over()
        reset_game()

    screen.fill(BLACK)
    draw_pacman(pacman_x, pacman_y)
    draw_ghost(ghost_x, ghost_y)
    draw_dots()

    # Display score and level
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
