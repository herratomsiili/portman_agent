import { Routes } from '@angular/router';
import { StandaloneTestComponent } from './standalone-test.component';

export const routes: Routes = [
  { path: '', redirectTo: '/voyages', pathMatch: 'full' },
  { 
    path: 'voyages', 
    loadComponent: () => import('./pages/voyages-page/voyages-page.component').then(m => m.VoyagesPageComponent),
  },
  {
    path: 'standalone-test',
    component: StandaloneTestComponent
  }
];
