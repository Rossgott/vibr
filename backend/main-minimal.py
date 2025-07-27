from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import random

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

def generate_game_code(prompt: str) -> str:
    """Generate game code based on the prompt"""
    prompt_lower = prompt.lower()
    
    # Determine game type based on keywords
    if any(word in prompt_lower for word in ['space', 'shooter', 'alien', 'spaceship', 'asteroid']):
        return generate_space_shooter(prompt)
    elif any(word in prompt_lower for word in ['platform', 'jump', 'mario', 'runner']):
        return generate_platformer(prompt)
    elif any(word in prompt_lower for word in ['puzzle', 'match', 'connect', 'block']):
        return generate_puzzle_game(prompt)
    elif any(word in prompt_lower for word in ['racing', 'car', 'drive', 'speed']):
        return generate_racing_game(prompt)
    else:
        return generate_adventure_game(prompt)

def generate_space_shooter(prompt: str) -> str:
    return f'''import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - {prompt[:50] if prompt else 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Player
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.speed = 5
        self.size = 30
        self.health = 100
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed
            
    def draw(self, screen):
        pygame.draw.polygon(screen, BLUE, [
            (self.x, self.y + self.size),
            (self.x - self.size//2, self.y),
            (self.x + self.size//2, self.y)
        ])

# Enemy
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = -20
        self.speed = random.randint(2, 5)
        self.size = 20
        
    def move(self):
        self.y += self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
        
    def is_off_screen(self):
        return self.y > HEIGHT

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.size = 5
        
    def move(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)
        
    def is_off_screen(self):
        return self.y < 0

# Game variables
player = Player()
enemies = []
bullets = []
score = 0
enemy_spawn_timer = 0
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.x, player.y))
    
    # Handle input
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 60:  # Spawn every 60 frames
        enemies.append(Enemy())
        enemy_spawn_timer = 0
    
    # Update bullets
    for bullet in bullets[:]:
        bullet.move()
        if bullet.is_off_screen():
            bullets.remove(bullet)
    
    # Update enemies
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)
            player.health -= 10
    
    # Check collisions
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if (abs(enemy.x - bullet.x) < enemy.size and 
                abs(enemy.y - bullet.y) < enemy.size):
                if enemy in enemies:
                    enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                score += 10
                break
    
    # Check player collision with enemies
    for enemy in enemies[:]:
        if (abs(enemy.x - player.x) < enemy.size and 
            abs(enemy.y - player.y) < player.size):
            enemies.remove(enemy)
            player.health -= 20
    
    # Game over check
    if player.health <= 0:
        running = False
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw stars (background)
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    # Draw game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    health_text = font.render(f"Health: {player.health}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    
    # Draw instructions
    instructions = font.render("Arrow keys: Move, Space: Shoot", True, GREEN)
    screen.blit(instructions, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
font = pygame.font.Font(None, 72)
game_over_text = font.render("GAME OVER", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
screen.blit(final_score_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
pygame.display.flip()

# Wait 3 seconds before closing
pygame.time.wait(3000)
pygame.quit()'''

def generate_platformer(prompt: str) -> str:
    return f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer - {prompt[:50] if prompt else 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)

# Player
class Player:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 100
        self.width = 30
        self.height = 40
        self.vel_y = 0
        self.jumping = False
        self.speed = 5
        
    def move(self, keys, platforms):
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # Keep player on screen
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            
        # Gravity
        self.vel_y += 0.8
        self.y += self.vel_y
        
        # Check platform collisions
        self.jumping = True
        for platform in platforms:
            if (self.x < platform.x + platform.width and 
                self.x + self.width > platform.x and
                self.y + self.height >= platform.y and
                self.y + self.height <= platform.y + 10):
                self.y = platform.y - self.height
                self.vel_y = 0
                self.jumping = False
                break
                
        # Ground collision
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.vel_y = 0
            self.jumping = False
            
    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Platform
class Platform:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 20
        
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

