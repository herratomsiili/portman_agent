import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths';
import angular from '@analogjs/vite-plugin-angular';

export default defineConfig({
  plugins: [
    tsconfigPaths(),
    angular()
  ],
  resolve: {
    mainFields: ['module'],
    dedupe: ['@angular/core', '@angular/common']
  },
  server: {
    port: 4200,
    host: 'localhost',
    fs: {
      allow: ['..']
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['@angular/core', '@angular/common'],
          ngrx: ['@ngrx/store', '@ngrx/effects', '@ngrx/entity'],
        },
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // No additional data needed, let each file include what it needs
      },
    },
    devSourcemap: true,
  },
  optimizeDeps: {
    include: [
      '@angular/core', 
      '@angular/common',
      '@angular/platform-browser',
      '@angular/router',
      '@ngrx/store',
      '@ngrx/effects',
      '@ngrx/entity',
      'rxjs',
      'zone.js'
    ],
    exclude: ['@angular/compiler']
  },
  esbuild: {
    // Use these options to preserve Angular decorators during build
    legalComments: 'none',
    keepNames: true
  }
}); 