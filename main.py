import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop Game")

# Load background image and resize it to fit the screen
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load balloon image
balloon_img = pygame.image.load("balloon.png")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Define balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = balloon_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = HEIGHT
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()


# Create sprite groups
all_sprites = pygame.sprite.Group()
balloons = pygame.sprite.Group()

# Set up game variables
score = 0
game_font = pygame.font.Font(None, 48)
score_font = pygame.font.Font(None, 36)
timer_font = pygame.font.Font(None, 64)

# Define game states
START_SCREEN = 0
GAME_PLAYING = 1
GAME_OVER = 2
current_state = START_SCREEN

# Define game loop
running = True
clock = pygame.time.Clock()
timer = 120
start_ticks = 0
while running:
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == GAME_PLAYING:
            pos = pygame.mouse.get_pos()
            missed = True
            for balloon in balloons:
                if balloon.rect.collidepoint(pos):
                    balloon.kill()
                    score += 2
                    missed = False
            if missed:
                score -= 1  # Deduct 1 point for missed balloon
        elif event.type == pygame.MOUSEBUTTONDOWN and current_state == START_SCREEN:
            current_state = GAME_PLAYING
            start_ticks = pygame.time.get_ticks()

    # Game logic
    if current_state == GAME_PLAYING:
        # Calculate timer
        seconds = max(120 - int((pygame.time.get_ticks() - start_ticks) / 1000), 0)

        # Create new balloons
        if random.random() < 0.02:
            balloon = Balloon()
            all_sprites.add(balloon)
            balloons.add(balloon)

        # Update sprites
        all_sprites.update()

        # Check for collisions
        for balloon in balloons:
            if balloon.rect.y + balloon.rect.height < 0:
                balloon.kill()

        # Check game over condition
        if seconds <= 0:
            current_state = GAME_OVER

    # Clear the screen
    screen.blit(background_img, (0, 0))

    # Draw sprites
    all_sprites.draw(screen)

    # Draw UI elements
    if current_state == START_SCREEN:
        start_text = game_font.render("Balloon Pop Game", True, BLACK)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50))
        start_button_text = game_font.render("Start", True, WHITE)
        start_button_rect = start_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 75))
        screen.blit(start_button_text, start_button_rect)
    elif current_state == GAME_PLAYING:
        score_text = score_font.render(f"Score: {score}", True, BLACK)
        score_text_rect = score_text.get_rect(right=WIDTH - 10, top=10)
        screen.blit(score_text, score_text_rect)

        timer_text = timer_font.render(f"Timer: {seconds // 60:02d}:{seconds % 60:02d}", True, BLACK)
        timer_text_rect = timer_text.get_rect(left=10, top=10)
        screen.blit(timer_text, timer_text_rect)
    elif current_state == GAME_OVER:
        game_over_text = game_font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)

        final_score_text = score_font.render(f"Final Score: {score}", True, BLACK)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(final_score_text, final_score_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
