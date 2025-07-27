# Vibr - Vibe Coding Playground

An AI-powered platform that enables anyone—technical or non-technical—to create, customize, and play simple 2D games using natural language prompts directly in a browser.

## 🎮 Features

- **AI-Powered Game Creation**: Describe your game idea in plain English and watch AI generate complete, playable 2D games
- **Real-time Preview**: See your game come to life instantly with live preview
- **Iterative Updates**: Make changes through natural language and see immediate updates
- **Asset Management**: Upload and manage custom game assets
- **Game Sharing**: Share your creations with friends and collaborate
- **No Coding Required**: Perfect for beginners and non-technical users
- **Modern UI**: Beautiful, responsive interface built with modern web technologies
- **Access Anywhere**: Works on computers, tablets, and smartphones

## 🌐 Access Vibr

**Vibr is now live in the cloud!** You can access it from any device:

- **🌍 Live Demo**: [https://vibr.vercel.app](https://vibr.vercel.app)
- **📱 Mobile Friendly**: Works perfectly on smartphones and tablets
- **💻 Desktop Ready**: Optimized for computers and laptops
- **🏫 School Safe**: No downloads or installations required

## 🚀 How to Use

1. **Open your browser** on any device (computer, phone, tablet)
2. **Visit** [https://vibr.vercel.app](https://vibr.vercel.app)
3. **Start creating games** with natural language descriptions
4. **Share your creations** with friends and family

### Example Game Descriptions

- "Create a space shooter game where the player controls a spaceship and shoots aliens. The player should move with arrow keys and shoot with spacebar. Include scoring and multiple levels."
- "Make a simple platformer game with a character that can jump and collect coins. The character should be able to double jump and there should be obstacles to avoid."
- "Build a puzzle game where players need to match colored blocks. Include a timer and score system with increasing difficulty levels."

## 🤖 AI Options

Vibr supports multiple AI providers for game generation:

### **Option 1: Anthropic Claude (Recommended)**
- **Best for**: High-quality, creative game generation
- **Cost**: ~$0.01-0.05 per game generation
- **Setup**: Get API key from [console.anthropic.com](https://console.anthropic.com)

### **Option 2: OpenAI GPT-4**
- **Best for**: Reliable, consistent game generation
- **Cost**: ~$0.02-0.10 per game generation
- **Setup**: Get API key from [platform.openai.com](https://platform.openai.com)

### **Option 3: No AI (Demo Mode)**
- **Best for**: Testing and demonstration
- **Cost**: Free
- **Features**: Basic template games, no custom generation
- **Setup**: Deploy without any API keys

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 with App Router
- **UI**: React 18 + Tailwind CSS
- **Animations**: Framer Motion
- **Type Safety**: TypeScript
- **Deployment**: Vercel (global CDN)

### Backend
- **API**: FastAPI (Python)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT tokens
- **AI Integration**: Anthropic Claude API / OpenAI GPT-4
- **Storage**: AWS S3 for assets
- **Deployment**: Railway

### Game Execution
- **Runtime**: WebAssembly (Pyodide)
- **Framework**: Pygame for 2D games
- **Sandbox**: Secure containerized execution

## 🔧 For Developers

### Quick Deploy (No Local Setup Required)

The easiest way to deploy your own instance:

#### **Option A: With AI (Full Features)**
1. **Fork this repository** to your GitHub account
2. **Get AI API key** (Anthropic or OpenAI)
3. **Deploy to Railway** (Backend):
   - Visit [Railway](https://railway.app/)
   - Connect your GitHub repo
   - Add environment variables:
     - `ANTHROPIC_API_KEY`: Your Anthropic API key (or)
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `SECRET_KEY`: A secure random string
4. **Deploy to Vercel** (Frontend):
   - Visit [Vercel](https://vercel.com/)
   - Import your GitHub repo
   - Set environment variable:
     - `NEXT_PUBLIC_API_URL`: Your Railway backend URL

#### **Option B: Without AI (Demo Mode)**
1. **Fork this repository** to your GitHub account
2. **Deploy to Railway** (Backend):
   - Visit [Railway](https://railway.app/)
   - Connect your GitHub repo
   - Add environment variable:
     - `SECRET_KEY`: A secure random string
   - **No AI API key needed** - will use fallback mode
3. **Deploy to Vercel** (Frontend):
   - Visit [Vercel](https://vercel.com/)
   - Import your GitHub repo
   - Set environment variable:
     - `NEXT_PUBLIC_API_URL`: Your Railway backend URL

### Local Development (Optional)

If you want to run locally for development:

```bash
# Clone the repository
git clone <repository-url>
cd vibr

# Backend setup
cd backend
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
python main.py

# Frontend setup (in new terminal)
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## 📁 Project Structure

```
vibr/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── services.py         # Business logic
│   ├── auth.py             # Authentication
│   ├── database.py         # Database configuration
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/                # Next.js App Router
│   ├── components/         # React components
│   ├── lib/                # Utility functions
│   ├── types/              # TypeScript types
│   └── package.json        # Node.js dependencies
├── .github/workflows/      # GitHub Actions for deployment
├── railway.json            # Railway deployment config
├── render.yaml             # Render deployment config
├── vercel.json             # Vercel deployment config
└── README.md              # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Games
- `GET /games` - Get user's games
- `POST /games` - Create new game
- `GET /games/{id}` - Get specific game
- `PUT /games/{id}` - Update game
- `DELETE /games/{id}` - Delete game

### AI
- `POST /ai/generate-game` - Generate game code from prompt
- `POST /ai/update-game` - Update existing game code

### Assets
- `GET /assets` - Get user's assets
- `POST /assets` - Upload new asset

## 🛠️ Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
cd backend
black .
isort .

# Frontend
cd frontend
npm run lint
npm run format
```

## 🚀 Deployment

### Automatic Deployment

The project is configured for automatic deployment:

- **Frontend**: Automatically deploys to Vercel on push to main
- **Backend**: Automatically deploys to Railway on push to main
- **Database**: PostgreSQL on Railway
- **CDN**: Vercel Edge Network for global performance

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to various platforms.

## 🔒 Security

- **HTTPS**: All connections are encrypted
- **CORS**: Properly configured for production domains
- **Authentication**: JWT-based secure authentication
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: API endpoints are rate-limited

## 📊 Performance

- **Global CDN**: Vercel Edge Network for fast loading worldwide
- **Optimized Images**: Next.js Image optimization
- **Code Splitting**: Automatic code splitting for faster loads
- **Caching**: Intelligent caching strategies
- **Mobile Optimized**: Responsive design for all devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com/) for Claude AI API
- [OpenAI](https://openai.com/) for GPT-4 API
- [Pygame](https://www.pygame.org/) for 2D game development
- [Next.js](https://nextjs.org/) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Vercel](https://vercel.com/) for hosting and CDN
- [Railway](https://railway.app/) for backend hosting

## 📞 Support

For support, email support@vibr.dev or join our Discord community.

---

**Vibr** - Making game development accessible to everyone, everywhere! 🎮✨
