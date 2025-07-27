'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeftIcon, SparklesIcon, PlayIcon, SaveIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'
import toast from 'react-hot-toast'

export default function CreateGame() {
  const [prompt, setPrompt] = useState('')
  const [gameTitle, setGameTitle] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedCode, setGeneratedCode] = useState('')
  const [gamePreview, setGamePreview] = useState('')

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a game description')
      return
    }

    setIsGenerating(true)
    toast.loading('Generating your game...')

    try {
      // TODO: Call AI API
      // For now, simulate API call
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      const mockCode = `import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("${gameTitle || 'My Game'}")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game variables
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_speed = 5
score = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
        player_x += player_speed
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()`

      setGeneratedCode(mockCode)
      toast.success('Game generated successfully!')
    } catch (error) {
      toast.error('Failed to generate game. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleSave = async () => {
    if (!gameTitle.trim()) {
      toast.error('Please enter a game title')
      return
    }

    if (!generatedCode) {
      toast.error('No game code to save')
      return
    }

    try {
      // TODO: Save game to backend
      toast.success('Game saved successfully!')
    } catch (error) {
      toast.error('Failed to save game')
    }
  }

  const handlePlay = () => {
    if (!generatedCode) {
      toast.error('No game to play')
      return
    }

    // TODO: Implement game preview/play functionality
    toast.success('Game preview coming soon!')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center py-6">
            <Link href="/" className="btn-secondary mr-4">
              <ArrowLeftIcon className="h-5 w-5 mr-2" />
              Back
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Create New Game</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Game Creation */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-6"
          >
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Game Details</h2>
              <div className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                    Game Title
                  </label>
                  <input
                    type="text"
                    id="title"
                    value={gameTitle}
                    onChange={(e) => setGameTitle(e.target.value)}
                    placeholder="Enter game title..."
                    className="input-field"
                  />
                </div>
              </div>
            </div>

            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Describe Your Game</h2>
              <div className="space-y-4">
                <div>
                  <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
                    Game Description
                  </label>
                  <textarea
                    id="prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe your game idea in detail. For example: 'Create a space shooter game where the player controls a spaceship and shoots aliens. The player should move with arrow keys and shoot with spacebar. Include scoring and multiple levels.'"
                    rows={6}
                    className="input-field"
                  />
                </div>
                <button
                  onClick={handleGenerate}
                  disabled={isGenerating || !prompt.trim()}
                  className="btn-primary w-full flex items-center justify-center"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <SparklesIcon className="h-5 w-5 mr-2" />
                      Generate Game
                    </>
                  )}
                </button>
              </div>
            </div>

            {generatedCode && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="card"
              >
                <h2 className="text-xl font-semibold mb-4">Game Actions</h2>
                <div className="flex space-x-4">
                  <button
                    onClick={handlePlay}
                    className="btn-primary flex-1 flex items-center justify-center"
                  >
                    <PlayIcon className="h-5 w-5 mr-2" />
                    Play Game
                  </button>
                  <button
                    onClick={handleSave}
                    className="btn-secondary flex-1 flex items-center justify-center"
                  >
                    <SaveIcon className="h-5 w-5 mr-2" />
                    Save Game
                  </button>
                </div>
              </motion.div>
            )}
          </motion.div>

          {/* Right Panel - Code Preview */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-6"
          >
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Generated Code</h2>
              {generatedCode ? (
                <div className="bg-gray-900 rounded-lg p-4 overflow-auto max-h-96">
                  <pre className="text-green-400 text-sm font-mono">
                    <code>{generatedCode}</code>
                  </pre>
                </div>
              ) : (
                <div className="bg-gray-100 rounded-lg p-8 text-center">
                  <SparklesIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600">
                    Enter a game description and click "Generate Game" to see the code here.
                  </p>
                </div>
              )}
            </div>

            {generatedCode && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="card"
              >
                <h2 className="text-xl font-semibold mb-4">Game Preview</h2>
                <div className="bg-gray-900 rounded-lg p-4 h-64 flex items-center justify-center">
                  <div className="text-center text-gray-400">
                    <PlayIcon className="h-12 w-12 mx-auto mb-2" />
                    <p>Game preview will be available here</p>
                  </div>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  )
}
