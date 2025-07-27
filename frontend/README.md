# Vibr Frontend

The frontend application for the Vibr - Vibe Coding Playground platform.

## Features

- **Modern UI**: Built with Next.js 14, React 18, and Tailwind CSS
- **Responsive Design**: Mobile-first approach with beautiful animations
- **Game Creation**: Intuitive interface for creating games with AI
- **Game Management**: Dashboard for managing your games
- **Real-time Updates**: Live preview and iterative game updates
- **Asset Management**: Upload and manage game assets
- **Game Sharing**: Share games with other users

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Heroicons
- **Forms**: React Hook Form
- **Notifications**: React Hot Toast
- **HTTP Client**: Axios
- **Type Safety**: TypeScript

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Environment configuration**:
   Create a `.env.local` file in the frontend directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_APP_NAME=Vibr
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Dashboard page
│   └── create/            # Game creation pages
├── components/            # Reusable components
├── lib/                   # Utility functions
├── types/                 # TypeScript type definitions
├── public/                # Static assets
└── package.json           # Dependencies and scripts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Pages

### Dashboard (`/`)
- Overview of user's games
- Quick actions for creating, playing, and sharing games
- Modern grid layout with game cards

### Create Game (`/create`)
- AI-powered game creation interface
- Real-time code generation preview
- Game title and description input
- Save and play functionality

### Game Preview (`/game/[id]`)
- Live game preview with WebAssembly execution
- Chat interface for iterative updates
- Game controls and settings

### Asset Library (`/assets`)
- Upload and manage game assets
- Drag-and-drop file upload
- Asset tagging and organization

## Components

### UI Components
- `Button` - Reusable button component with variants
- `Card` - Card container component
- `Input` - Form input component
- `Modal` - Modal dialog component

### Game Components
- `GameCard` - Game preview card
- `GamePreview` - Game execution canvas
- `CodeEditor` - Code display and editing
- `ChatInterface` - AI interaction interface

## Styling

The application uses Tailwind CSS with custom design tokens:

- **Primary Colors**: Blue gradient for main actions
- **Secondary Colors**: Purple gradient for secondary actions
- **Typography**: Inter font for UI, JetBrains Mono for code
- **Animations**: Framer Motion for smooth transitions

## Development

### Code Style
- Use TypeScript for type safety
- Follow ESLint configuration
- Use Prettier for code formatting
- Write meaningful component names

### State Management
- Use React hooks for local state
- Consider Context API for global state
- Implement proper error boundaries

### Performance
- Use Next.js Image component for images
- Implement proper loading states
- Optimize bundle size with dynamic imports

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Configure environment variables
3. Deploy automatically on push

### Other Platforms
1. Build the application: `npm run build`
2. Start the production server: `npm run start`
3. Configure your hosting platform

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `Vibr` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Vibr platform.
