import { ActionReducerMap } from '@ngrx/store';
import { VoyageState, voyageReducer } from './voyage/voyage.reducer';
import { TestState, testReducer } from './test/test.reducer';
import { VoyageEffects } from './voyage/voyage.effects';

export interface AppState {
  voyages: VoyageState;
  test: TestState;
}

export const reducers: ActionReducerMap<AppState> = {
  voyages: voyageReducer,
  test: testReducer
};

export const effects = [
  VoyageEffects
]; 