from sqlalchemy.orm import Session
from typing import List, Optional
import anthropic
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

from models import User, Game, Asset, GameShare
from schemas import UserCreate, GameCreate, GameUpdate, AssetCreate
from auth import get_password_hash, verify_password

load_dotenv()

class UserService:
    def create_user(self, db: Session, user: UserCreate) -> User:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.username == user.username)
        ).first()
        if existing_user:
            raise ValueError("User with this email or username already exists")
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

class GameService:
    def create_game(self, db: Session, game: GameCreate, owner_id: int) -> Game:
        db_game = Game(
            title=game.title,
            description=game.description,
            prompt=game.prompt,
            code=game.code,
            is_public=game.is_public,
            metadata=game.metadata,
            owner_id=owner_id
        )
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game
    
    def get_user_games(self, db: Session, user_id: int) -> List[Game]:
        return db.query(Game).filter(Game.owner_id == user_id).all()
    
    def get_game(self, db: Session, game_id: int, user_id: int) -> Optional[Game]:
        return db.query(Game).filter(
            Game.id == game_id,
            Game.owner_id == user_id
        ).first()
    
    def update_game(self, db: Session, game_id: int, game_update: GameUpdate, user_id: int) -> Optional[Game]:
        db_game = self.get_game(db, game_id, user_id)
        if not db_game:
            return None
        
        update_data = game_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_game, field, value)
        
        # Increment version
        db_game.version += 1
        
        db.commit()
        db.refresh(db_game)
        return db_game
    
    def delete_game(self, db: Session, game_id: int, user_id: int) -> bool:
        db_game = self.get_game(db, game_id, user_id)
        if not db_game:
            return False
        
        db.delete(db_game)
        db.commit()
        return True
    
    def share_game(self, db: Session, game_id: int, shared_with_email: str, can_edit: bool, user_id: int) -> Optional[GameShare]:
        # Verify game ownership
        game = self.get_game(db, game_id, user_id)
        if not game:
            return None
        
        # Create share record
        share = GameShare(
            game_id=game_id,
            shared_with_email=shared_with_email,
            can_edit=can_edit
        )
        db.add(share)
        db.commit()
        db.refresh(share)
        return share

class AIService:
    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        self.use_fallback = False
        
        # Try to initialize Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                print("✅ Anthropic API initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Anthropic: {e}")
        
        # Try to initialize OpenAI as fallback
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
                print("✅ OpenAI API initialized as fallback")
            except Exception as e:
                print(f"❌ Failed to initialize OpenAI: {e}")
        
        # If no AI providers available, use fallback mode
        if not self.anthropic_client and not self.openai_client:
            self.use_fallback = True
            print("⚠️ No AI API keys found - using fallback mode")

    def generate_game_code(self, prompt: str) -> str:
        """Generate game code from natural language prompt"""
        
        if self.anthropic_client:
            return self._generate_with_anthropic(prompt)
        elif self.openai_client:
            return self._generate_with_openai(prompt)
        else:
            return self._generate_fallback(prompt)

    def _generate_with_anthropic(self, prompt: str) -> str:
        """Generate using Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert game developer who creates Python/Pygame games from natural language descriptions. 
                        Generate complete, runnable game code that includes:
                        - All necessary imports
                        - Game initialization
                        - Main game loop
                        - Player controls
                        - Game mechanics
                        - Basic graphics and sound
                        
                        Return ONLY the Python code, no explanations."""
                    },
                    {
                        "role": "user",
                        "content": f"Create a 2D game based on this description: {prompt}"
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            if self.openai_client:
                return self._generate_with_openai(prompt)
            else:
                return self._generate_fallback(prompt)

    def _generate_with_openai(self, prompt: str) -> str:
        """Generate using OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                max_tokens=4000,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert game developer who creates Python/Pygame games from natural language descriptions. 
                        Generate complete, runnable game code that includes:
                        - All necessary imports
                        - Game initialization
                        - Main game loop
                        - Player controls
                        - Game mechanics
                        - Basic graphics and sound
                        
                        Return ONLY the Python code, no explanations."""
                    },
                    {
                        "role": "user",
                        "content": f"Create a 2D game based on this description: {prompt}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._generate_fallback(prompt)

    def _generate_fallback(self, prompt: str) -> str:
        """Generate a simple fallback game when no AI is available"""
        return f'''import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vibr Game - {prompt[:50]}...")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

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
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

    def update_game_code(self, existing_code: str, update_prompt: str) -> str:
        """Update existing game code based on new prompt"""
        
        if self.anthropic_client:
            return self._update_with_anthropic(existing_code, update_prompt)
        elif self.openai_client:
            return self._update_with_openai(existing_code, update_prompt)
        else:
            return self._update_fallback(existing_code, update_prompt)

    def _update_with_anthropic(self, existing_code: str, update_prompt: str) -> str:
        """Update using Anthropic Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert game developer. Update the provided Python/Pygame game code based on the user's request.
                        Return ONLY the updated Python code, no explanations."""
                    },
                    {
                        "role": "user",
                        "content": f"Here's the current game code:\n\n{existing_code}\n\nUpdate it based on this request: {update_prompt}"
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            if self.openai_client:
                return self._update_with_openai(existing_code, update_prompt)
            else:
                return self._update_fallback(existing_code, update_prompt)

    def _update_with_openai(self, existing_code: str, update_prompt: str) -> str:
        """Update using OpenAI GPT"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                max_tokens=4000,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert game developer. Update the provided Python/Pygame game code based on the user's request.
                        Return ONLY the updated Python code, no explanations."""
                    },
                    {
                        "role": "user",
                        "content": f"Here's the current game code:\n\n{existing_code}\n\nUpdate it based on this request: {update_prompt}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._update_fallback(existing_code, update_prompt)

    def _update_fallback(self, existing_code: str, update_prompt: str) -> str:
        """Fallback update - just return the original code with a comment"""
        return f'''# Updated based on: {update_prompt}
# Note: AI features are disabled. This is the original game code.

{existing_code}'''

class AssetService:
    def create_asset(self, db: Session, asset: AssetCreate, owner_id: int) -> Asset:
        db_asset = Asset(
            filename=asset.filename,
            original_filename=asset.original_filename,
            file_url=asset.file_url,
            file_type=asset.file_type,
            file_size=asset.file_size,
            tags=asset.tags,
            owner_id=owner_id
        )
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    
    def get_user_assets(self, db: Session, user_id: int) -> List[Asset]:
        return db.query(Asset).filter(Asset.owner_id == user_id).all()
    
    def get_asset(self, db: Session, asset_id: int, user_id: int) -> Optional[Asset]:
        return db.query(Asset).filter(
            Asset.id == asset_id,
            Asset.owner_id == user_id
        ).first()
