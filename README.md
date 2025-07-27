# 🎮 Vibr - AI-Powered Game Creation Platform

**Create, save, and play games directly in your browser - no downloads required!**

Vibr is a revolutionary web platform that lets you create custom 2D games using natural language prompts. Simply describe your game idea, and watch as AI generates a complete, playable Python game right in your browser.

## ✨ Features

### 🚀 **Cloud-First Experience**
- **No Downloads Required**: Everything runs in your browser
- **Instant Game Creation**: Describe your game, get code instantly
- **Browser Preview**: See your game in action before downloading
- **Cross-Platform**: Works on any device with a web browser

### 🎯 **Smart Game Generation**
- **AI-Powered**: Uses advanced AI to understand your game descriptions
- **Multiple Game Types**: Space shooters, platformers, puzzle games, racing games, and more
- **Intelligent Detection**: Automatically determines game type from your description
- **Complete Code**: Generates full, runnable Python games with Pygame

### 💾 **Game Management**
- **Save Games**: Store your creations with custom names
- **Load Games**: Access your saved games anytime
- **Local Storage**: Games saved in your browser for privacy
- **Easy Sharing**: Download and share your games

### 🎮 **Game Types Supported**
- **Space Shooters**: "A space shooter with aliens and asteroids"
- **Platformers**: "A jumping platformer like Mario"
- **Puzzle Games**: "A color matching puzzle game"
- **Racing Games**: "A car racing game with obstacles"
- **Adventure Games**: "An adventure game with treasure hunting"

## 🌐 **Live Demo**

**Access Vibr right now:**
- **Frontend**: https://vibr-frontend.onrender.com
- **Backend**: https://vibr-backend.onrender.com

## 🚀 **Quick Start**

### **For Users (No Installation Required)**

1. **Visit the Website**: Go to https://vibr-frontend.onrender.com
2. **Describe Your Game**: Enter a detailed description of your game
3. **Generate**: Click "Generate Game" and watch the magic happen
4. **Preview**: See your game running in the browser
5. **Save**: Give your game a name and save it
6. **Download**: Get the Python file to run locally (optional)

### **Example Prompts**
- "Create a space shooter where I control a spaceship and shoot aliens"
- "Make a platformer where I jump between platforms and collect coins"
- "Design a puzzle game where I match colored tiles"
- "Build a racing game where I avoid obstacles on the road"

## 🛠️ **For Developers**

### **Prerequisites**
- Python 3.8+
- Node.js 18+ (for frontend development)
- Git

### **Local Development Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rossgott/vibr.git
   cd vibr
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements-minimal.txt
   python main-minimal.py
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the app**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## 🏗️ **Architecture**

### **Frontend (Next.js 14)**
- **Framework**: Next.js with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Features**: 
  - Game creation interface
  - Browser-based game preview
  - Local game storage
  - Responsive design

### **Backend (FastAPI)**
- **Framework**: FastAPI
- **Language**: Python
- **Features**:
  - AI-powered game generation
  - Multiple game type support
  - RESTful API
  - CORS enabled

### **Game Generation**
- **Engine**: Pygame
- **Types**: Space shooters, platformers, puzzle games, racing games, adventure games
- **Output**: Complete, runnable Python code

## 🎮 **How It Works**

1. **User Input**: User describes their game idea in natural language
2. **AI Processing**: Backend analyzes the prompt and determines game type
3. **Code Generation**: AI generates complete Pygame code based on the description
4. **Browser Preview**: Frontend shows a preview of the game mechanics
5. **Save & Share**: User can save the game and download the Python file

## 🔧 **API Endpoints**

### **Health Check**
```
GET /health
```

### **Game Generation**
```
POST /api/generate-game
Content-Type: application/json

{
  "prompt": "Create a space shooter game"
}
```

## 🎯 **Game Types & Keywords**

The system automatically detects game types based on keywords:

- **Space Shooter**: `space`, `shooter`, `alien`, `spaceship`, `asteroid`
- **Platformer**: `platform`, `jump`, `mario`, `runner`
- **Puzzle**: `puzzle`, `match`, `connect`, `block`
- **Racing**: `racing`, `car`, `drive`, `speed`
- **Adventure**: Default for other descriptions

## 🌟 **Why Vibr?**

### **For Users**
- **No Technical Knowledge Required**: Just describe what you want
- **Instant Gratification**: See your game idea come to life immediately
- **Educational**: Learn about game development through generated code
- **Creative Freedom**: Endless possibilities with natural language

### **For Educators**
- **Teaching Tool**: Great for introducing programming concepts
- **Student Engagement**: Visual, interactive way to learn coding
- **Project-Based Learning**: Students can create and modify games

### **For Developers**
- **Rapid Prototyping**: Quickly test game ideas
- **Code Examples**: Study generated code for learning
- **Extensible**: Easy to add new game types and features

## 🚀 **Deployment**

### **Cloud Deployment (Recommended)**
The app is designed for cloud deployment with:
- **Render**: Backend and frontend hosting
- **Vercel**: Alternative frontend hosting
- **Railway**: Alternative backend hosting

### **Local Deployment**
See the developer setup section above for local development.

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### **Areas for Contribution**
- New game types
- Improved AI prompts
- Better browser preview
- Enhanced UI/UX
- Performance optimizations

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Pygame**: For the game development framework
- **FastAPI**: For the robust backend API
- **Next.js**: For the modern frontend framework
- **Tailwind CSS**: For the beautiful styling

## 📞 **Support**

- **Issues**: [GitHub Issues](https://github.com/Rossgott/vibr/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Rossgott/vibr/discussions)
- **Email**: [Your Email]

---

**Ready to create your first game? Visit [Vibr](https://vibr-frontend.onrender.com) and start building!** 🎮✨
