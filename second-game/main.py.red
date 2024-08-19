import os
import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Doors Challenge")

# Colors
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)

# Door properties
door_width = WIDTH // 3
door_height = 250  # Reduced door height
door_y = HEIGHT - door_height - 50

# Ball properties
ball_radius = 15  # Reduced ball size
ball_speed = 5  # Initial ball speed (adjustable with arrow keys)
ball_direction = 1
ball_y_start = 50

# Font
font = pygame.font.Font(None, 36)  # Reduced font size

# Game variables
clock = pygame.time.Clock()
running = True
score = 0
current_round = 0
level = 1

# Input file containing the level details and actions
input_file = "game_levels_4.txt"

def read_input_file(file):
    levels = {}
    with open(file, "r") as f:
        lines = f.readlines()
    
    level = None
    rounds_per_level = 0
    rounds = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Skip empty lines and comments
            continue
        if line.startswith("level:"):
            if level is not None:
                levels[level] = (rounds_per_level, rounds)
            level = int(line.split(":")[1].strip())
            rounds = []
        elif line.startswith("rounds:"):
            rounds_per_level = int(line.split(":")[1].strip())
        else:
            parts = line.split()
            if len(parts) >= 2:  # Ensure there are at least two elements
                ball_position_index = int(parts[0]) - 1
                action = parts[1].strip()
                rounds.append((ball_position_index, action))
            else:
                print(f"Warning: Skipping improperly formatted line: '{line}'")
    
    if level is not None:
        levels[level] = (rounds_per_level, rounds)
    
    return levels

# Load the input data
levels_data = read_input_file(input_file)

def update_positions(n):
    return [(i + 0.5) * (door_width / n) for i in range(n)] + \
           [WIDTH // 2] + \
           [(2 * door_width) + (i + 0.5) * (door_width / n) for i in range(n)]

ball_x_positions = update_positions(1)

def update_position_to_door(n):
    return {
        (0, n - 1): "left",
        n: "middle",
        (n + 1, 2 * n): "right",
    }

position_to_door = update_position_to_door(1)
door_open = "middle"

def get_door_for_position(pos_index):
    for key, door in position_to_door.items():
        if isinstance(key, tuple):
            start, end = key
            if start <= pos_index <= end:
                return door
        elif key == pos_index:
            return door
    return None

def draw_doors(open_door):
    # Define door rectangles
    left_door_rect = pygame.Rect(0, door_y, door_width, door_height)
    middle_door_rect = pygame.Rect(door_width, door_y, door_width, door_height)
    right_door_rect = pygame.Rect(2 * door_width, door_y, door_width, door_height)

    # Draw all doors in brown first
    pygame.draw.rect(screen, BROWN, left_door_rect)
    pygame.draw.rect(screen, BROWN, middle_door_rect)
    pygame.draw.rect(screen, BROWN, right_door_rect)

    # Highlight the open door in grey
    if open_door == "left":
        pygame.draw.rect(screen, GRAY, left_door_rect)
    elif open_door == "middle":
        pygame.draw.rect(screen, GRAY, middle_door_rect)
    elif open_door == "right":
        pygame.draw.rect(screen, GRAY, right_door_rect)

    # Draw door handles
    pygame.draw.circle(screen, YELLOW, (door_width // 2, door_y + door_height // 2), 10)
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2, door_y + door_height // 2), 10)
    pygame.draw.circle(screen, YELLOW, (2 * door_width + door_width // 2, door_y + door_height // 2), 10)

def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

def increase_speed():
    global ball_speed
    ball_speed += 2  # Increase ball speed

def decrease_speed():
    global ball_speed
    ball_speed = max(2, ball_speed - 2)  # Decrease ball speed, but not below 2

# Main game loop
for level, (rounds_per_level, round_data) in sorted(levels_data.items()):
    n = level  # Increment n with each level
    ball_x_positions = update_positions(n)
    position_to_door = update_position_to_door(n)
    current_round = 0
    
    for ball_position_index, action in round_data:
        ball_y = ball_y_start  # Reset ball position for the new round
        
        while ball_y < door_y - ball_radius:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        increase_speed()
                    elif event.key == pygame.K_DOWN:
                        decrease_speed()

            # Clear the screen
            screen.fill(GREEN)
            
            # Move the ball
            ball_y += ball_speed * ball_direction

            # Set door based on action
            if action == "left":
                door_open = "left"
            elif action == "right":
                door_open = "right"
            elif action == "middle":
                door_open = "middle"

            # Draw doors
            draw_doors(door_open)

            # Draw ball
            draw_ball(ball_x_positions[ball_position_index], ball_y)

            # Draw the Score, Level, and Rounds labels
            score_text = font.render(f"Score: {score}", True, RED)
            level_text = font.render(f"Level: {level}", True, RED)
            rounds_text = font.render(f"Round: {current_round + 1}/{rounds_per_level}", True, RED)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (10, 60))
            screen.blit(rounds_text, (WIDTH - 300, 10))

            # Update the display
            pygame.display.flip()
            clock.tick(30)

        # Check if ball enters the open door
        expected_door = get_door_for_position(ball_position_index)
        if door_open == expected_door:
            score += 1
        current_round += 1

pygame.quit()

print(f"Final Score: {score}")

