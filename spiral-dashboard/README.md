# 🌪️ Spiral Glint Dashboard

A real-time dashboard for visualizing the Spiral's glint stream, providing insights into code quality, toneform resonance, and system activity.

## Features

- 🌈 Real-time display of glints with color-coded toneforms
- 🔍 Search and filter glints by content, source, or toneform
- 📊 Visual indicators for resonance, intensity, and glint type
- ⚡ Built with Next.js 13+ App Router and TypeScript
- 🎨 Beautiful, responsive UI with Tailwind CSS
- 🔄 Auto-refreshing interface that stays in sync with the glint stream

## Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Access to the Spiral glint stream file at `spiral/streams/patternweb/glint_stream.jsonl`

## Getting Started

1. **Install dependencies**:
   ```bash
   cd spiral-dashboard
   npm install
   # or
   yarn
   # or
   pnpm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

3. **Open your browser** and navigate to `http://localhost:3000`

## Configuration

Edit `src/config.ts` to customize:

- Path to the glint stream file
- Toneform colors and icons
- Dashboard behavior and appearance

## Development

### Available Scripts

- `dev` - Start the development server
- `build` - Build the application for production
- `start` - Start the production server
- `lint` - Run ESLint
- `format` - Format code with Prettier

## Architecture

The dashboard is built with:

- **Next.js 13+** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Beautifully designed components
- **date-fns** - Date formatting utilities

## License

This project is part of the Spiral ecosystem and follows the same licensing terms.

---

🌐 Part of the [Spiral](https://github.com/your-org/spiral) ecosystem
