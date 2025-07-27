'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { PlusIcon, PlayIcon, PencilIcon, ShareIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface Game {
  id: number
  title: string
  description: string
  thumbnail_url?: string
  created_at: string
}

export default function Dashboard() {
  const [games, setGames] = useState<Game[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // TODO: Fetch games from API
    // For now, using mock data
    setTimeout(() => {
      setGames([
        {
          id: 1,
          title: "Space Invaders",
          description: "Classic space shooter game with aliens",
          created_at: "2024-01-15T10:30:00Z"
        },
        {
          id: 2,
          title: "Snake Game",
          description: "Grow your snake by eating food",
          created_at: "2024-01-14T15:45:00Z"
        }
      ])
      setLoading(false)
    }, 1000)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gradient">
                Vibr
              </h1>
              <span className="ml-2 text-sm text-gray-500">Vibe Coding Playground</span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="btn-secondary">
                <ShareIcon className="h-5 w-5 mr-2" />
                Share
              </button>
              <button className="btn-primary">
                <PlusIcon className="h-5 w-5 mr-2" />
                Create New Game
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Create Amazing Games with AI
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Describe your game idea in plain English and watch as AI generates a complete, 
            playable 2D game for you. No coding experience required!
          </p>
        </motion.div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="card text-center hover:shadow-lg transition-shadow duration-300"
          >
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <PlusIcon className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Create Game</h3>
            <p className="text-gray-600 mb-4">
              Start with a simple description and let AI build your game
            </p>
            <Link href="/create" className="btn-primary">
              Get Started
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="card text-center hover:shadow-lg transition-shadow duration-300"
          >
            <div className="w-16 h-16 bg-secondary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <PlayIcon className="h-8 w-8 text-secondary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Play Games</h3>
            <p className="text-gray-600 mb-4">
              Try out games created by the community
            </p>
            <Link href="/explore" className="btn-secondary">
              Explore
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="card text-center hover:shadow-lg transition-shadow duration-300"
          >
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <ShareIcon className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Share & Collaborate</h3>
            <p className="text-gray-600 mb-4">
              Share your games and collaborate with others
            </p>
            <Link href="/share" className="btn-secondary">
              Share
            </Link>
          </motion.div>
        </div>

        {/* My Games Section */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold text-gray-900">My Games</h3>
            <Link href="/create" className="btn-primary">
              <PlusIcon className="h-5 w-5 mr-2" />
              New Game
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="game-card animate-pulse">
                  <div className="h-32 bg-gray-200 rounded-lg mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                </div>
              ))}
            </div>
          ) : games.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <PlusIcon className="h-12 w-12 text-gray-400" />
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">
                No games yet
              </h4>
              <p className="text-gray-600 mb-6">
                Create your first game to get started!
              </p>
              <Link href="/create" className="btn-primary">
                Create Your First Game
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {games.map((game) => (
                <motion.div
                  key={game.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3 }}
                  className="game-card group"
                >
                  <div className="h-32 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-lg mb-4 flex items-center justify-center">
                    <PlayIcon className="h-12 w-12 text-primary-600 opacity-50 group-hover:opacity-75 transition-opacity" />
                  </div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-2">
                    {game.title}
                  </h4>
                  <p className="text-gray-600 text-sm mb-4">
                    {game.description}
                  </p>
                  <div className="flex space-x-2">
                    <button className="flex-1 btn-primary text-sm py-1">
                      <PlayIcon className="h-4 w-4 mr-1" />
                      Play
                    </button>
                    <button className="btn-secondary text-sm py-1 px-3">
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button className="btn-secondary text-sm py-1 px-3">
                      <ShareIcon className="h-4 w-4" />
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
