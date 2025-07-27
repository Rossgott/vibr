from sqlalchemy.orm import Session
from typing import List, Optional
import anthropic
import os
from dotenv import load_dotenv

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
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    async def generate_game_code(self, prompt: str) -> str:
        """Generate game code using Claude API"""
        system_prompt = """You are an expert game developer specializing in creating simple 2D games using Python and Pygame. 
        
        When given a game description, generate complete, runnable Python code that:
        1. Uses Pygame for graphics and input
        2. Creates a simple, fun 2D game
        3. Includes proper game loop, collision detection, and basic physics
        4. Has clear, well-commented code
        5. Is ready to run immediately
        
        The code should be self-contained and not require additional assets unless specifically mentioned.
        Focus on creating engaging, playable games that match the user's description."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Create a 2D game based on this description: {prompt}"
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"AI generation failed: {str(e)}")
    
    async def update_game_code(self, game_id: int, update_prompt: str, db: Session) -> str:
        """Update existing game code based on new prompt"""
        # Get current game code
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise Exception("Game not found")
        
        system_prompt = """You are an expert game developer. You will be given existing Python/Pygame code and a request to modify it.
        
        Your task is to:
        1. Understand the existing code structure
        2. Make the requested modifications
        3. Ensure the code remains functional and well-structured
        4. Preserve the core game mechanics while implementing the changes
        5. Return the complete updated code
        
        Always return the full, updated code, not just the changes."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Here's the current game code:\n\n{game.code}\n\nPlease modify it according to this request: {update_prompt}"
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"AI update failed: {str(e)}")

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
