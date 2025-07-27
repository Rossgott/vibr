'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function CreateGame() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [gameCode, setGameCode] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const generateGame = async () => {
    if (!prompt.trim()) {
      setError('Please enter a game description');
      return;
    }

    setIsGenerating(true);
    setError('');

    try {
      const response = await fetch('/api/generate-game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await response.json();

      if (data.success) {
        setGameCode(data.code);
      } else {
        setError(data.error || 'Failed to generate game');
      }
    } catch (err) {
      setError('Failed to connect to server');
    } finally {
      setIsGenerating(false);
    }
  };

  const saveGame = async () => {
    if (!gameCode) return;

    try {
      // For demo mode, we'll just show the code
      // In a full implementation, this would save to a database
      alert('Game saved! (Demo mode - code displayed below)');
    } catch (err) {
      setError('Failed to save game');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4">
              Create Your Game
            </h1>
            <p className="text-xl text-gray-300">
              Describe your game idea and watch AI bring it to life
            </p>
          </div>

          {/* Game Creation Form */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8">
            <div className="mb-6">
              <label htmlFor="prompt" className="block text-white text-lg font-semibold mb-3">
                Describe Your Game
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Create a space shooter game where the player controls a spaceship and shoots aliens. The player should move with arrow keys and shoot with spacebar. Include scoring and multiple levels."
                className="w-full h-32 p-4 bg-white/20 border border-white/30 rounded-lg text-white placeholder-gray-300 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-200">
                {error}
              </div>
            )}

            <div className="flex gap-4">
              <button
                onClick={generateGame}
                disabled={isGenerating}
                className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isGenerating ? 'Generating...' : 'Generate Game'}
              </button>
              <button
                onClick={() => router.push('/')}
                className="px-6 py-3 bg-white/20 hover:bg-white/30 text-white font-semibold rounded-lg transition-all duration-200"
              >
                Back to Home
              </button>
            </div>
          </div>

          {/* Generated Game Code */}
          {gameCode && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Generated Game Code</h2>
                <button
                  onClick={saveGame}
                  className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-all duration-200"
                >
                  Save Game
                </button>
              </div>
              
              <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                <pre className="text-green-400 text-sm whitespace-pre-wrap">
                  {gameCode}
                </pre>
              </div>
              
              <div className="mt-6 p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                <h3 className="text-white font-semibold mb-2">How to Play:</h3>
                <ul className="text-gray-300 space-y-1">
                  <li>• Copy the code above</li>
                  <li>• Save it as a .py file</li>
                  <li>• Install Pygame: pip install pygame</li>
                  <li>• Run: python your_game.py</li>
                  <li>• Use arrow keys to move the blue square</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
