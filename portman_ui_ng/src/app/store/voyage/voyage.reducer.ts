import { createReducer, on } from '@ngrx/store';
import { EntityState, EntityAdapter, createEntityAdapter } from '@ngrx/entity';
import { Voyage } from '../../models/voyage.model';
import * as VoyageActions from './voyage.actions';

export interface VoyageState extends EntityState<Voyage> {
  selectedVoyageId: number | null;
  loading: boolean;
  error: any;
}

export const adapter: EntityAdapter<Voyage> = createEntityAdapter<Voyage>({
  selectId: (voyage: Voyage) => voyage.portcallid,
  sortComparer: (a: Voyage, b: Voyage) => {
    // Sort by eta, with most recent first
    const aDate = a.eta ? new Date(a.eta).getTime() : 0;
    const bDate = b.eta ? new Date(b.eta).getTime() : 0;
    return bDate - aDate;
  },
});

export const initialState: VoyageState = adapter.getInitialState({
  selectedVoyageId: null,
  loading: false,
  error: null
});

export const voyageReducer = createReducer(
  initialState,
  on(VoyageActions.loadVoyages, (state) => ({
    ...state,
    loading: true,
    error: null
  })),
  on(VoyageActions.loadVoyagesSuccess, (state, { voyages }) => 
    adapter.setAll(voyages, {
      ...state,
      loading: false
    })
  ),
  on(VoyageActions.loadVoyagesFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error
  })),
  on(VoyageActions.loadVoyage, (state, { id }) => ({
    ...state,
    selectedVoyageId: id,
    loading: true,
    error: null
  })),
  on(VoyageActions.loadVoyageSuccess, (state, { voyage }) => 
    adapter.upsertOne(voyage, {
      ...state,
      loading: false
    })
  ),
  on(VoyageActions.loadVoyageFailure, (state, { error }) => ({
    ...state,
    loading: false,
    error
  }))
);

// Export selectors
export const {
  selectIds,
  selectEntities,
  selectAll,
  selectTotal,
} = adapter.getSelectors(); 