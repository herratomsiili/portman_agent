import { createFeatureSelector, createSelector } from '@ngrx/store';
import { VoyageState, selectAll, selectEntities } from './voyage.reducer';

export const selectVoyageState = createFeatureSelector<VoyageState>('voyages');

export const selectAllVoyages = createSelector(
  selectVoyageState,
  selectAll
);

export const selectVoyageEntities = createSelector(
  selectVoyageState,
  selectEntities
);

export const selectVoyageLoading = createSelector(
  selectVoyageState,
  (state: VoyageState) => state.loading
);

export const selectVoyageError = createSelector(
  selectVoyageState,
  (state: VoyageState) => state.error
);

export const selectSelectedVoyageId = createSelector(
  selectVoyageState,
  (state: VoyageState) => state.selectedVoyageId
);

export const selectSelectedVoyage = createSelector(
  selectVoyageEntities,
  selectSelectedVoyageId,
  (entities, selectedId) => selectedId ? entities[selectedId] : null
);

// Active voyages (with ata set)
export const selectActiveVoyages = createSelector(
  selectAllVoyages,
  (voyages) => voyages.filter(voyage => voyage.ata !== undefined && voyage.ata !== null)
);

// Upcoming voyages (with ata not set)
export const selectUpcomingVoyages = createSelector(
  selectAllVoyages,
  (voyages) => voyages.filter(voyage => voyage.ata === undefined || voyage.ata === null)
    .sort((a, b) => {
      const aDate = a.eta ? new Date(a.eta).getTime() : 0;
      const bDate = b.eta ? new Date(b.eta).getTime() : 0;
      return aDate - bDate;
    })
); 