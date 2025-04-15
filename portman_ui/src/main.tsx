import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import "leaflet/dist/leaflet.css"; // Leaflet styles

const root = document.getElementById('root')

if (root) {
    console.log("Creating root")
    ReactDOM.createRoot(root).render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    )
}
