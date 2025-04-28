// Import Zone.js
import 'zone.js';

// Import the compiler for JIT compilation
import '@angular/compiler';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';

console.log('Starting application bootstrap with dynamic platform');

// Wait for the DOM to be loaded before bootstrapping
function bootstrapApplication() {
  // Check if app-root element exists
  if (!document.querySelector('app-root')) {
    console.error('app-root element not found, creating one');
    // Create app-root element if it doesn't exist
    const appRoot = document.createElement('app-root');
    document.body.appendChild(appRoot);
  }

  // Use the dynamic platform
  platformBrowserDynamic()
    .bootstrapModule(AppModule)
    .catch((err: any) => console.error('Bootstrap error:', err));
}

// Bootstrap when the DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrapApplication);
} else {
  bootstrapApplication();
}
