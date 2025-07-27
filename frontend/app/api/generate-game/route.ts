export async function POST(request: Request) {
  try {
    const { prompt } = await request.json();
    
    // Simple fallback game generation (no AI required)
    const gameCode = `import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vibr Game - ${prompt?.substring(0, 50) || 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # Keep player on screen
    player_x = max(0, min(WIDTH - 50, player_x))
    player_y = max(0, min(HEIGHT - 50, player_y))
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
    
    # Draw instructions
    font = pygame.font.Font(None, 36)
    text = font.render("Use arrow keys to move", True, BLACK)
    screen.blit(text, (10, 10))
    
    # Draw game title
    title = font.render("Vibr Game", True, GREEN)
    screen.blit(title, (10, 50))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()`;

    return Response.json({
      success: true,
      code: gameCode,
      message: "Game generated successfully (demo mode)"
    });
    
  } catch (error) {
    return Response.json({
      success: false,
      error: "Failed to generate game"
    }, { status: 500 });
  }
} 