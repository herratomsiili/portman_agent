/// <reference types="vite/client" />

import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import * as path from 'path'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), '')

    return {
        root: 'src',
        plugins: [react()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src'),
            },
        },
        define: {
            __API_BASE_URL__: JSON.stringify(API_BASE_URL), // Usage: __API_BASE_URL__
        },
        build: {
            outDir: '../dist',
            emptyOutDir: true,
        },
        server: {
            port: 3000
        },
    }
})
