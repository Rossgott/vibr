from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Game schemas
class GameBase(BaseModel):
    title: str
    description: Optional[str] = None
    prompt: str
    is_public: bool = False

class GameCreate(GameBase):
    code: str
    metadata: Optional[Dict[str, Any]] = None

class GameUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None
    is_public: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class GameResponse(GameBase):
    id: int
    code: str
    thumbnail_url: Optional[str] = None
    version: int
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int
    
    class Config:
        from_attributes = True

# Asset schemas
class AssetBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    tags: Optional[List[str]] = None

class AssetCreate(AssetBase):
    file_url: str
    file_size: int

class AssetResponse(AssetBase):
    id: int
    file_url: str
    file_size: int
    created_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True

# Game Share schemas
class GameShareCreate(BaseModel):
    game_id: int
    shared_with_email: EmailStr
    can_edit: bool = False

class GameShareResponse(BaseModel):
    id: int
    game_id: int
    shared_with_email: str
    can_edit: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# AI Generation schemas
class GameGenerationRequest(BaseModel):
    prompt: str
    game_type: Optional[str] = "2d"  # 2d, 3d, etc.
    framework: Optional[str] = "pygame"  # pygame, p5.js, etc.

class GameUpdateRequest(BaseModel):
    game_id: int
    update_prompt: str
    current_code: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
