import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { catchError, map, mergeMap, tap } from 'rxjs/operators';
import { VoyageService } from '../../services/voyage.service';
import * as VoyageActions from './voyage.actions';

@Injectable()
export class VoyageEffects {
  // Use the new inject function from Angular to get the dependencies
  private actions$ = inject(Actions);
  private voyageService = inject(VoyageService);

  constructor() {
    console.log('VoyageEffects initialized');
  }

  loadVoyages$ = createEffect(() => 
    this.actions$.pipe(
      ofType(VoyageActions.loadVoyages),
      tap(() => console.log('Effect: Load Voyages action triggered')),
      mergeMap(() => 
        this.voyageService.getVoyages().pipe(
          tap(voyages => console.log('Effect: Got voyages from service:', voyages)),
          map(voyages => {
            console.log('Effect: Dispatching loadVoyagesSuccess with:', voyages);
            return VoyageActions.loadVoyagesSuccess({ voyages })
          }),
          catchError(error => {
            console.error('Effect: Error loading voyages:', error);
            return of(VoyageActions.loadVoyagesFailure({ error: error.toString() }))
          })
        )
      )
    )
  );

  loadVoyage$ = createEffect(() => 
    this.actions$.pipe(
      ofType(VoyageActions.loadVoyage),
      tap(({ id }) => console.log('Effect: Load Voyage action triggered for id:', id)),
      mergeMap(({ id }) => 
        this.voyageService.getVoyageById(id).pipe(
          tap(voyage => console.log('Effect: Got voyage from service:', voyage)),
          map(voyage => VoyageActions.loadVoyageSuccess({ voyage })),
          catchError(error => {
            console.error(`Effect: Error loading voyage ${id}:`, error);
            return of(VoyageActions.loadVoyageFailure({ error: error.toString() }))
          })
        )
      )
    )
  );
} 