import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TestComponent } from './test.component';

@Component({
  selector: 'app-root-standalone',
  standalone: true,
  imports: [RouterOutlet, RouterLink, CommonModule, TestComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'Portman';

  ngOnInit(): void {
    console.log('App component initialized');
    
    // Check if Redux DevTools extension is available
    if (typeof window !== 'undefined') {
      console.log('Redux DevTools available:', !!(window as any).__REDUX_DEVTOOLS_EXTENSION__);
    }

    // Log any uncaught errors
    window.onerror = function(message, source, lineno, colno, error) {
      console.error('Global error caught:', message);
      console.error('Error details:', error);
      return false;
    };
  }
}
