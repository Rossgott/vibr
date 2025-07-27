from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Vibr API",
    description="AI-powered game creation platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Vibr API is running", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Welcome to Vibr API", "docs": "/docs"}

@app.post("/api/generate-game")
async def generate_game(request: dict):
    """Generate game code from prompt"""
    try:
        prompt = request.get("prompt", "Custom Game")
        
        # Simple fallback game generation
        game_code = f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vibr Game - {prompt[:50] if prompt else 'Custom Game'}")

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

pygame.quit()'''

        return {
            "success": True,
            "code": game_code,
            "message": "Game generated successfully (demo mode)"
        }
        
    except Exception as e:
        return {
            "success": False,
            "code": "",
            "message": f"Failed to generate game: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000))) 