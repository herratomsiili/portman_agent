import { Component } from '@angular/core';
import { VoyagesListComponent } from '../../components/voyages/voyages-list/voyages-list.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-voyages-page',
  standalone: true,
  imports: [CommonModule, VoyagesListComponent],
  template: `
    <div class="voyages-page">
      <header>
        <h1>{{ title }}</h1>
        <p class="subtitle">View and manage all vessel voyages in the port</p>
      </header>
      
      <app-voyages-list></app-voyages-list>
    </div>
  `,
  styles: [`
    .voyages-page {
      padding: 1.5rem;
    }
    
    header {
      margin-bottom: 2rem;
    }
    
    h1 {
      font-size: 2rem;
      margin-bottom: 0.5rem;
      color: #1565c0;
    }
    
    .subtitle {
      color: #666;
      font-size: 1.1rem;
      margin-top: 0;
    }
  `]
})
export class VoyagesPageComponent {
  title = 'Voyages Management';
} 