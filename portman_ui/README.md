# Portman UI

Portman UI is a modern, TypeScript-based React frontend for tracking maritime vessel port calls. It integrates with the Portman Agent backend and is designed for responsive use on desktop and mobile devices.

Built using [Vite](https://vitejs.dev/) for blazing fast development and optimized production builds.

---

## 🚀 Features

- ⚛️ React 19 with TypeScript
- 🎨 Material UI (MUI 6) + Emotion for styling
- 📊 Chart.js integration for data visualization
- 🔗 React Router v7 for navigation
- 🔍 Axios for API communication
- 🧪 Testing with Testing Library + Jest

---

## 🛠️ Getting Started

### 1. Install dependencies

```bash
npm install
```

### 2. Start development server

```bash
npm run dev
```

The app will be available at http://localhost:3000

### 3. 📦 Build for Production

```bash
npm run build
```

Compiled output will be located in the dist/ directory.

### 4. 🔍 Preview Production Build

```bash
npm run preview
```

Runs a local static file server to test the production build.

### 5. 🧪 Run Tests

```bash
npm test
```

### 6. 🧹 Lint the Project

```bash
npm run lint
```

### UI Structure

```plaintext
portman-ui/
├── index.html          # Vite HTML entry
├── vite.config.ts      # Vite config
├── public/             # Static assets (favicon, manifest, etc.)
├── src/
│   ├── main.tsx        # App entry point
│   ├── App.tsx         # Root component
│   ├── components/     # Reusable UI components
│   └── index.css       # Global styles
```