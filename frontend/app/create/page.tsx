'use client';

import { useState, useEffect, useRef } from 'react';

interface Game {
  id: string;
  name: string;
  code: string;
  prompt: string;
  createdAt: string;
}

export default function CreatePage() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCode, setGeneratedCode] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [gameName, setGameName] = useState('');
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [savedGames, setSavedGames] = useState<Game[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const gameIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Load saved games from localStorage on component mount
  useEffect(() => {
    const saved = localStorage.getItem('vibr-saved-games');
    if (saved) {
      setSavedGames(JSON.parse(saved));
    }
  }, []);

  const generateGame = async () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'https://vibr-backend.onrender.com';
      const response = await fetch(`${backendUrl}/api/generate-game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();
      if (data.success) {
        setGeneratedCode(data.code);
        // Auto-generate a game name from the prompt
        const autoName = prompt.split(' ').slice(0, 3).join(' ').substring(0, 30);
        setGameName(autoName);
      } else {
        alert('Failed to generate game: ' + data.message);
      }
    } catch (err) {
      console.error('Error generating game:', err);
      alert('Failed to connect to game generation service');
    } finally {
      setIsGenerating(false);
    }
  };

  const playGame = () => {
    if (!canvasRef.current) return;

    setIsPlaying(true);
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Simple browser-based game simulation
    let playerX = canvas.width / 2;
    let playerY = canvas.height / 2;
    const playerSpeed = 5;
    let frameCount = 0;

    const gameLoop = () => {
      if (!isPlaying || frameCount > 300) {
        setIsPlaying(false);
        return;
      }

      // Clear canvas
      ctx.fillStyle = 'white';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw player
      ctx.fillStyle = 'blue';
      ctx.fillRect(playerX, playerY, 50, 50);

      // Draw instructions
      ctx.fillStyle = 'black';
      ctx.font = '24px Arial';
      ctx.fillText('Browser Game Preview', 10, 30);
      ctx.fillText('Use arrow keys to move', 10, 60);
      ctx.fillText('Click "Play Full Game" to download', 10, 90);

      // Simulate some movement
      playerX += Math.sin(frameCount * 0.1) * 2;
      playerY += Math.cos(frameCount * 0.1) * 2;

      // Keep player on screen
      playerX = Math.max(0, Math.min(canvas.width - 50, playerX));
      playerY = Math.max(0, Math.min(canvas.height - 50, playerY));

      frameCount++;
      requestAnimationFrame(gameLoop);
    };

    gameLoop();
  };

  const stopGame = () => {
    setIsPlaying(false);
    if (gameIntervalRef.current) {
      clearInterval(gameIntervalRef.current);
      gameIntervalRef.current = null;
    }
  };

  const downloadGame = () => {
    if (!generatedCode) return;

    const blob = new Blob([generatedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${gameName || 'vibr-game'}.py`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const saveGame = () => {
    if (!gameName.trim() || !generatedCode) return;

    const newGame: Game = {
      id: Date.now().toString(),
      name: gameName.trim(),
      code: generatedCode,
      prompt: prompt,
      createdAt: new Date().toISOString(),
    };

    const updatedGames = [...savedGames, newGame];
    setSavedGames(updatedGames);
    localStorage.setItem('vibr-saved-games', JSON.stringify(updatedGames));
    setShowSaveDialog(false);
    setGameName('');
  };

  const loadGame = (game: Game) => {
    setGeneratedCode(game.code);
    setPrompt(game.prompt);
    setGameName(game.name);
  };

  const deleteGame = (gameId: string) => {
    const updatedGames = savedGames.filter(game => game.id !== gameId);
    setSavedGames(updatedGames);
    localStorage.setItem('vibr-saved-games', JSON.stringify(updatedGames));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            🎮 Create Your Game
          </h1>

          {/* Game Creation Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Input Section */}
            <div className="space-y-6">
              <div>
                <label className="block text-white text-lg font-semibold mb-3">
                  Describe Your Game
                </label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="e.g., A space shooter where you control a spaceship and shoot asteroids..."
                  className="w-full h-32 p-4 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 resize-none focus:outline-none focus:ring-2 focus:ring-purple-400"
                />
              </div>

              <button
                onClick={generateGame}
                disabled={isGenerating || !prompt.trim()}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-4 px-6 rounded-xl font-semibold text-lg disabled:opacity-50 disabled:cursor-not-allowed hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
              >
                {isGenerating ? '🎮 Generating Game...' : '🚀 Generate Game'}
              </button>

              {generatedCode && (
                <button
                  onClick={() => setShowSaveDialog(true)}
                  className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-green-700 hover:to-emerald-700 transition-all duration-200"
                >
                  💾 Save Game
                </button>
              )}
            </div>

            {/* Game Display Section */}
            <div className="space-y-6">
              <div>
                <label className="block text-white text-lg font-semibold mb-3">
                  Generated Game Code
                </label>
                <div className="bg-gray-900 rounded-xl p-4 h-64 overflow-auto">
                  <pre className="text-green-400 text-sm whitespace-pre-wrap">
                    {generatedCode || 'Your game code will appear here...'}
                  </pre>
                </div>
              </div>

              {generatedCode && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-white text-lg font-semibold mb-3">
                      🎮 Game Preview
                    </label>
                    <div className="bg-black rounded-xl overflow-hidden">
                      <canvas
                        ref={canvasRef}
                        width={800}
                        height={600}
                        className="w-full h-auto"
                      />
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <button
                      onClick={playGame}
                      disabled={isPlaying}
                      className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 px-6 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-green-700 hover:to-emerald-700 transition-all duration-200"
                    >
                      {isPlaying ? '⏸️ Stop' : '▶️ Preview'}
                    </button>

                    <button
                      onClick={downloadGame}
                      className="flex-1 bg-gradient-to-r from-orange-600 to-red-600 text-white py-3 px-6 rounded-xl font-semibold hover:from-orange-700 hover:to-red-700 transition-all duration-200"
                    >
                      📥 Download
                    </button>
                  </div>

                  <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4">
                    <h3 className="text-white font-semibold mb-2">How to Play:</h3>
                    <ul className="text-gray-300 space-y-1 text-sm">
                      <li>• Click "Download" to get the Python file</li>
                      <li>• Install Python and Pygame: <code className="bg-gray-800 px-1 rounded">pip install pygame</code></li>
                      <li>• Run: <code className="bg-gray-800 px-1 rounded">python your-game.py</code></li>
                      <li>• Use arrow keys to control the game</li>
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Saved Games Section */}
          {savedGames.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold text-white mb-6">💾 Saved Games</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {savedGames.map((game) => (
                  <div
                    key={game.id}
                    className="bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-white/20"
                  >
                    <h3 className="text-white font-semibold text-lg mb-2">{game.name}</h3>
                    <p className="text-white/70 text-sm mb-3 line-clamp-2">{game.prompt}</p>
                    <p className="text-white/50 text-xs mb-4">
                      {new Date(game.createdAt).toLocaleDateString()}
                    </p>
                    <div className="flex gap-2">
                      <button
                        onClick={() => loadGame(game)}
                        className="flex-1 bg-blue-600 text-white py-2 px-3 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                      >
                        📂 Load
                      </button>
                      <button
                        onClick={() => deleteGame(game.id)}
                        className="bg-red-600 text-white py-2 px-3 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Save Game Dialog */}
      {showSaveDialog && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Save Your Game</h3>
            <input
              type="text"
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              placeholder="Enter game name..."
              className="w-full p-3 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-purple-400"
            />
            <div className="flex gap-3">
              <button
                onClick={saveGame}
                disabled={!gameName.trim()}
                className="flex-1 bg-purple-600 text-white py-2 px-4 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-purple-700 transition-colors"
              >
                Save
              </button>
              <button
                onClick={() => setShowSaveDialog(false)}
                className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
