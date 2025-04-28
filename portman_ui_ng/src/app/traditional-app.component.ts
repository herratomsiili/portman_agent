import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  standalone: false,
  template: `
    <div class="app-container">
      <header class="app-header">
        <div class="app-logo">
          <h1>Portman</h1>
        </div>
        <nav class="app-nav">
          <ul>
            <li><a routerLink="/voyages">Voyages</a></li>
            <li><a routerLink="/standalone-test">Standalone Test</a></li>
          </ul>
        </nav>
      </header>
      
      <main class="app-content">
        <router-outlet></router-outlet>
      </main>
      
      <footer class="app-footer">
        <p>&copy; 2024 Portman - Angular Port Management System</p>
      </footer>
    </div>
  `,
  styles: [`
    .app-container {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }
    .app-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 2rem;
      background-color: #1565c0;
      color: white;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .app-logo h1 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 600;
    }
    .app-nav ul {
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .app-nav li {
      margin-left: 1.5rem;
    }
    .app-nav a {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      font-weight: 500;
    }
    .app-nav a:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
    .app-content {
      flex: 1;
      background-color: #f5f5f5;
    }
    .app-footer {
      padding: 1rem 2rem;
      background-color: #f0f0f0;
      border-top: 1px solid #e0e0e0;
      text-align: center;
      color: #666;
    }
    .app-footer p {
      margin: 0;
      font-size: 0.875rem;
    }
  `]
})
export class TraditionalAppComponent { } 