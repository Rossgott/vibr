from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db, engine
import models
import schemas
import services
import auth

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vibr API",
    description="AI-powered game creation platform",
    version="1.0.0"
)

# Get allowed origins from environment or use defaults
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://vibr.vercel.app,https://vibr-frontend.vercel.app").split(",")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Services
game_service = services.GameService()
user_service = services.UserService()
ai_service = services.AIService()

@app.get("/health")
async def health_check():
    """Health check endpoint for cloud deployment"""
    return {"status": "healthy", "message": "Vibr API is running", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Welcome to Vibr API", "docs": "/docs"}

# User endpoints
@app.post("/auth/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@app.post("/auth/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Game endpoints
@app.post("/games", response_model=schemas.GameResponse)
async def create_game(
    game: schemas.GameCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    return game_service.create_game(db, game, current_user.id)

@app.get("/games", response_model=List[schemas.GameResponse])
async def get_games(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    return game_service.get_user_games(db, current_user.id)

@app.get("/games/{game_id}", response_model=schemas.GameResponse)
async def get_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    game = game_service.get_game(db, game_id, current_user.id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.put("/games/{game_id}", response_model=schemas.GameResponse)
async def update_game(
    game_id: int,
    game: schemas.GameUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    updated_game = game_service.update_game(db, game_id, game, current_user.id)
    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return updated_game

@app.delete("/games/{game_id}")
async def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    success = game_service.delete_game(db, game_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game deleted successfully"}

# AI endpoints
@app.post("/ai/generate-game")
async def generate_game_code(
    prompt: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    try:
        game_code = await ai_service.generate_game_code(prompt)
        return {"code": game_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@app.post("/ai/update-game")
async def update_game_code(
    game_id: int,
    update_prompt: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    try:
        updated_code = await ai_service.update_game_code(game_id, update_prompt, db)
        return {"code": updated_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI update failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
