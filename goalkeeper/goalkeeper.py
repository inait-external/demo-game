import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Goalkeeper Challenge")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
GRAY = (169, 169, 169)

# Goalkeeper properties
goalkeeper_width, goalkeeper_height = 50, 100
goalkeeper_y = HEIGHT - goalkeeper_height - 50

# Ball properties
ball_radius = 15
ball_positions = ["left", "middle", "right"]
ball_x_positions = {"left": WIDTH // 4, "middle": WIDTH // 2, "right": 3 * WIDTH // 4}
ball_y = 50
ball_speed = 10  # Increased speed
ball_direction = 1  # 1 for down, -1 for up

# Font
font = pygame.font.Font(None, 36)

# Game variables
clock = pygame.time.Clock()
running = True
score = 0
num_rounds = 46
current_round = 0
goalkeeper_position = "middle"
goalkeeper_x = WIDTH // 2 - (goalkeeper_width // 2)

# Function to read moves from a file
def read_moves_from_file(file_path):
    moves = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    ball_pos_index = int(parts[0]) - 1  # Adjusting to zero-based index
                    ball_pos = ball_positions[ball_pos_index]  # Convert number to position
                    move_direction = parts[1]
                    if move_direction in ball_positions:
                        moves.append((ball_pos, move_direction))
                except (ValueError, IndexError):
                    print(f"Skipping invalid line in file: {line.strip()}")
    return moves

# Load the moves from the file
moves = read_moves_from_file("goalkeeper_moves.txt")
current_move_index = 0

# Initial game speed (FPS)
game_speed = 30

def draw_goal():
    pygame.draw.rect(screen, GRAY, (WIDTH // 8, HEIGHT - 150, WIDTH - WIDTH // 4, 10))  # goal post
    pygame.draw.rect(screen, GRAY, (WIDTH // 8, HEIGHT - 150, 10, 150))  # left post
    pygame.draw.rect(screen, GRAY, (WIDTH - WIDTH // 8 - 10, HEIGHT - 150, 10, 150))  # right post

def draw_goalkeeper(x, y):
    # Draw the head
    pygame.draw.circle(screen, BLUE, (x + goalkeeper_width // 2, y - 20), goalkeeper_width // 4)
    # Draw the body
    pygame.draw.rect(screen, BLUE, (x, y, goalkeeper_width, goalkeeper_height))
    # Draw the arms
    pygame.draw.line(screen, BLUE, (x - 20, y + 20), (x + goalkeeper_width + 20, y + 20), 5)
    # Draw the legs
    pygame.draw.line(screen, BLUE, (x + 10, y + goalkeeper_height), (x - 10, y + goalkeeper_height + 40), 5)
    pygame.draw.line(screen, BLUE, (x + goalkeeper_width - 10, y + goalkeeper_height), (x + goalkeeper_width + 10, y + goalkeeper_height + 40), 5)

def draw_field():
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, HEIGHT))  # Green field background

# Main game loop
while running and current_round < num_rounds:
    draw_field()  # Draw the field background
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_speed += 5  # Increase speed
            elif event.key == pygame.K_DOWN:
                game_speed = max(5, game_speed - 5)  # Decrease speed, minimum speed is 5

    # Use the current move from the file
    if current_move_index < len(moves):
        ball_position, move_direction = moves[current_move_index]
        goalkeeper_position = move_direction
        goalkeeper_x = ball_x_positions[goalkeeper_position] - (goalkeeper_width // 2)

    # Move the ball
    ball_y += ball_speed * ball_direction
    
    # Draw goal post
    draw_goal()

    # Draw ball
    pygame.draw.circle(screen, RED, (ball_x_positions[ball_position], ball_y), ball_radius)
    
    # Draw goalkeeper
    draw_goalkeeper(goalkeeper_x, goalkeeper_y)
    
    # Check if goalkeeper catches the ball
    if ball_direction == 1 and ball_y >= goalkeeper_y - ball_radius:
        if goalkeeper_position == ball_position:
            print("Goalkeeper caught the ball!")
            score += 1
            ball_direction = -1  # Bounce the ball back up
        else:
            print("Goalkeeper missed the ball.")
            # Prepare for next round
            ball_y = 50
            ball_direction = 1
            current_round += 1
            current_move_index += 1

    if ball_direction == -1 and ball_y <= ball_radius:
        # Ball has bounced back to the top, reset for next round
        ball_y = 50
        ball_direction = 1
        current_round += 1
        current_move_index += 1

    # Display score and rounds
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    round_text = font.render(f"Round: {current_round + 1}/{num_rounds}", True, BLACK)
    screen.blit(round_text, (WIDTH - 200, 10))
    
    pygame.display.flip()
    clock.tick(game_speed)

pygame.quit()

print(f"Final Score: {score}/{num_rounds}")