# Coin
class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), self.size)
            
    def check_collision(self, player):
        if not self.collected:
            if (player.x < self.x + self.size and 
                player.x + player.width > self.x - self.size and
                player.y < self.y + self.size and
                player.y + player.height > self.y - self.size):
                self.collected = True
                return True
        return False

# Game variables
player = Player()
platforms = [
    Platform(0, HEIGHT - 20, WIDTH),  # Ground
    Platform(200, HEIGHT - 150, 100),
    Platform(400, HEIGHT - 200, 100),
    Platform(600, HEIGHT - 250, 100),
    Platform(300, HEIGHT - 300, 100),
]
coins = [
    Coin(250, HEIGHT - 180),
    Coin(450, HEIGHT - 230),
    Coin(650, HEIGHT - 280),
    Coin(350, HEIGHT - 330),
]
score = 0
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Handle input
    keys = pygame.key.get_pressed()
    player.move(keys, platforms)
    
    # Check coin collisions
    for coin in coins:
        if coin.check_collision(player):
            score += 10
    
    # Clear screen
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw platforms
    for platform in platforms:
        platform.draw(screen)
    
    # Draw coins
    for coin in coins:
        coin.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Draw instructions
    instructions = font.render("Arrow keys: Move, Space: Jump", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

def generate_puzzle_game(prompt: str) -> str:
    return f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 600
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Puzzle Game - {prompt[:50] if prompt else 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Game variables
GRID_SIZE = 8
CELL_SIZE = WIDTH // GRID_SIZE
colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
grid = []
score = 0
moves = 0

# Initialize grid
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(random.choice(colors))
    grid.append(row)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = grid[y][x]
            pygame.draw.rect(screen, color, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

def get_cell_from_pos(pos):
    x, y = pos
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        return grid_x, grid_y
    return None

def find_matches():
    matches = set()
    
    # Check horizontal matches
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if (grid[y][x] == grid[y][x+1] == grid[y][x+2]):
                matches.add((x, y))
                matches.add((x+1, y))
                matches.add((x+2, y))
    
    # Check vertical matches
    for y in range(GRID_SIZE - 2):
        for x in range(GRID_SIZE):
            if (grid[y][x] == grid[y+1][x] == grid[y+2][x]):
                matches.add((x, y))
                matches.add((x, y+1))
                matches.add((x, y+2))
    
    return matches

def remove_matches(matches):
    global score
    for x, y in matches:
        grid[y][x] = random.choice(colors)
        score += 10

def drop_tiles():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 1, 0, -1):
            if grid[y][x] == None:
                # Find the first non-empty tile above
                for above_y in range(y - 1, -1, -1):
                    if grid[above_y][x] != None:
                        grid[y][x] = grid[above_y][x]
                        grid[above_y][x] = None
                        break

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            cell = get_cell_from_pos(pos)
            if cell:
                x, y = cell
                # Change the clicked tile color
                current_color = grid[y][x]
                color_index = colors.index(current_color)
                grid[y][x] = colors[(color_index + 1) % len(colors)]
                moves += 1
                
                # Check for matches
                matches = find_matches()
                if matches:
                    remove_matches(matches)
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw grid
    draw_grid()
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    moves_text = font.render(f"Moves: {moves}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 80))
    screen.blit(moves_text, (10, HEIGHT - 40))
    
    # Draw instructions
    instructions = font.render("Click tiles to change colors, match 3+ in a row", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 120))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

def generate_racing_game(prompt: str) -> str:
    return f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game - {prompt[:50] if prompt else 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Player car
class PlayerCar:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 40
        self.height = 60
        self.speed = 5
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        # Car body
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        # Car details
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 10, 30, 40))
        pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 15, 20, 30))

# Enemy car
class EnemyCar:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = -60
        self.width = 40
        self.height = 60
        self.speed = random.randint(3, 7)
        
    def move(self):
        self.y += self.speed
        
    def draw(self, screen):
        # Car body
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        # Car details
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 10, 30, 40))
        pygame.draw.rect(screen, WHITE, (self.x + 10, self.y + 15, 20, 30))
        
    def is_off_screen(self):
        return self.y > HEIGHT

