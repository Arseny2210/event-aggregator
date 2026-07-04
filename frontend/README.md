# Event Aggregator — Frontend

Next.js 15 + React 19 + TypeScript + Tailwind CSS application for the Event Aggregator platform.

## Stack

- **Framework**: Next.js 15 (App Router)
- **UI Library**: React 19
- **Language**: TypeScript (strict)
- **Styling**: Tailwind CSS 3.4
- **Data Fetching**: TanStack Query 5
- **Forms**: React Hook Form + Zod
- **State**: Zustand (UI) + React Context (Auth)
- **Icons**: Lucide React

## Getting Started

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Project Structure

```
src/
├── app/           # App Router routes
│   ├── (auth)/    # Public auth pages
│   └── (dashboard)/ # Protected dashboard
├── components/    # Reusable UI components
│   ├── ui/        # Primitives (Button, Input, Card)
│   ├── layout/    # Layout components
│   └── features/  # Feature components
├── lib/           # Core logic
│   ├── api/       # API client + endpoints
│   ├── hooks/     # Custom React hooks
│   ├── providers/ # Context providers
│   ├── store/     # Zustand stores
│   └── utils/     # Utilities
├── types/         # TypeScript types
└── config.ts      # App configuration
```

## Commands

- `npm run dev` — Start dev server
- `npm run build` — Production build
- `npm run lint` — Run ESLint
- `npm run typecheck` — TypeScript check
- `npm run format` — Prettier format
