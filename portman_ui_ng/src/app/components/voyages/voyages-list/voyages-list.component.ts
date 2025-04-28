import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable, of, Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { AppState } from '../../../store';
import { Voyage } from '../../../models/voyage.model';
import * as VoyageActions from '../../../store/voyage/voyage.actions';
import * as VoyageSelectors from '../../../store/voyage/voyage.selectors';
import { CommonModule } from '@angular/common';
import { VoyageService } from '../../../services/voyage.service';
import { MOCK_VOYAGES } from '../../../data/mock-voyages';

@Component({
  selector: 'app-voyages-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './voyages-list.component.html',
  styleUrls: ['./voyages-list.component.scss']
})
export class VoyagesListComponent implements OnInit, OnDestroy {
  private store = inject(Store<AppState>);
  private voyageService = inject(VoyageService);
  
  voyages$: Observable<Voyage[]>;
  loading$: Observable<boolean>;
  error$: Observable<any>;
  
  // Directly use mock data for debugging
  debugMockVoyages: Voyage[] = MOCK_VOYAGES;
  
  // For cleanup of subscriptions
  private destroy$ = new Subject<void>();

  constructor() {
    console.log('VoyagesListComponent constructor called');
    
    // Initialize selectors
    this.voyages$ = this.store.select(VoyageSelectors.selectAllVoyages);
    this.loading$ = this.store.select(VoyageSelectors.selectVoyageLoading);
    this.error$ = this.store.select(VoyageSelectors.selectVoyageError);
    
    // Log state changes - for debugging only
    this.voyages$.pipe(takeUntil(this.destroy$)).subscribe(voyages => {
      console.log('Voyages from store:', voyages);
    });
    
    this.loading$.pipe(takeUntil(this.destroy$)).subscribe(loading => {
      console.log('Loading state:', loading);
    });
    
    this.error$.pipe(takeUntil(this.destroy$)).subscribe(error => {
      if (error) {
        console.error('Error from store:', error);
      }
    });
  }

  ngOnInit(): void {
    console.log('VoyagesListComponent initialized, dispatching loadVoyages action');
    this.store.dispatch(VoyageActions.loadVoyages());
    
    // Direct API call for debugging
    this.voyageService.getVoyages().subscribe({
      next: (voyages) => console.log('Direct API call result:', voyages),
      error: (err) => console.error('Direct API call error:', err)
    });
  }
  
  ngOnDestroy(): void {
    // Clean up subscriptions to prevent memory leaks
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  formatDate(dateString: string | undefined): string {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  }
} 