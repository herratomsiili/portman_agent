# Portman UI Angular

This is an Angular-based UI for the Portman port management system. The application provides a modern interface for managing port operations, vessel voyages, and related data.

## Features

- Voyages listing view
- Redux state management with NgRx
- TypeScript for type safety
- Vite for fast development and building

## Project Structure

```
portman_ui_ng/
├── src/
│   ├── app/
│   │   ├── components/  # Reusable components
│   │   │   └── voyages/ # Voyage-related components
│   │   ├── config/      # Configuration files
│   │   ├── models/      # TypeScript interfaces
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── store/       # NgRx store (Redux)
│   ├── assets/          # Static assets
│   └── styles.scss      # Global styles
└── ...
```

## Getting Started

### Prerequisites

- Node.js (latest LTS version recommended)
- npm (comes with Node.js)

### Installation

1. Clone the repository
2. Navigate to the project directory:
   ```
   cd portman_ui_ng
   ```
3. Install dependencies:
   ```
   npm install
   ```

### Development

To start the development server with Angular CLI:

```
npm start
```

Or to use Vite for faster development:

```
npm run dev
```

This will start the development server at http://localhost:4200.

### Building for Production

To build the application for production:

```
npm run build
```

Or with Vite:

```
npm run build:vite
```

The built files will be in the `dist` directory.

## Comparison with React UI

This Angular UI is structured similarly to the existing React UI (`portman_ui`), but uses Angular-specific patterns and libraries:

- NgRx for state management (equivalent to Redux in React)
- Angular Router for routing
- Angular's dependency injection for services
- Standalone components for better modularity

## License

This project is part of the Portman system.