# Game variables
player = PlayerCar()
enemies = []
score = 0
enemy_spawn_timer = 0
game_speed = 1
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    # Spawn enemies
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 60 // game_speed:
        enemies.append(EnemyCar())
        enemy_spawn_timer = 0
    
    # Update enemies
    for enemy in enemies[:]:
        enemy.move()
        if enemy.is_off_screen():
            enemies.remove(enemy)
            score += 10
    
    # Check collisions
    for enemy in enemies[:]:
        if (player.x < enemy.x + enemy.width and 
            player.x + player.width > enemy.x and
            player.y < enemy.y + enemy.height and
            player.y + player.height > enemy.y):
            running = False
    
    # Increase game speed
    if score > 0 and score % 100 == 0:
        game_speed += 0.1
    
    # Clear screen
    screen.fill(GREEN)  # Road background
    
    # Draw road lines
    for i in range(0, HEIGHT, 50):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i, 10, 30))
    
    # Draw game objects
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    speed_text = font.render(f"Speed: {game_speed:.1f}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 50))
    
    # Draw instructions
    instructions = font.render("Arrow keys: Move left/right", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
font = pygame.font.Font(None, 72)
game_over_text = font.render("GAME OVER", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
screen.blit(final_score_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
pygame.display.flip()

# Wait 3 seconds before closing
pygame.time.wait(3000)
pygame.quit()'''

def generate_adventure_game(prompt: str) -> str:
    return f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Game - {prompt[:50] if prompt else 'Custom Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Player
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 20
        self.speed = 5
        self.health = 100
        self.score = 0
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.size:
            self.y += self.speed
            
    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, self.y), self.size)

# Treasure
class Treasure:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.size = 15
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)
            
    def check_collision(self, player):
        if not self.collected:
            distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
            if distance < player.size + self.size:
                self.collected = True
                return True
        return False

# Enemy
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.size = 15
        self.speed = random.randint(1, 3)
        
    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)
        
    def check_collision(self, player):
        distance = ((player.x - self.x) ** 2 + (player.y - self.y) ** 2) ** 0.5
        return distance < player.size + self.size

# Game variables
player = Player()
treasures = [Treasure() for _ in range(5)]
enemies = [Enemy() for _ in range(3)]
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    # Update enemies
    for enemy in enemies:
        enemy.move_towards_player(player)
        if enemy.check_collision(player):
            player.health -= 10
            # Respawn enemy
            enemy.x = random.randint(0, WIDTH - 20)
            enemy.y = random.randint(0, HEIGHT - 20)
    
    # Check treasure collisions
    for treasure in treasures:
        if treasure.check_collision(player):
            player.score += 50
            player.health = min(100, player.health + 10)
    
    # Game over check
    if player.health <= 0:
        running = False
    
    # Clear screen
    screen.fill(GREEN)  # Grass background
    
    # Draw game objects
    player.draw(screen)
    for treasure in treasures:
        treasure.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player.score}", True, BLACK)
    health_text = font.render(f"Health: {player.health}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    
    # Draw instructions
    instructions = font.render("Arrow keys: Move, Collect yellow coins, Avoid red enemies", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

# Game over screen
screen.fill(BLACK)
font = pygame.font.Font(None, 72)
game_over_text = font.render("GAME OVER", True, RED)
final_score_text = font.render(f"Final Score: {player.score}", True, WHITE)
screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
screen.blit(final_score_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
pygame.display.flip()

# Wait 3 seconds before closing
pygame.time.wait(3000)
pygame.quit()'''

@app.post("/api/generate-game")
async def generate_game(request: dict):
    """Generate game code from prompt"""
    try:
        prompt = request.get("prompt", "Custom Game")
        
        # Generate appropriate game code based on prompt
        game_code = generate_game_code(prompt)
        
        return {
            "success": True,
            "code": game_code,
            "message": "Game generated successfully!"
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